import type { BotEvent } from '../types'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import './ActivityChart.css'

interface ActivityChartProps {
  events: BotEvent[]
}

export default function ActivityChart({ events }: ActivityChartProps) {
  const chartData = processEventsForChart(events)

  return (
    <div className="activity-chart">
      <h2 className="section-title">Session Activity</h2>
      {chartData.length === 0 ? (
        <div className="empty-state">
          <p>No data available</p>
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" />
            <XAxis
              dataKey="time"
              stroke="#94a3b8"
              tick={{ fill: '#94a3b8', fontSize: 12 }}
            />
            <YAxis
              stroke="#94a3b8"
              tick={{ fill: '#94a3b8', fontSize: 12 }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                border: '1px solid rgba(148, 163, 184, 0.2)',
                borderRadius: '0.5rem',
                color: '#f1f5f9'
              }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="sessions"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={{ fill: '#3b82f6', r: 4 }}
              name="Sessions"
            />
            <Line
              type="monotone"
              dataKey="clicks"
              stroke="#10b981"
              strokeWidth={2}
              dot={{ fill: '#10b981', r: 4 }}
              name="Clicks"
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}

function processEventsForChart(events: BotEvent[]) {
  const timeMap = new Map<string, { sessions: number; clicks: number }>()

  events.forEach((event) => {
    const date = new Date(event.timestamp)
    const minute = `${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
    
    if (!timeMap.has(minute)) {
      timeMap.set(minute, { sessions: 0, clicks: 0 })
    }

    const data = timeMap.get(minute)!
    if (event.type === 'session_start') {
      data.sessions++
    } else if (event.type === 'click') {
      data.clicks++
    }
  })

  return Array.from(timeMap.entries())
    .map(([time, data]) => ({ time, ...data }))
    .sort((a, b) => a.time.localeCompare(b.time))
    .slice(-20)
}
