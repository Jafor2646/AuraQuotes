'use client'

import { useState, useRef, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useChat } from '../../hooks'

export default function ChatInterface() {
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const router = useRouter()
  
  const {
    messages,
    sessionId,
    isLoading,
    error,
    sendMessage,
    clearChat
  } = useChat()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setInput(value)
  }

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return

    const messageContent = input.trim()
    setInput('')
    
    await sendMessage(messageContent)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleQuickMessage = (message: string) => {
    setInput(message)
    inputRef.current?.focus()
  }

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg overflow-hidden border">
        {/* Chat Header */}
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-lg font-semibold">AI Quote Assistant</h3>
              <p className="text-sm text-blue-100">
                Tell me how you're feeling, and I'll find the perfect quotes for you!
              </p>
            </div>
            {messages.length > 0 && (
              <button
                onClick={clearChat}
                className="bg-white/20 hover:bg-white/30 px-3 py-1 rounded-lg text-sm transition-colors"
              >
                Clear Chat
              </button>
            )}
          </div>
        </div>

        {/* Messages Container */}
        <div className="chat-container p-4 h-96 overflow-y-auto bg-gray-50">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 mt-8">
              <div className="text-4xl mb-4">🤖</div>
              <p className="text-lg mb-2">Welcome! I'm your AI quote assistant.</p>
              <p className="text-sm">Start by telling me how you're feeling or what kind of quotes you need.</p>
              <div className="mt-4 flex flex-wrap justify-center gap-2">
                <button
                  onClick={() => handleQuickMessage("I need some motivation for work")}
                  className="bg-blue-100 hover:bg-blue-200 text-blue-800 px-3 py-1 rounded-full text-sm transition-colors"
                >
                  Need motivation
                </button>
                <button
                  onClick={() => handleQuickMessage("I'm feeling romantic today")}
                  className="bg-pink-100 hover:bg-pink-200 text-pink-800 px-3 py-1 rounded-full text-sm transition-colors"
                >
                  Feeling romantic
                </button>
                <button
                  onClick={() => handleQuickMessage("I want something funny to cheer me up")}
                  className="bg-yellow-100 hover:bg-yellow-200 text-yellow-800 px-3 py-1 rounded-full text-sm transition-colors"
                >
                  Need humor
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-xl ${
                      message.role === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-white text-gray-800 shadow-sm border'
                    }`}
                  >
                    <p className="text-sm">{message.content}</p>
                    <p className={`text-xs mt-1 ${
                      message.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                    }`}>
                      {formatTime(message.timestamp)}
                    </p>
                    
                    {/* Show tool calls info */}
                    {message.tool_calls && (
                      <div className="mt-2 text-xs opacity-75">
                        {message.tool_calls.intent_detection && (
                          <div className="mb-1">
                            🎯 Detected mood: <span className="font-medium">
                              {message.tool_calls.intent_detection.intent}
                            </span>
                            {message.tool_calls.intent_detection.ai_model && (
                              <span className="ml-1 opacity-60">
                                ({message.tool_calls.intent_detection.ai_model})
                              </span>
                            )}
                          </div>
                        )}
                        {message.tool_calls.navigation && (
                          <div className="flex items-center justify-between">
                            <div>
                              🧭 Suggested page: <span className="font-medium">
                                {message.tool_calls.navigation.category}
                              </span>
                            </div>
                            <button
                              onClick={() => router.push(`/quotes/${message.tool_calls.navigation.category}`)}
                              className="ml-2 bg-blue-500 hover:bg-blue-600 text-white text-xs px-2 py-1 rounded transition-colors"
                            >
                              Go to {message.tool_calls.navigation.category}
                            </button>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-white text-gray-800 shadow-sm border max-w-xs lg:max-w-md px-4 py-2 rounded-xl">
                    <div className="flex items-center space-x-2">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      </div>
                      <span className="text-sm text-gray-500">AI is thinking...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Error Display */}
        {error && (
          <div className="px-4 py-2 bg-red-50 border-t border-red-200">
            <p className="text-sm text-red-600">❌ {error}</p>
          </div>
        )}

        {/* Input Area */}
        <div className="border-t p-4 bg-white">
          <div className="flex space-x-3">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              placeholder="Tell me how you're feeling or what you need..."
              className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-black"
              disabled={isLoading}
              autoComplete="off"
              style={{ color: 'black', backgroundColor: 'white' }}
            />
            <button
              onClick={handleSendMessage}
              disabled={!input.trim() || isLoading}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white px-6 py-2 rounded-lg transition-colors"
            >
              {isLoading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              ) : (
                'Send'
              )}
            </button>
          </div>
          <div className="flex justify-between items-center mt-2">
            <p className="text-xs text-gray-500">
              Session ID: {sessionId ? sessionId.slice(0, 8) + '...' : 'Not started'}
            </p>
            <p className="text-xs text-gray-500">
              AI System: Local LLM with Agentic Workflow
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
