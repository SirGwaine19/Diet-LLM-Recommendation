interface Props {
  calories: number | null
  protein_g: number | null
  carbs_g: number | null
  fat_g: number | null
  calorieTarget?: number | null
  proteinTarget?: number | null
  carbTarget?: number | null
  fatTarget?: number | null
}

export default function NutritionBreakdown({
  calories,
  protein_g,
  carbs_g,
  fat_g,
  calorieTarget,
  proteinTarget,
  carbTarget,
  fatTarget,
}: Props) {
  const hasTargets = calorieTarget != null || proteinTarget != null || carbTarget != null || fatTarget != null

  const bar = (value: number | null, target: number | null | undefined, key: string) => {
    if (value == null) return null
    const pct = target && target > 0 ? Math.min(100, (value / target) * 100) : null
    return (
      <div key={key} className="input-group" style={{ marginBottom: '0.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem' }}>
          <span style={{ textTransform: 'capitalize' }}>{key}</span>
          <span>{value.toFixed(0)} {target != null ? `/ ${target}` : ''}</span>
        </div>
        {pct != null && (
          <div className="progress-bar">
            <div
              className={`progress-bar-fill ${key}`}
              style={{ width: `${Math.min(100, pct)}%` }}
            />
          </div>
        )}
      </div>
    )
  }

  return (
    <div>
      <h3 style={{ marginBottom: '0.75rem', fontSize: '1rem' }}>Nutrition</h3>
      {bar(calories, calorieTarget, 'calories')}
      {bar(protein_g, proteinTarget, 'protein')}
      {bar(carbs_g, carbTarget, 'carbs')}
      {bar(fat_g, fatTarget, 'fat')}
      {!hasTargets && calories == null && protein_g == null && carbs_g == null && fat_g == null && (
        <p style={{ color: 'var(--text-muted)', margin: 0 }}>No nutrition data for this meal.</p>
      )}
    </div>
  )
}
