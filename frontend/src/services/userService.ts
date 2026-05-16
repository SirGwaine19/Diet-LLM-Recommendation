import { api } from './api'

export interface UserResponse {
  id: number
  email: string
  full_name: string | null
  age: number | null
  sex: string | null
  height_cm: number | null
  weight_kg: number | null
  target_weight_kg: number | null
  activity_level: string | null
  dietary_preferences: string[]
  allergies: string[]
  cultural_preferences: string[]
  daily_calorie_target: number | null
  protein_target_g: number | null
  carb_target_g: number | null
  fat_target_g: number | null
}

export interface UserUpdate {
  full_name?: string | null
  age?: number | null
  sex?: string | null
  height_cm?: number | null
  weight_kg?: number | null
  target_weight_kg?: number | null
  activity_level?: string | null
  dietary_preferences?: string[] | null
  allergies?: string[] | null
  cultural_preferences?: string[] | null
}

export interface GoalsResponse {
  daily_calorie_target: number | null
  protein_target_g: number | null
  carb_target_g: number | null
  fat_target_g: number | null
}

export interface GoalsUpdate {
  daily_calorie_target?: number | null
  protein_target_g?: number | null
  carb_target_g?: number | null
  fat_target_g?: number | null
}

export const userService = {
  getMe: () => api.get<UserResponse>('/users/me'),
  updateMe: (data: UserUpdate) => api.put<UserResponse>('/users/me', data),
  getGoals: () => api.get<GoalsResponse>('/users/me/goals'),
  updateGoals: (data: GoalsUpdate) => api.put<GoalsResponse>('/users/me/goals', data),
}
