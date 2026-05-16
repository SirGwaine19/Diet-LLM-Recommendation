import { api } from './api'

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  email: string
  password: string
  full_name?: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface MeResponse {
  id: number
  email: string
  full_name: string | null
}

export const authService = {
  register: (data: RegisterPayload) =>
    api.post<TokenResponse>('/auth/register', data),

  login: (data: LoginPayload) =>
    api.post<TokenResponse>('/auth/login', data),

  me: () =>
    api.get<MeResponse>('/auth/me'),
}
