/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_PANEL_BASE?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
