import { format } from 'date-fns'
import type { MealResponse } from '../../services/mealService'
import NutritionBreakdown from './NutritionBreakdown'

interface Props {
  meal: MealResponse
  onDelete: () => void
  isDeleting?: boolean
}

export default function MealCard({ meal, onDelete, isDeleting }: Props) {
  const time = format(new Date(meal.timestamp), 'MMM d, yyyy · h:mm a')
  const type = meal.meal_type ? meal.meal_type.charAt(0).toUpperCase() + meal.meal_type.slice(1) : 'Meal'

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
        <div>
          <span style={{ fontWeight: 600 }}>{type}</span>
          <span style={{ color: 'var(--text-muted)', marginLeft: '0.5rem' }}>{time}</span>
        </div>
        <button
          type="button"
          className="btn btn-danger"
          onClick={onDelete}
          disabled={isDeleting}
        >
          {isDeleting ? 'Deleting…' : 'Delete'}
        </button>
      </div>
      <ul style={{ margin: '0 0 1rem', paddingLeft: '1.25rem' }}>
        {meal.items.map((i) => (
          <li key={i.id}>
            {i.quantity} {i.unit || ''} {i.food_name}
            {i.portion_size_category ? ` (${i.portion_size_category})` : ''}
          </li>
        ))}
      </ul>
      <NutritionBreakdown
        calories={meal.calories}
        protein_g={meal.protein_g}
        carbs_g={meal.carbs_g}
        fat_g={meal.fat_g}
      />
    </div>
  )
}
