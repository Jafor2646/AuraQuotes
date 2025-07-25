// API service for backend communication
const API_BASE_URL = 'http://localhost:8000'

export interface Quote {
  id: number
  quote: string
  author: string
  category: string
  created_at?: string
}

export interface Category {
  name: string
  emoji: string
  description: string
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  tool_calls?: any
  timestamp: string
}

export interface ChatResponse {
  response: string
  session_id: string
  tool_calls?: any
}

class APIService {
  private baseURL: string

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  // Chat endpoints
  async sendChatMessage(message: string, sessionId?: string): Promise<ChatResponse> {
    const response = await fetch(`${this.baseURL}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        session_id: sessionId || undefined
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  async getChatHistory(sessionId: string): Promise<{ session_id: string; messages: ChatMessage[] }> {
    const response = await fetch(`${this.baseURL}/chat/history/${sessionId}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  // Quote endpoints
  async getQuotesByCategory(category: string, limit: number = 15): Promise<{ category: string; quotes: Quote[] }> {
    const response = await fetch(`${this.baseURL}/quotes/${category}?limit=${limit}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  async getAllQuotes(limit: number = 100): Promise<{ quotes: Quote[] }> {
    const response = await fetch(`${this.baseURL}/quotes/?limit=${limit}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  async getCategories(): Promise<{ categories: Category[] }> {
    const response = await fetch(`${this.baseURL}/quotes/categories/`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  async createQuote(category: string, quote: string, author: string): Promise<any> {
    const response = await fetch(`${this.baseURL}/quotes/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        category,
        quote,
        author
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  // Health check
  async healthCheck(): Promise<{ status: string; service: string }> {
    const response = await fetch(`${this.baseURL}/health`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }
}

// Export singleton instance
export const apiService = new APIService()
export default apiService
