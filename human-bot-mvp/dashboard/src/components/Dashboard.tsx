import { useState, useEffect } from 'react'
import { apiClient, wsService } from '../services'
import type { Stats, Session, BotEvent } from '../types'
import StatsCards from './StatsCards'
import SessionList from './SessionList'
import IPStatus from './IPStatus'
import ActivityChart from './ActivityChart'
import './Dashboard.css'

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [sessions, setSessions] = useState<Session[]>([])
  const [events, setEvents] = useState<BotEvent[]>([])
  const [loading, setLoading] = useState(true)
  const [connected, setConnected] = useState(false)
  const [apiConnected, setApiConnected] = useState(false)

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 5000) // Refresh every 5 seconds
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    // Subscribe to WebSocket events
    const unsubscribe = wsService.subscribe((event) => {
      setEvents((prev) => [...prev.slice(-99), event]) // Keep last 100 events
      loadData() // Refresh data on new event
    })

    // Check connection status
    const statusInterval = setInterval(() => {
      setConnected(wsService.isConnected())
    }, 1000)

    return () => {
      unsubscribe()
      clearInterval(statusInterval)
    }
  }, [])

  async function loadData() {
    try {
      // Check API health first
      try {
        await apiClient.healthCheck()
        setApiConnected(true)
      } catch (error) {
        setApiConnected(false)
        setLoading(false)
        return
      }

      const [statsData, sessionsData, eventsData] = await Promise.all([
        apiClient.getStats(),
        apiClient.getSessions(),
        apiClient.getEvents(200) // Get last 200 events for chart
      ])
      setStats(statsData)
      setSessions(sessionsData)
      // Combine historical events with WebSocket events (WebSocket events take precedence for real-time)
      setEvents((prev) => {
        const wsEventIds = new Set(prev.map(e => `${e.type}-${e.timestamp}`))
        const historical = eventsData.filter((e: BotEvent) => 
          !wsEventIds.has(`${e.type}-${e.timestamp}`)
        )
        return [...historical, ...prev].slice(-100) // Keep last 100 total
      })
      setLoading(false)
      setApiConnected(true)
    } catch (error) {
      console.error('Error loading data:', error)
      // Set default values if API is not available
      setStats(null)
      setSessions([])
      setLoading(false)
      setApiConnected(false)
    }
  }


  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    )
  }

  return (
    <div className="dashboard">
      <div className="dashboard-status">
        <div className={`status-indicator ${apiConnected ? 'connected' : 'disconnected'}`}>
          <span className="status-dot"></span>
          {apiConnected ? 'API Connected' : 'API Disconnected'}
        </div>
        <div className={`status-indicator ${connected ? 'connected' : 'disconnected'}`}>
          <span className="status-dot"></span>
          {connected ? 'WebSocket Connected' : 'WebSocket Disconnected'}
        </div>
        {!apiConnected && (
          <div className="api-warning">
            <p>⚠️ API server not running. Please start it with:</p>
            <code>cd human-bot-mvp\bot-engine && .\run-api.bat</code>
          </div>
        )}
      </div>

      <div className="dashboard-content">
        <div className="dashboard-section">
          <StatsCards stats={stats} />
        </div>

        <div className="dashboard-section">
          <ActivityChart events={events} />
        </div>

        <div className="dashboard-grid">
          <div className="dashboard-section">
            <SessionList sessions={sessions} />
          </div>

          <div className="dashboard-section">
            <IPStatus stats={stats} />
          </div>
        </div>
      </div>
    </div>
  )
}
