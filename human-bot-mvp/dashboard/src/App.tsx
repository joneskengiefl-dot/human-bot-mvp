import { useEffect } from 'react'
import Dashboard from './components/Dashboard'
import { wsService } from './services/websocket'
import './App.css'

function App() {
  useEffect(() => {
    // Connect WebSocket after a short delay to allow page to load first
    const connectTimeout = setTimeout(() => {
      wsService.connect()
    }, 500)
    
    return () => {
      clearTimeout(connectTimeout)
      // Disconnect on unmount
      wsService.disconnect()
    }
  }, [])

  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 Human B.O.T Dashboard</h1>
        <p>Real-time Bot Engine Monitoring</p>
      </header>
      <Dashboard />
    </div>
  )
}

export default App
