import NutritionBreakdown from '../meals/NutritionBreakdown'

interface Props {
  calories: number
  protein_g: number
  carbs_g: number
  fat_g: number
  calorieTarget?: number
  proteinTarget?: number
  carbTarget?: number
  fatTarget?: number
}

export default function NutritionProgress({
  calories,
  protein_g,
  carbs_g,
  fat_g,
  calorieTarget,
  proteinTarget,
  carbTarget,
  fatTarget,
}: Props) {
  return (
    <div>
      <h2 style={{ marginTop: 0, marginBottom: '1rem' }}>Today&apos;s nutrition</h2>
      <NutritionBreakdown
        calories={calories}
        protein_g={protein_g}
        carbs_g={carbs_g}
        fat_g={fat_g}
        calorieTarget={calorieTarget}
        proteinTarget={proteinTarget}
        carbTarget={carbTarget}
        fatTarget={fatTarget}
      />
    </div>
  )
}
