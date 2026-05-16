import { addDays, format, isSameDay } from 'date-fns'
import type { MealResponse } from '../../services/mealService'

interface DayProgress {
  date: Date
  calories: number
  protein: number
  carbs: number
  fat: number
}

interface Props {
  meals: MealResponse[]
  weekStart: Date
  onPreviousWeek: () => void
  onNextWeek: () => void
  disableNextWeek?: boolean
  calorieTarget?: number
}

function buildWeeklyData(meals: MealResponse[], weekStart: Date): DayProgress[] {
  const days = Array.from({ length: 7 }, (_, idx) => {
    const date = addDays(weekStart, idx)
    return {
      date,
      calories: 0,
      protein: 0,
      carbs: 0,
      fat: 0,
    }
  })

  for (const meal of meals) {
    const mealDate = new Date(meal.timestamp)
    const day = days.find((d) => isSameDay(d.date, mealDate))
    if (!day) continue

    day.calories += meal.calories ?? 0
    day.protein += meal.protein_g ?? 0
    day.carbs += meal.carbs_g ?? 0
    day.fat += meal.fat_g ?? 0
  }

  return days
}

export default function WeeklyProgressGraph({
  meals,
  weekStart,
  onPreviousWeek,
  onNextWeek,
  disableNextWeek = false,
  calorieTarget,
}: Props) {
  const weeklyData = buildWeeklyData(meals, weekStart)
  const peakCalories = Math.max(...weeklyData.map((d) => d.calories), calorieTarget ?? 0, 1)
  const weekEnd = addDays(weekStart, 6)

  const chartWidth = 560
  const chartHeight = 160
  const xStep = chartWidth / 6

  const points = weeklyData
    .map((d, i) => {
      const x = i * xStep
      const y = chartHeight - (d.calories / peakCalories) * chartHeight
      return `${x},${y}`
    })
    .join(' ')

  const totalCalories = weeklyData.reduce((sum, d) => sum + d.calories, 0)
  const avgCalories = Math.round(totalCalories / 7)

  return (
    <div>
      <div className="weekly-progress-header">
        <div className="weekly-title-wrap">
          <h2 style={{ margin: 0 }}>Weekly progress</h2>
          <p style={{ margin: 0, color: 'var(--text-muted)' }}>
            {format(weekStart, 'dd MMM')} - {format(weekEnd, 'dd MMM yyyy')}
          </p>
        </div>
        <div className="weekly-actions">
          <button type="button" className="btn btn-secondary" onClick={onPreviousWeek}>
            Previous
          </button>
          <button type="button" className="btn btn-secondary" onClick={onNextWeek} disabled={disableNextWeek}>
            Next
          </button>
        </div>
      </div>
      <p style={{ margin: '0 0 0.75rem', color: 'var(--text-muted)' }}>Avg calories/day: {avgCalories}</p>

      <div className="weekly-chart-wrap">
        <svg viewBox={`0 0 ${chartWidth} ${chartHeight}`} className="weekly-chart" role="img" aria-label="Calories trend over last 7 days">
          <polyline points={points} fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
          {weeklyData.map((d, i) => {
            const x = i * xStep
            const y = chartHeight - (d.calories / peakCalories) * chartHeight
            return <circle key={format(d.date, 'yyyy-MM-dd')} cx={x} cy={y} r="4" fill="var(--accent)" />
          })}
        </svg>
      </div>

      <div className="weekly-bars">
        {weeklyData.map((day) => {
          const pct = Math.min((day.calories / peakCalories) * 100, 100)
          return (
            <div className="weekly-bar-item" key={format(day.date, 'yyyy-MM-dd')}>
              <div className="weekly-bar-label">{format(day.date, 'EEE')}</div>
              <div className="weekly-bar-bg">
                <div className="weekly-bar-fill" style={{ width: `${pct}%` }} />
              </div>
              <div className="weekly-bar-meta">
                <span>{Math.round(day.calories)} kcal</span>
                <span>
                  P {Math.round(day.protein)} / C {Math.round(day.carbs)} / F {Math.round(day.fat)}
                </span>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
