/**
 * API Client - TypeScript client for Python Bot Engine API
 */

import axios from 'axios'
import type { Session, Stats } from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiClient {
  private baseURL: string

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  async healthCheck(): Promise<{ status: string; timestamp: string; active_sessions: number }> {
    try {
      const response = await axios.get(`${this.baseURL}/api/health`, { timeout: 5000 })
      return response.data
    } catch (error) {
      console.warn('API health check failed:', error)
      throw error
    }
  }

  async getSessions(): Promise<Session[]> {
    try {
      const response = await axios.get(`${this.baseURL}/api/sessions`, { timeout: 5000 })
      return response.data
    } catch (error) {
      console.warn('Failed to fetch sessions:', error)
      return [] // Return empty array on error
    }
  }

  async getStats(): Promise<Stats | null> {
    try {
      const response = await axios.get(`${this.baseURL}/api/stats`, { timeout: 5000 })
      return response.data
    } catch (error) {
      console.warn('Failed to fetch stats:', error)
      return null // Return null on error
    }
  }

  async getIPStatus(): Promise<{ proxies: any[]; health: any }> {
    const response = await axios.get(`${this.baseURL}/api/ip/status`)
    return response.data
  }

  async getEvents(limit: number = 200, eventType?: string): Promise<any[]> {
    try {
      const params = new URLSearchParams()
      params.append('limit', limit.toString())
      if (eventType) {
        params.append('event_type', eventType)
      }
      const response = await axios.get(`${this.baseURL}/api/events?${params.toString()}`, { timeout: 5000 })
      return response.data
    } catch (error) {
      console.warn('Failed to fetch events:', error)
      return []
    }
  }
}

export const apiClient = new ApiClient()
