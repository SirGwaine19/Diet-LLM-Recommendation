import { Outlet } from 'react-router-dom'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'

export default function Layout() {
  const logout = useAuthStore((s) => s.logout)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundImage: 'url(/app-bg.png)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundAttachment: 'fixed',
      }}
    >
      <div className="app">
        <nav
          className="nav"
          style={{
            background: 'rgba(26, 35, 50, 0.95)',
            borderRadius: 'var(--radius)',
            padding: '0.75rem 1rem',
          }}
        >
          <Link to="/dashboard">Diet Recommendation</Link>
          <div className="nav-links">
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/log-meal">Log Meal</Link>
            <Link to="/meal-history">Meal History</Link>
            <Link to="/profile">Profile</Link>
            <button type="button" className="btn btn-secondary" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </nav>
        <Outlet />
      </div>
    </div>
  )
}
