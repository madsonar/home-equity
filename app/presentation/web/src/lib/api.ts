// Cliente HTTP minimalista para a API do CashMe (FastAPI /api/v1)
const API_BASE = '/api/v1';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) },
    ...init,
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`HTTP ${res.status}: ${detail}`);
  }
  return res.json() as Promise<T>;
}

// ── tipos ────────────────────────────────────────────────────────────
export interface ChatRequest {
  message: string;
  session_id?: string;
  agent?: 'langchain' | 'agno';
  provider?: string;
  model?: string;
  use_guardrails?: boolean;
}
export interface ChatResponse {
  response: string;
  session_id: string;
  agent: string;
}

export interface ScoreRequest {
  monthly_income: number;
  property_value: number;
  requested_amount: number;
  employment_years?: number;
  age?: number;
  has_other_debts?: boolean;
  profession?: string;
  loan_purpose?: string;
}
export interface ScoreResponse {
  score: number;
  approved: boolean;
  ltv: number;
  monthly_installment: number;
  risk_factors: string[];
  explanation: string;
}

export interface IngestURLRequest {
  url: string;
  bypass_cache?: boolean;
}
export interface IngestResponse {
  chunks_added: number;
  source: string;
  message: string;
}

export interface SearchResult {
  content: string;
  source: string;
  score: number;
}

// ── endpoints ────────────────────────────────────────────────────────
export const api = {
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
    const res = await fetch(`${API_BASE}/ingest/doc`, { method: 'POST', body: fd });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    return res.json();
  },
  search: (q: string, k = 4) =>
    request<SearchResult[]>(`/search?q=${encodeURIComponent(q)}&k=${k}`),
};
