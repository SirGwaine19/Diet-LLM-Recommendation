import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useAuthStore } from '../store/authStore'
import { authService } from '../services/authService'
import type { LoginPayload } from '../services/authService'
import { networkErrorMessage } from '../utils/apiErrors'

export default function Login() {
  const navigate = useNavigate()
  const setToken = useAuthStore((s) => s.setToken)
  const [error, setError] = useState<string | null>(null)

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginPayload>()

  const onSubmit = async (data: LoginPayload) => {
    setError(null)
    try {
      const res = await authService.login(data)
      setToken(res.data.access_token)
      navigate('/dashboard')
    } catch (e: unknown) {
      const err = e as {
        response?: { data?: { detail?: string | Array<{ msg?: string }>; message?: string } }
        message?: string
      }
      const detail = err.response?.data?.detail
      let msg: string
      if (!err.response) {
        msg = networkErrorMessage()
      } else if (typeof detail === 'string') {
        msg = detail
      } else if (Array.isArray(detail) && detail.length > 0) {
        msg = detail.map((x) => x.msg || JSON.stringify(x)).join('. ')
      } else {
        msg = err.response?.data?.message || 'Login failed'
      }
      setError(msg)
    }
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundImage: 'url(/login-bg.jpg)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div
        style={{
          maxWidth: 400,
          width: '100%',
          padding: '2rem',
          background: 'rgba(30, 30, 30, 0.9)',
          borderRadius: 'var(--radius)',
        }}
      >
        <h1 className="page-title" style={{ textAlign: 'center' }}>Log in</h1>
        <div className="card" style={{ background: 'transparent', boxShadow: 'none' }}>
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
              <label>Password</label>
              <input
                type="password"
                autoComplete="current-password"
                {...register('password', { required: 'Password is required' })}
              />
              {errors.password && <p className="error-msg">{errors.password.message}</p>}
            </div>
            {error && <p className="error-msg">{error}</p>}
            <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
              {isSubmitting ? 'Logging in…' : 'Log in'}
            </button>
          </form>
        </div>
        <p style={{ marginTop: '1rem', color: 'var(--text-muted)', textAlign: 'center' }}>
          Don't have an account? <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
  )
}
