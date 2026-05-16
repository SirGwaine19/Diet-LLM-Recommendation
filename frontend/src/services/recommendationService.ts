import { api } from './api'

export interface RecommendationResponse {
  id: number
  user_id: number
  type: string
  content: string
  generated_at: string
  user_feedback: string | null
}

export const recommendationService = {
  getDaily: () =>
    api.get<RecommendationResponse | null>('/recommendations/daily'),

  generate: () =>
    api.post<RecommendationResponse>('/recommendations/generate'),

  feedback: (recommendationId: number, feedback: string) =>
    api.post(`/recommendations/${recommendationId}/feedback`, { feedback }),
}
