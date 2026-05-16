import { create } from 'zustand'

const TOKEN_KEY = 'token'

type AuthStore = {
  token: string | null
  setToken: (t: string | null) => void
  logout: () => void
}

export const useAuthStore = create<AuthStore>((set) => ({
  token: typeof window !== 'undefined' ? localStorage.getItem(TOKEN_KEY) : null,
  setToken: (t) => {
    if (t) localStorage.setItem(TOKEN_KEY, t)
    else localStorage.removeItem(TOKEN_KEY)
    set({ token: t })
  },
  logout: () => {
    localStorage.removeItem(TOKEN_KEY)
    set({ token: null })
  },
}))
