import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useQueryClient } from '@tanstack/react-query'
import { mealService, type MealResponse } from '../services/mealService'
import MealInput, { type MealLogFormFields } from '../components/meals/MealInput'
import NutritionBreakdown from '../components/meals/NutritionBreakdown'

type FormData = MealLogFormFields

export default function LogMeal() {
  const queryClient = useQueryClient()
  const [result, setResult] = useState<MealResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    defaultValues: { meal_type: 'lunch' },
  })

  const onSubmit = async (data: FormData) => {
    setError(null)
    setResult(null)
    setLoading(true)
    try {
      const res = await mealService.log(data.text, data.meal_type || undefined)
      setResult(res.data)
      queryClient.invalidateQueries({ queryKey: ['meals'] })
      queryClient.invalidateQueries({ queryKey: ['recommendations'] })
    } catch (e: unknown) {
      const err = e as {
        response?: { data?: { detail?: string | Array<{ msg?: string }>; message?: string }; status?: number }
        message?: string
      }
      const detail = err.response?.data?.detail
      let msg: string
      if (!err.response) {
        msg = 'Cannot reach server. Is the backend running?'
      } else if (typeof detail === 'string') {
        msg = detail
      } else if (Array.isArray(detail) && detail.length > 0) {
        msg = detail.map((x) => x.msg || JSON.stringify(x)).join('. ')
      } else {
        msg = err.response?.data?.message || `Failed to log meal (${err.response?.status ?? 'error'}). Check backend logs or OpenAI API key in backend/.env`
      }
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <h1 className="page-title">Log a meal</h1>
      <div className="card">
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="input-group">
            <label>Meal type</label>
            <select {...register('meal_type')}>
              <option value="breakfast">Breakfast</option>
              <option value="lunch">Lunch</option>
              <option value="dinner">Dinner</option>
              <option value="snack">Snack</option>
            </select>
          </div>
          <MealInput register={register} disabled={loading} error={errors.text?.message} />
          {error && <p className="error-msg">{error}</p>}
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Parsing & saving…' : 'Log meal'}
          </button>
        </form>
      </div>
      {result && (
        <div className="card">
          <h2 style={{ marginTop: 0, marginBottom: '0.75rem' }}>Logged meal</h2>
          <ul style={{ margin: '0 0 1rem', paddingLeft: '1.25rem' }}>
            {result.items.map((i) => (
              <li key={i.id}>
                {i.quantity} {i.unit || ''} {i.food_name}
                {i.portion_size_category ? ` (${i.portion_size_category})` : ''}
              </li>
            ))}
          </ul>
          <NutritionBreakdown
            calories={result.calories}
            protein_g={result.protein_g}
            carbs_g={result.carbs_g}
            fat_g={result.fat_g}
          />
        </div>
      )}
    </>
  )
}
