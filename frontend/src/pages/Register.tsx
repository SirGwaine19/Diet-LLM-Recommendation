import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useAuthStore } from '../store/authStore'
import { authService } from '../services/authService'
import type { RegisterPayload } from '../services/authService'

export default function Register() {
  const navigate = useNavigate()
  const setToken = useAuthStore((s) => s.setToken)
  const [error, setError] = useState<string | null>(null)

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<RegisterPayload>()

  const onSubmit = async (data: RegisterPayload) => {
    setError(null)
    try {
      const res = await authService.register(data)
      setToken(res.data.access_token)
      navigate('/dashboard')
    } catch (e: unknown) {
      const err = e as {
        response?: { data?: { detail?: string | Array<{ msg?: string }>; message?: string }; status?: number }
        message?: string
      }
      const detail = err.response?.data?.detail
      let msg: string
      if (!err.response) {
        msg = 'Cannot reach server. Is the backend running at http://localhost:8000?'
      } else if (typeof detail === 'string') {
        msg = detail
      } else if (Array.isArray(detail) && detail.length > 0) {
        msg = detail.map((x) => x.msg || JSON.stringify(x)).join('. ')
      } else {
        msg = err.response?.data?.message || `Registration failed (${err.response?.status ?? 'error'})`
      }
      setError(msg)
    }
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundImage: 'url(/app-bg.png)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundAttachment: 'fixed',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div style={{ maxWidth: 400, width: '100%', padding: '2rem' }}>
        <h1 className="page-title" style={{ textAlign: 'center' }}>Create account</h1>
        <div className="card">
          <form onSubmit={handleSubmit(onSubmit)}>
          <div className="input-group">
            <label>Email</label>
            <input
              type="email"
              autoComplete="email"
              {...register('email', { required: 'Email is required' })}
            />
            {errors.email && <p className="error-msg">{errors.email.message}</p>}
          </div>
          <div className="input-group">
            <label>Full name (optional)</label>
            <input type="text" autoComplete="name" {...register('full_name')} />
          </div>
          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              autoComplete="new-password"
              {...register('password', { required: 'Password is required', minLength: { value: 4, message: 'At least 4 characters' } })}
            />
            {errors.password && <p className="error-msg">{errors.password.message}</p>}
          </div>
          {error && <p className="error-msg">{error}</p>}
          <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
            {isSubmitting ? 'Creating account…' : 'Register'}
          </button>
        </form>
      </div>
        <p style={{ marginTop: '1rem', color: 'var(--text-muted)', textAlign: 'center' }}>
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </div>
    </div>
  )
}
