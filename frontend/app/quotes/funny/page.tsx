'use client'

import { useState } from 'react'
import Navbar from '../../components/Navbar'
import QuoteCard from '../../components/QuoteCard'
import QuoteModal from '../../components/QuoteModal'
import Link from 'next/link'
import { useQuotes } from '../../../hooks'

interface Quote {
  id: number
  quote: string
  author: string
  category: string
}

export default function FunnyQuotes() {
  const { quotes, loading, error } = useQuotes('funny')
  const [selectedQuote, setSelectedQuote] = useState<Quote | null>(null)

  const handleQuoteClick = (quote: Quote) => {
    setSelectedQuote(quote)
  }

  const closeModal = () => {
    setSelectedQuote(null)
  }

  return (
    <div className="min-h-screen">
      <Navbar />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-yellow-400 to-orange-500 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="text-6xl mb-6">😂</div>
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              Funny Quotes
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-yellow-100 max-w-3xl mx-auto">
              Brighten your day with these hilarious and witty quotes. 
              Laughter is the best medicine, so let's spread some joy and humor!
            </p>
            <Link 
              href="/"
              className="inline-flex items-center bg-white text-orange-600 hover:bg-yellow-50 font-semibold px-6 py-3 rounded-full transition-all duration-300"
            >
              ← Back to Chat
            </Link>
          </div>
        </div>
      </section>

      {/* Quotes Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {loading ? (
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-500 mx-auto"></div>
              <p className="mt-4 text-gray-600">Loading funny quotes...</p>
            </div>
          ) : quotes.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {quotes.map((quote) => (
                <QuoteCard 
                  key={quote.id} 
                  quote={quote} 
                  onClick={() => handleQuoteClick(quote)}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="text-4xl mb-4">😕</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No quotes found</h3>
              <p className="text-gray-600 mb-6">
                We couldn't load the funny quotes. Check your internet connection.
              </p>
              <button 
                onClick={() => window.location.reload()}
                className="bg-yellow-500 hover:bg-yellow-600 text-white px-6 py-3 rounded-lg transition-colors"
              >
                Try Again
              </button>
            </div>
          )}
        </div>
      </section>

      {/* Quote Modal */}
      <QuoteModal 
        quote={selectedQuote}
        isOpen={!!selectedQuote}
        onClose={closeModal}
      />
    </div>
  )
}
