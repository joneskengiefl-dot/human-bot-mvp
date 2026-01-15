import type { Session } from '../types'
import { formatDistanceToNow } from 'date-fns'
import './SessionList.css'

interface SessionListProps {
  sessions: Session[]
}

export default function SessionList({ sessions }: SessionListProps) {
  return (
    <div className="session-list">
      <h2 className="section-title">Active Sessions</h2>
      {sessions.length === 0 ? (
        <div className="empty-state">
          <p>No active sessions</p>
        </div>
      ) : (
        <div className="session-items">
          {sessions.map((session) => (
            <div key={session.session_id} className="session-item">
              <div className="session-header">
                <span className="session-id">{session.session_id.substring(0, 8)}...</span>
                <span className="session-time">
                  {formatDistanceToNow(new Date(session.start_time), { addSuffix: true })}
                </span>
              </div>
              <div className="session-details">
                <div className="session-detail">
                  <span className="detail-label">Device:</span>
                  <span className="detail-value">{session.device}</span>
                </div>
                <div className="session-detail">
                  <span className="detail-label">URL:</span>
                  <span className="detail-value url">{session.target_url}</span>
                </div>
                {session.proxy && (
                  <div className="session-detail">
                    <span className="detail-label">Proxy:</span>
                    <span className="detail-value proxy">{session.proxy}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
