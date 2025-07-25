'use client'

import { useEffect } from 'react'

interface Quote {
  id: number
  quote: string
  author: string
  category: string
}

interface QuoteModalProps {
  quote: Quote | null
  isOpen: boolean
  onClose: () => void
}

export default function QuoteModal({ quote, isOpen, onClose }: QuoteModalProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose()
      }
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
      document.body.style.overflow = 'hidden'
    }

    return () => {
      document.removeEventListener('keydown', handleEscape)
      document.body.style.overflow = 'unset'
    }
  }, [isOpen, onClose])

  if (!isOpen || !quote) return null

  const getCategoryColor = (category: string) => {
    switch (category.toLowerCase()) {
      case 'motivational':
        return 'from-orange-400 to-red-500'
      case 'romantic':
        return 'from-pink-400 to-rose-500'
      case 'funny':
        return 'from-yellow-400 to-orange-500'
      case 'inspirational':
        return 'from-purple-400 to-indigo-500'
      default:
        return 'from-gray-400 to-gray-600'
    }
  }

  const getCategoryEmoji = (category: string) => {
    switch (category.toLowerCase()) {
      case 'motivational':
        return '💪'
      case 'romantic':
        return '💕'
      case 'funny':
        return '😂'
      case 'inspirational':
        return '✨'
      default:
        return '💭'
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="relative bg-white rounded-2xl shadow-2xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-auto">
        {/* Header */}
        <div className={`bg-gradient-to-r ${getCategoryColor(quote.category)} text-white p-6 rounded-t-2xl`}>
          <div className="flex justify-between items-start">
            <div className="flex items-center space-x-3">
              <span className="text-3xl">{getCategoryEmoji(quote.category)}</span>
              <div>
                <h2 className="text-xl font-semibold capitalize">{quote.category} Quote</h2>
                <p className="text-sm opacity-80">Quote #{quote.id}</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 transition-colors p-1"
              aria-label="Close modal"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-8">
          {/* Quote */}
          <blockquote className="text-center mb-8">
            <div className="text-4xl text-gray-300 mb-4">"</div>
            <p className="text-xl md:text-2xl text-gray-800 leading-relaxed font-medium mb-6">
              {quote.quote}
            </p>
            <footer className="text-lg text-gray-600">
              — <cite className="font-semibold">{quote.author}</cite>
            </footer>
          </blockquote>

          {/* Actions */}
          <div className="flex justify-center space-x-4">
            <button
              onClick={() => {
                navigator.clipboard.writeText(`"${quote.quote}" - ${quote.author}`)
                // Could add toast notification here
              }}
              className="flex items-center space-x-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <span>Copy Quote</span>
            </button>
            
            <button
              onClick={() => {
                const text = `"${quote.quote}" - ${quote.author}`
                const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`
                window.open(url, '_blank')
              }}
              className="flex items-center space-x-2 bg-sky-500 hover:bg-sky-600 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
              </svg>
              <span>Share</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
