import { API_BASE } from '../services/api'

export function networkErrorMessage(): string {
  if (API_BASE.startsWith('http')) {
    return `Cannot reach the API (${API_BASE}). The server may be waking up (wait ~1 min on free tier) or still deploying.`
  }
  return 'Cannot reach the API. Start the backend (e.g. uvicorn on port 8000 or Docker compose).'
}
