import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { userService, type UserResponse, type UserUpdate, type GoalsUpdate } from '../services/userService'

export default function Profile() {
  const queryClient = useQueryClient()
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user'],
    queryFn: () => userService.getMe().then((r) => r.data),
  })

  const updateProfile = useMutation({
    mutationFn: (data: UserUpdate) => userService.updateMe(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['user'] }),
  })

  const updateGoals = useMutation({
    mutationFn: (data: GoalsUpdate) => userService.updateGoals(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['user'] }),
  })

  if (isLoading) return <div className="loading">Loading profile…</div>
  if (error || !user) return <div className="loading">Failed to load profile.</div>

  return (
    <>
      <h1 className="page-title">Profile</h1>

      <div className="card">
        <h2 style={{ marginTop: 0, marginBottom: '1rem' }}>Profile</h2>
        <ProfileForm user={user} onSubmit={(d) => updateProfile.mutate(d)} isSubmitting={updateProfile.isPending} />
      </div>

      <div className="card">
        <h2 style={{ marginTop: 0, marginBottom: '1rem' }}>Goals</h2>
        <GoalsForm user={user} onSubmit={(d) => updateGoals.mutate(d)} isSubmitting={updateGoals.isPending} />
      </div>
    </>
  )
}

function ProfileForm({
  user,
  onSubmit,
  isSubmitting,
}: {
  user: UserResponse
  onSubmit: (d: UserUpdate) => void
  isSubmitting: boolean
}) {
  const { register, handleSubmit } = useForm<UserUpdate & { dietary_preferences_str?: string; allergies_str?: string; cultural_preferences_str?: string }>({
    defaultValues: {
      full_name: user.full_name ?? '',
      age: user.age ?? undefined,
      sex: user.sex ?? '',
      height_cm: user.height_cm ?? undefined,
      weight_kg: user.weight_kg ?? undefined,
      target_weight_kg: user.target_weight_kg ?? undefined,
      activity_level: user.activity_level ?? '',
      dietary_preferences_str: user.dietary_preferences?.join(', ') ?? '',
      allergies_str: user.allergies?.join(', ') ?? '',
      cultural_preferences_str: user.cultural_preferences?.join(', ') ?? '',
    },
  })

  const onFormSubmit = (data: UserUpdate & { dietary_preferences_str?: string; allergies_str?: string; cultural_preferences_str?: string }) => {
    const { dietary_preferences_str, allergies_str, cultural_preferences_str, ...rest } = data
    onSubmit({
      ...rest,
      dietary_preferences: dietary_preferences_str ? dietary_preferences_str.split(',').map((s) => s.trim()).filter(Boolean) : undefined,
      allergies: allergies_str ? allergies_str.split(',').map((s) => s.trim()).filter(Boolean) : undefined,
      cultural_preferences: cultural_preferences_str ? cultural_preferences_str.split(',').map((s) => s.trim()).filter(Boolean) : undefined,
    })
  }

  return (
    <form onSubmit={handleSubmit(onFormSubmit)}>
      <div className="input-group">
        <label>Full name</label>
        <input type="text" {...register('full_name')} />
      </div>
      <div className="input-group">
        <label>Age</label>
        <input type="number" min={1} max={120} {...register('age', { valueAsNumber: true })} />
      </div>
      <div className="input-group">
        <label>Sex</label>
        <select {...register('sex')}>
          <option value="">—</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>
      </div>
      <div className="input-group">
        <label>Height (cm)</label>
        <input type="number" min={50} max={300} step={0.1} {...register('height_cm', { valueAsNumber: true })} />
      </div>
      <div className="input-group">
        <label>Weight (kg)</label>
        <input type="number" min={20} max={500} step={0.1} {...register('weight_kg', { valueAsNumber: true })} />
      </div>
      <div className="input-group">
        <label>Target weight (kg)</label>
        <input type="number" min={20} max={500} step={0.1} {...register('target_weight_kg', { valueAsNumber: true })} />
      </div>
      <div className="input-group">
        <label>Activity level</label>
        <select {...register('activity_level')}>
          <option value="">—</option>
          <option value="sedentary">Sedentary</option>
          <option value="light">Light</option>
          <option value="moderate">Moderate</option>
          <option value="active">Active</option>
          <option value="very_active">Very active</option>
        </select>
      </div>
      <div className="input-group">
        <label>Dietary preferences (comma-separated)</label>
        <input type="text" placeholder="e.g. vegetarian, low-carb" {...register('dietary_preferences_str')} />
      </div>
      <div className="input-group">
        <label>Allergies (comma-separated)</label>
        <input type="text" placeholder="e.g. nuts, shellfish" {...register('allergies_str')} />
      </div>
      <div className="input-group">
        <label>Cultural preferences (comma-separated)</label>
        <input type="text" placeholder="e.g. Indian, Mediterranean" {...register('cultural_preferences_str')} />
      </div>
      <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
        {isSubmitting ? 'Saving…' : 'Save profile'}
      </button>
    </form>
  )
}

function GoalsForm({
  user,
  onSubmit,
  isSubmitting,
}: {
  user: UserResponse
  onSubmit: (d: GoalsUpdate) => void
  isSubmitting: boolean
}) {
  const { register, handleSubmit } = useForm<GoalsUpdate>({
    defaultValues: {
      daily_calorie_target: user.daily_calorie_target ?? undefined,
      protein_target_g: user.protein_target_g ?? undefined,
      carb_target_g: user.carb_target_g ?? undefined,
      fat_target_g: user.fat_target_g ?? undefined,
    },
  })

  const onGoalsSubmit = (data: GoalsUpdate) => {
    const clean: GoalsUpdate = {}
    if (data.daily_calorie_target != null && !Number.isNaN(data.daily_calorie_target)) clean.daily_calorie_target = data.daily_calorie_target
    if (data.protein_target_g != null && !Number.isNaN(data.protein_target_g)) clean.protein_target_g = data.protein_target_g
    if (data.carb_target_g != null && !Number.isNaN(data.carb_target_g)) clean.carb_target_g = data.carb_target_g
    if (data.fat_target_g != null && !Number.isNaN(data.fat_target_g)) clean.fat_target_g = data.fat_target_g
    onSubmit(clean)
  }

  return (
    <form onSubmit={handleSubmit(onGoalsSubmit)}>
      <div className="input-group">
        <label>Daily calorie target</label>
        <input type="number" min={0} {...register('daily_calorie_target', { valueAsNumber: true })} />
      </div>
      <div className="input-group">
        <label>Protein target (g)</label>
        <input type="number" min={0} step={0.1} {...register('protein_target_g', { valueAsNumber: true })} />
      </div>
      <div className="input-group">
        <label>Carb target (g)</label>
        <input type="number" min={0} step={0.1} {...register('carb_target_g', { valueAsNumber: true })} />
      </div>
      <div className="input-group">
        <label>Fat target (g)</label>
        <input type="number" min={0} step={0.1} {...register('fat_target_g', { valueAsNumber: true })} />
      </div>
      <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
        {isSubmitting ? 'Saving…' : 'Save goals'}
      </button>
    </form>
  )
}
