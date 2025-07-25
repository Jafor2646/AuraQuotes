// Custom hooks for the application
'use client'

import { useState, useEffect } from 'react'
import { apiService, Quote, Category, ChatMessage, ChatResponse } from '../lib/api'

// Hook for managing quotes
export function useQuotes(category?: string) {
  const [quotes, setQuotes] = useState<Quote[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchQuotes = async () => {
    try {
      setLoading(true)
      setError(null)
      
      let data
      if (category) {
        data = await apiService.getQuotesByCategory(category)
        setQuotes(data.quotes)
      } else {
        data = await apiService.getAllQuotes()
        setQuotes(data.quotes)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch quotes')
      console.error('Error fetching quotes:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchQuotes()
  }, [category])

  return { quotes, loading, error, refetch: fetchQuotes }
}

// Hook for managing categories
export function useCategories() {
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true)
        setError(null)
        const data = await apiService.getCategories()
        setCategories(data.categories)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch categories')
        console.error('Error fetching categories:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchCategories()
  }, [])

  return { categories, loading, error }
}

// Hook for managing chat
export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [sessionId, setSessionId] = useState<string>('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Load chat history from localStorage on mount
  useEffect(() => {
    const savedSessionId = localStorage.getItem('aura-chat-session-id')
    const savedMessages = localStorage.getItem('aura-chat-messages')
    
    if (savedSessionId) {
      setSessionId(savedSessionId)
    }
    
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages))
      } catch (error) {
        console.error('Error parsing saved messages:', error)
      }
    }
  }, [])

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('aura-chat-messages', JSON.stringify(messages))
    }
  }, [messages])

  // Save session ID to localStorage whenever it changes
  useEffect(() => {
    if (sessionId) {
      localStorage.setItem('aura-chat-session-id', sessionId)
    }
  }, [sessionId])

  const sendMessage = async (messageContent: string) => {
    if (!messageContent.trim() || isLoading) return

    setIsLoading(true)
    setError(null)

    // Add user message to chat
    const userMessage: ChatMessage = {
      role: 'user',
      content: messageContent,
      timestamp: new Date().toISOString()
    }
    
    setMessages(prev => [...prev, userMessage])

    try {
      const response: ChatResponse = await apiService.sendChatMessage(messageContent, sessionId)

      // Update session ID if new
      if (response.session_id && response.session_id !== sessionId) {
        setSessionId(response.session_id)
      }

      // Add assistant response to chat
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.response,
        tool_calls: response.tool_calls,
        timestamp: new Date().toISOString()
      }
      
      setMessages(prev => [...prev, assistantMessage])

      return response

    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to send message'
      setError(errorMsg)
      
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please make sure the backend server is running on http://localhost:8000',
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const clearChat = () => {
    setMessages([])
    setSessionId('')
    setError(null)
    localStorage.removeItem('aura-chat-messages')
    localStorage.removeItem('aura-chat-session-id')
  }

  return {
    messages,
    sessionId,
    isLoading,
    error,
    sendMessage,
    clearChat
  }
}

// Hook for local storage management
export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(initialValue)

  useEffect(() => {
    try {
      const item = window.localStorage.getItem(key)
      if (item) {
        setStoredValue(JSON.parse(item))
      }
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error)
    }
  }, [key])

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error)
    }
  }

  return [storedValue, setValue] as const
}
