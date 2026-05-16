import { Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { mealService } from '../services/mealService'
import MealCard from '../components/meals/MealCard'

export default function MealHistory() {
  const queryClient = useQueryClient()
  const { data: meals, isLoading, error } = useQuery({
    queryKey: ['meals'],
    queryFn: () => mealService.list().then((r) => r.data),
  })

  const deleteMeal = useMutation({
    mutationFn: (id: number) => mealService.delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['meals'] }),
  })

  if (isLoading) return <div className="loading">Loading meals…</div>
  if (error) return <div className="loading">Failed to load meals.</div>

  return (
    <>
      <h1 className="page-title">Meal history</h1>
      {!meals?.length ? (
        <div className="card">
          <p style={{ margin: 0, color: 'var(--text-muted)' }}>No meals logged yet. <Link to="/log-meal">Log your first meal</Link>.</p>
        </div>
      ) : (
        meals.map((meal) => (
          <MealCard
            key={meal.id}
            meal={meal}
            onDelete={() => deleteMeal.mutate(meal.id)}
            isDeleting={deleteMeal.isPending}
          />
        ))
      )}
    </>
  )
}
