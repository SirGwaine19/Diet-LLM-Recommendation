import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { recommendationService } from '../services/recommendationService'
import { mealService } from '../services/mealService'
import { userService } from '../services/userService'
import DailySummary from '../components/recommendations/DailySummary'
import NutritionProgress from '../components/dashboard/NutritionProgress'
import WeeklyProgressGraph from '../components/dashboard/WeeklyProgressGraph'
import { useState } from 'react'
import { format, startOfWeek, addDays, subWeeks, addWeeks, isSameWeek } from 'date-fns'

export default function Dashboard() {
  const [weekStart, setWeekStart] = useState(() => startOfWeek(new Date(), { weekStartsOn: 1 }))
  const weekEnd = addDays(weekStart, 6)
  const isCurrentWeek = isSameWeek(weekStart, new Date(), { weekStartsOn: 1 })

  const { data: user } = useQuery({
    queryKey: ['user'],
    queryFn: () => userService.getMe().then((r) => r.data),
  })
  const { data: dailyRec, isLoading: recLoading, refetch: refetchRec } = useQuery({
    queryKey: ['recommendations', 'daily'],
    queryFn: () => recommendationService.getDaily().then((r) => r.data),
  })
  const { data: weekMeals } = useQuery({
    queryKey: ['meals', 'week', format(weekStart, 'yyyy-MM-dd')],
    queryFn: () =>
      mealService
        .list({
          limit: 500,
          startDate: format(weekStart, 'yyyy-MM-dd'),
          endDate: format(weekEnd, 'yyyy-MM-dd'),
        })
        .then((r) => r.data),
  })

  const { data: meals } = useQuery({
    queryKey: ['meals', 'today'],
    queryFn: () =>
      mealService
        .list({
          limit: 200,
          startDate: format(new Date(), 'yyyy-MM-dd'),
          endDate: format(new Date(), 'yyyy-MM-dd'),
        })
        .then((r) => r.data),
  })

  const todayMeals = meals?.filter((m) => {
    const d = new Date(m.timestamp)
    const today = new Date()
    return d.getDate() === today.getDate() && d.getMonth() === today.getMonth() && d.getFullYear() === today.getFullYear()
  }) ?? []

  const todayCal = todayMeals.reduce((s, m) => s + (m.calories ?? 0), 0)
  const todayProtein = todayMeals.reduce((s, m) => s + (m.protein_g ?? 0), 0)
  const todayCarbs = todayMeals.reduce((s, m) => s + (m.carbs_g ?? 0), 0)
  const todayFat = todayMeals.reduce((s, m) => s + (m.fat_g ?? 0), 0)

  return (
    <>
      <h1 className="page-title">Dashboard</h1>

      <div className="card">
        <NutritionProgress
          calories={todayCal}
          protein_g={todayProtein}
          carbs_g={todayCarbs}
          fat_g={todayFat}
          calorieTarget={user?.daily_calorie_target ?? undefined}
          proteinTarget={user?.protein_target_g ?? undefined}
          carbTarget={user?.carb_target_g ?? undefined}
          fatTarget={user?.fat_target_g ?? undefined}
        />
      </div>

      <div className="card">
        <WeeklyProgressGraph
          meals={weekMeals ?? []}
          weekStart={weekStart}
          onPreviousWeek={() => setWeekStart((d) => subWeeks(d, 1))}
          onNextWeek={() => setWeekStart((d) => addWeeks(d, 1))}
          disableNextWeek={isCurrentWeek}
          calorieTarget={user?.daily_calorie_target ?? undefined}
        />
      </div>

      <div className="card">
        <h2 style={{ marginTop: 0, marginBottom: '0.75rem' }}>Today&apos;s summary</h2>
        {recLoading ? (
          <p className="loading">Loading…</p>
        ) : (
          <DailySummary
            recommendation={dailyRec ?? null}
            onGenerate={refetchRec}
          />
        )}
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
          <h2 style={{ margin: 0 }}>Recent meals</h2>
          <Link to="/log-meal" className="btn btn-primary">Log meal</Link>
        </div>
        {!todayMeals.length ? (
          <p style={{ margin: 0, color: 'var(--text-muted)' }}>No meals logged today. <Link to="/log-meal">Log a meal</Link>.</p>
        ) : (
          <ul style={{ margin: 0, paddingLeft: '1.25rem' }}>
            {todayMeals.slice(0, 5).map((m) => (
              <li key={m.id}>
                {m.meal_type} – {m.items.map((i) => i.food_name).join(', ')} ({format(new Date(m.timestamp), 'h:mm a')})
              </li>
            ))}
          </ul>
        )}
      </div>
    </>
  )
}
