// Cliente HTTP minimalista para a API do CashMe (FastAPI /api/v1)
const API_BASE = '/api/v1';
const TOKEN_KEY = 'cashme.token';
const USER_KEY = 'cashme.user';

export function setToken(token: string) { localStorage.setItem(TOKEN_KEY, token); }
export function getToken(): string | null { return localStorage.getItem(TOKEN_KEY); }
export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}
export function setStoredUser(u: AuthUser) { localStorage.setItem(USER_KEY, JSON.stringify(u)); }
export function getStoredUser(): AuthUser | null {
  const raw = localStorage.getItem(USER_KEY);
  return raw ? (JSON.parse(raw) as AuthUser) : null;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...((init?.headers as Record<string, string>) || {}),
  };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, { ...init, headers });
  if (res.status === 401) {
    clearAuth();
    if (!location.pathname.endsWith('/ui/login') && !location.pathname.endsWith('/ui/')) {
      location.href = '/ui/login';
    }
    throw new Error('Não autenticado');
  }
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`HTTP ${res.status}: ${detail}`);
  }
  const ct = res.headers.get('content-type') || '';
  return ct.includes('json') ? ((await res.json()) as T) : ((await res.text()) as unknown as T);
}

export interface AuthUser {
  user_id: number;
  email: string;
  full_name: string;
  role: 'cliente' | 'analista' | 'admin';
}
export interface TokenResponse extends AuthUser { access_token: string; token_type: string; }

export interface ChatRequest {
  message: string; session_id?: string; agent?: 'langchain' | 'agno';
  provider?: string; model?: string; use_guardrails?: boolean;
}
export interface ChatResponse { response: string; session_id: string; agent: string; }

export interface ScoreRequest {
  monthly_income: number; property_value: number; requested_amount: number;
  employment_years?: number; age?: number; has_other_debts?: boolean;
  profession?: string; loan_purpose?: string;
}
export interface ScoreResponse {
  score: number; approved: boolean; ltv: number; monthly_installment: number;
  risk_factors: string[]; explanation: string;
}

export interface IngestURLRequest { url: string; bypass_cache?: boolean; }
export interface IngestResponse { chunks_added: number; source: string; message: string; }
export interface SearchResult { content: string; source: string; score: number; }

export interface SimulationResponse {
  id: number; status: string; amount_requested: number;
  score_snapshot: ScoreResponse | null; public_message: string | null;
  created_at: string; decided_at: string | null;
}

export interface QueueItem {
  id: number; amount_requested: number; status: string;
  client_name: string; client_email: string;
  score_snapshot: ScoreResponse | null; created_at: string;
  assigned_analyst_id: number | null;
}

export interface SessionInfo {
  id: number; request_id: number; thread_id: string; analyst_id: number;
  opened_at: string; closed_at: string | null;
}

export interface SessionDetail {
  session: SessionInfo;
  request: Record<string, unknown>;
  client: Record<string, unknown>;
  messages: Array<{
    role: string; agent_name: string | null;
    content: string; event_type: string | null;
    metadata: Record<string, unknown>; created_at: string;
  }>;
  attachments: Array<{
    id: number; filename: string; mime: string;
    size_bytes: number; chunks_indexed: number; created_at: string;
  }>;
}

export interface ClientNotificationT {
  id: number; title: string; body: string; request_id: number | null;
  read: boolean; created_at: string;
}

export const api = {
  // auth
  login: async (email: string, password: string): Promise<TokenResponse> => {
    const body = new URLSearchParams();
    body.set('username', email);
    body.set('password', password);
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
    });
    if (!res.ok) throw new Error('Credenciais inválidas');
    return res.json();
  },
  me: () => request<AuthUser>('/auth/me'),
  register: (email: string, password: string, full_name: string) =>
    request<AuthUser>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, full_name, role: 'cliente' }),
    }),

  // legado
  health: () => request<{ status: string }>('/health'),
  chat: (body: ChatRequest) =>
    request<ChatResponse>('/chat', { method: 'POST', body: JSON.stringify(body) }),
  score: (body: ScoreRequest) =>
    request<ScoreResponse>('/score', { method: 'POST', body: JSON.stringify(body) }),
  retrain: () => request<Record<string, unknown>>('/score/retrain', { method: 'POST' }),
  ingestUrl: (body: IngestURLRequest) =>
    request<IngestResponse>('/ingest/url', { method: 'POST', body: JSON.stringify(body) }),
  ingestDoc: async (file: File): Promise<IngestResponse> => {
    const fd = new FormData();
    fd.append('file', file);
    const token = getToken();
    const res = await fetch(`${API_BASE}/ingest/doc`, {
      method: 'POST', body: fd,
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    return res.json();
  },
  search: (q: string, k = 4) =>
    request<SearchResult[]>(`/search?q=${encodeURIComponent(q)}&k=${k}`),

  // cliente
  submitSimulation: (body: ScoreRequest) =>
    request<SimulationResponse>('/client/simulations', { method: 'POST', body: JSON.stringify(body) }),
  listMySimulations: () => request<SimulationResponse[]>('/client/simulations'),
  getMySimulation: (id: number) => request<SimulationResponse>(`/client/simulations/${id}`),
  listNotifications: () => request<ClientNotificationT[]>('/client/notifications'),
  markNotificationRead: (id: number) =>
    request<{ status: string }>(`/client/notifications/${id}/read`, { method: 'POST' }),

  // analista
  listQueue: (f: 'pending_analyst' | 'mine' | 'all_open' = 'pending_analyst') =>
    request<QueueItem[]>(`/analyst/queue?status_filter=${f}`),
  claim: (reqId: number) =>
    request<SessionInfo>(`/analyst/queue/${reqId}/claim`, { method: 'POST' }),
  getSession: (sessId: number) => request<SessionDetail>(`/analyst/sessions/${sessId}`),
  uploadAttachment: async (sessId: number, file: File) => {
    const fd = new FormData();
    fd.append('file', file);
    const token = getToken();
    const res = await fetch(`${API_BASE}/analyst/sessions/${sessId}/attachments`, {
      method: 'POST', body: fd,
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    return res.json();
  },

  // admin
  listUsers: () => request<Array<{
    id: number; email: string; full_name: string; role: string; created_at: string;
  }>>('/admin/users'),
  createUser: (data: { email: string; password: string; full_name: string; role: string }) =>
    request('/admin/users', { method: 'POST', body: JSON.stringify(data) }),
  deleteUser: (id: number) =>
    request(`/admin/users/${id}`, { method: 'DELETE' }),
};

export function wsUrl(sessId: number): string {
  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const token = getToken() || '';
  return `${proto}//${location.host}/ws/analyst/sessions/${sessId}?token=${encodeURIComponent(token)}`;
}
