import type { Stats } from '../types'
import './StatsCards.css'

interface StatsCardsProps {
  stats: Stats | null
}

export default function StatsCards({ stats }: StatsCardsProps) {
  if (!stats) {
    return (
      <div className="stats-cards">
        <div className="stat-card empty">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <div className="stat-value">-</div>
            <div className="stat-label">No data available</div>
            <div className="stat-hint">Start the API server to see statistics</div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="stats-cards">
      <div className="stat-card">
        <div className="stat-icon">📊</div>
        <div className="stat-content">
          <div className="stat-value">{stats.total_sessions}</div>
          <div className="stat-label">Total Sessions</div>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon">🟢</div>
        <div className="stat-content">
          <div className="stat-value">{stats.active_sessions}</div>
          <div className="stat-label">Active Sessions</div>
        </div>
      </div>

      <div className="stat-card success">
        <div className="stat-icon">✅</div>
        <div className="stat-content">
          <div className="stat-value">{stats.successful_sessions}</div>
          <div className="stat-label">Successful</div>
        </div>
      </div>

      <div className="stat-card error">
        <div className="stat-icon">❌</div>
        <div className="stat-content">
          <div className="stat-value">{stats.failed_sessions}</div>
          <div className="stat-label">Failed</div>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon">🖱️</div>
        <div className="stat-content">
          <div className="stat-value">{stats.total_clicks}</div>
          <div className="stat-label">Total Clicks</div>
        </div>
      </div>
    </div>
  )
}
