import type { UseFormRegister } from 'react-hook-form'

export type MealLogFormFields = { text: string; meal_type: string }

export default function MealInput({
  register,
  disabled,
  error,
}: {
  register: UseFormRegister<MealLogFormFields>
  disabled?: boolean
  error?: string
}) {
  return (
    <div className="input-group">
      <label>What did you eat? (e.g. &quot;2 eggs, toast with butter, orange juice&quot;)</label>
      <textarea
        placeholder="Describe your meal in plain text..."
        disabled={disabled}
        {...register('text', { required: 'Describe your meal' })}
      />
      {error && <p className="error-msg">{error}</p>}
    </div>
  )
}
