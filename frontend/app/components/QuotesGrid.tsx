'use client'

import { useState } from 'react'
import { useQuotes } from '../../hooks'
import QuoteCard from './QuoteCard'
import QuoteModal from './QuoteModal'

interface Quote {
  id: number
  quote: string
  author: string
  category: string
}

interface QuotesGridProps {
  category?: string
  limit?: number
}

export default function QuotesGrid({ category, limit }: QuotesGridProps) {
  const {
    quotes,
    loading,
    error,
    refetch
  } = useQuotes(category)

  const [selectedQuote, setSelectedQuote] = useState<Quote | null>(null)

  const handleQuoteClick = (quote: Quote) => {
    setSelectedQuote(quote)
  }

  const closeModal = () => {
    setSelectedQuote(null)
  }

  const displayedQuotes = limit ? quotes.slice(0, limit) : quotes

  if (loading && quotes.length === 0) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="bg-white rounded-xl p-6 shadow-lg animate-pulse">
            <div className="h-4 bg-gray-200 rounded mb-4"></div>
            <div className="h-4 bg-gray-200 rounded mb-4 w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-500 text-lg mb-4">❌ {error}</div>
        <button
          onClick={refetch}
          className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors"
        >
          Try Again
        </button>
      </div>
    )
  }

  if (displayedQuotes.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📭</div>
        <h3 className="text-xl font-semibold text-gray-700 mb-2">No quotes found</h3>
        <p className="text-gray-500 mb-4">
          {category 
            ? `No quotes available in the "${category}" category yet.`
            : 'No quotes available at the moment.'
          }
        </p>
        <button
          onClick={refetch}
          className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors"
        >
          Refresh Quotes
        </button>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">
            {category ? `${category} Quotes` : 'All Quotes'}
          </h2>
          <p className="text-gray-600">
            Showing {displayedQuotes.length} of {quotes.length} quotes
          </p>
        </div>
        <div className="flex gap-2">
          {loading && (
            <div className="flex items-center text-gray-500">
              <div className="w-4 h-4 border-2 border-gray-300 border-t-blue-500 rounded-full animate-spin mr-2"></div>
              Loading...
            </div>
          )}
          <button
            onClick={refetch}
            disabled={loading}
            className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg transition-colors disabled:opacity-50"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {displayedQuotes.map((quote) => (
          <QuoteCard 
            key={quote.id} 
            quote={{
              id: quote.id,
              text: quote.quote,
              author: quote.author,
              category: quote.category
            }} 
            showActions={true}
            onClick={() => handleQuoteClick(quote)}
          />
        ))}
      </div>

      {limit && quotes.length > limit && (
        <div className="text-center mt-8">
          <p className="text-gray-600 mb-4">
            Showing {limit} of {quotes.length} quotes
          </p>
          <button 
            onClick={() => window.location.href = '/quotes'}
            className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-8 py-3 rounded-lg font-medium transition-all transform hover:scale-105"
          >
            View All {quotes.length} Quotes
          </button>
        </div>
      )}

      {/* Quote Modal */}
      <QuoteModal 
        quote={selectedQuote}
        isOpen={!!selectedQuote}
        onClose={closeModal}
      />
    </div>
  )
}
