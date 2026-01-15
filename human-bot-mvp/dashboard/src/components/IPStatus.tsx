import type { Stats } from '../types'
import './IPStatus.css'

interface IPStatusProps {
  stats: Stats | null
}

export default function IPStatus({ stats }: IPStatusProps) {
  if (!stats) return null

  const { ip_health, proxy_stats } = stats

  return (
    <div className="ip-status">
      <h2 className="section-title">IP Status</h2>
      
      <div className="ip-health-summary">
        <div className="health-item healthy">
          <span className="health-label">Healthy:</span>
          <span className="health-value">{ip_health.healthy}</span>
        </div>
        <div className="health-item flagged">
          <span className="health-label">Flagged:</span>
          <span className="health-value">{ip_health.flagged}</span>
        </div>
        <div className="health-item blacklisted">
          <span className="health-label">Blacklisted:</span>
          <span className="health-value">{ip_health.blacklisted}</span>
        </div>
      </div>

      {proxy_stats.length === 0 ? (
        <div className="empty-state">
          <p>No proxies configured</p>
        </div>
      ) : (
        <div className="proxy-list">
          {proxy_stats.map((proxy) => (
            <div key={proxy.url} className={`proxy-item ${proxy.status}`}>
              <div className="proxy-header">
                <span className="proxy-url">{proxy.url}</span>
                <span className={`proxy-status ${proxy.enabled ? 'active' : 'inactive'}`}>
                  {proxy.enabled ? '●' : '○'}
                </span>
              </div>
              <div className="proxy-metrics">
                <div className="metric">
                  <span className="metric-label">Uses:</span>
                  <span className="metric-value">{proxy.uses}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Success Rate:</span>
                  <span className="metric-value">
                    {(proxy.success_rate * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
