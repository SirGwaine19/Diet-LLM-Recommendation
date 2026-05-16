import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import type { RecommendationResponse } from '../../services/recommendationService'
import { recommendationService } from '../../services/recommendationService'

interface Props {
  recommendation: RecommendationResponse | null
  onGenerate: () => void
}

export default function DailySummary({ recommendation, onGenerate }: Props) {
  const queryClient = useQueryClient()
  const [feedbackSent, setFeedbackSent] = useState(false)

  const generate = useMutation({
    mutationFn: () => recommendationService.generate(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recommendations'] })
      onGenerate()
    },
  })

  const sendFeedback = useMutation({
    mutationFn: ({ id, feedback }: { id: number; feedback: string }) =>
      recommendationService.feedback(id, feedback),
    onSuccess: () => setFeedbackSent(true),
  })

  if (!recommendation) {
    return (
      <div>
        <p style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>
          No summary for today yet. Generate one based on your meals and goals.
        </p>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => generate.mutate()}
          disabled={generate.isPending}
        >
          {generate.isPending ? 'Generating…' : 'Generate today\'s summary'}
        </button>
      </div>
    )
  }

  return (
    <div>
      <div
        style={{
          whiteSpace: 'pre-wrap',
          marginBottom: '1rem',
          lineHeight: 1.6,
        }}
      >
        {recommendation.content}
      </div>
      {!feedbackSent && (
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => sendFeedback.mutate({ id: recommendation.id, feedback: 'liked' })}
            disabled={sendFeedback.isPending}
          >
            Like
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => sendFeedback.mutate({ id: recommendation.id, feedback: 'ignored' })}
            disabled={sendFeedback.isPending}
          >
            Ignore
          </button>
        </div>
      )}
      {feedbackSent && <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.9rem' }}>Thanks for your feedback.</p>}
    </div>
  )
}
