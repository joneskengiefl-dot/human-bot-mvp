/**
 * TypeScript Types for Dashboard
 */

export interface Session {
  session_id: string
  device: string
  start_time: string
  target_url: string
  proxy?: string
}

export interface Stats {
  total_sessions: number
  active_sessions: number
  successful_sessions: number
  failed_sessions: number
  total_clicks: number
  average_duration: number
  success_rate: number
  proxy_stats: ProxyStat[]
  ip_health: {
    healthy: number
    flagged: number
    blacklisted: number
  }
}

export interface ProxyStat {
  url: string
  uses: number
  successes: number
  failures: number
  success_rate: number
  status: 'healthy' | 'flagged' | 'blacklisted'
  enabled: boolean
  last_used?: string
}

export interface BotEvent {
  type: string
  timestamp: string
  data: Record<string, any>
}

// MVP: RunSessionRequest removed - dashboard is monitor-only
// Future: Execution control will be implemented in intelligence layer
