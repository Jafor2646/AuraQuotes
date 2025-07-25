'use client'

import Navbar from './components/Navbar'
import ChatInterface from './components/ChatInterface'
import CategoryGrid from './components/CategoryGrid'
import QuotesGrid from './components/QuotesGrid'

export default function Home() {
  return (
    <div className="min-h-screen">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 text-white">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Welcome to <span className="text-yellow-400">AuraQuotes</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100 max-w-3xl mx-auto">
              Discover the perfect quote for your mood with our AI-powered chatbot. 
              Let artificial intelligence guide you to inspiration, motivation, and wisdom.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                className="bg-yellow-400 hover:bg-yellow-300 text-blue-900 font-semibold px-8 py-3 rounded-full transition-all duration-300 transform hover:scale-105"
                onClick={() => document.getElementById('chat-section')?.scrollIntoView({ behavior: 'smooth' })}
              >
                Start Chatting 🤖
              </button>
              <button 
                className="border-2 border-white hover:bg-white hover:text-blue-900 text-white font-semibold px-8 py-3 rounded-full transition-all duration-300"
                onClick={() => document.getElementById('categories-section')?.scrollIntoView({ behavior: 'smooth' })}
              >
                Browse Quotes
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Chat Section */}
      <section id="chat-section" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Chat with Our AI Assistant
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Tell our AI how you're feeling, and it will guide you to the perfect quotes. 
              The chatbot uses a lightweight local LLM with agentic workflow for intelligent mood detection and quote recommendations.
            </p>
          </div>
          <ChatInterface />
        </div>
      </section>

      {/* Categories Section */}
      <section id="categories-section" className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Explore Quote Categories
            </h2>
            <p className="text-lg text-gray-600">
              Browse our carefully curated collection of quotes by category
            </p>
          </div>
          <CategoryGrid />
        </div>
      </section>

      {/* Featured Quotes Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Featured Quotes
            </h2>
            <p className="text-lg text-gray-600">
              Some of our most inspiring and popular quotes
            </p>
          </div>
          <QuotesGrid limit={6} />
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold mb-2">AuraQuotes</h3>
            <p className="text-gray-400">
              AI-powered inspirational quotes for every mood
            </p>
            <p className="text-sm text-gray-500 mt-4">
              Built for KaizenAI Full Stack Engineer Internship Challenge
            </p>
            <div className="mt-4 text-xs text-gray-500">
              🤖 AI System: Local LLM with External Tool Calling (Agentic Workflow)
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
