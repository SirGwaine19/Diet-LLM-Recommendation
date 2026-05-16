import { api } from './api'

export interface MealItemResponse {
  id: number
  food_name: string
  quantity: number
  unit: string | null
  portion_size_category: string | null
  preparation_method: string | null
}

export interface MealResponse {
  id: number
  user_id: number
  timestamp: string
  meal_type: string | null
  source: string
  items: MealItemResponse[]
  calories: number | null
  protein_g: number | null
  carbs_g: number | null
  fat_g: number | null
}

interface MealListOptions {
  limit?: number
  startDate?: string
  endDate?: string
}

export const mealService = {
  log: (text: string, meal_type?: string) =>
    api.post<MealResponse>('/meals/log', { text, meal_type }),

  list: ({ limit = 50, startDate, endDate }: MealListOptions = {}) =>
    api.get<MealResponse[]>('/meals', {
      params: { limit, start_date: startDate, end_date: endDate },
    }),

  get: (mealId: number) =>
    api.get<MealResponse>(`/meals/${mealId}`),

  delete: (mealId: number) =>
    api.delete(`/meals/${mealId}`),
}
