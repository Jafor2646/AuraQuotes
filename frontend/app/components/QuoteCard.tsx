'use client'

interface Quote {
  id: number
  text?: string
  quote?: string
  author: string
  category?: string
}

interface QuoteCardProps {
  quote: Quote
  showActions?: boolean
  onClick?: () => void
}

export default function QuoteCard({ quote, showActions = true, onClick }: QuoteCardProps) {
  // Support both 'text' and 'quote' properties for backwards compatibility
  const quoteText = quote.text || quote.quote || ''
  const getCategoryEmoji = (category?: string) => {
    if (!category) return '💭'
    switch (category.toLowerCase()) {
      case 'motivational':
        return '💪'
      case 'romantic':
        return '💖'
      case 'funny':
        return '😂'
      case 'inspirational':
        return '✨'
      default:
        return '💭'
    }
  }

  const getCategoryColor = (category?: string) => {
    if (!category) return 'from-gray-400 to-gray-500'
    switch (category.toLowerCase()) {
      case 'motivational':
        return 'from-orange-400 to-red-500'
      case 'romantic':
        return 'from-pink-400 to-red-500'
      case 'funny':
        return 'from-yellow-400 to-orange-500'
      case 'inspirational':
        return 'from-blue-400 to-purple-500'
      default:
        return 'from-gray-400 to-gray-500'
    }
  }

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          text: `"${quoteText}" — ${quote.author}`,
          title: 'Inspirational Quote'
        })
      } catch (err) {
        console.log('Share cancelled')
      }
    } else {
      // Fallback for browsers that don't support native sharing
      handleCopy()
    }
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(`"${quoteText}" — ${quote.author}`)
      // You could add a toast notification here
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  return (
    <div 
      className={`quote-card bg-white rounded-xl shadow-lg p-6 border hover:shadow-xl transition-all duration-300 ${onClick ? 'cursor-pointer hover:scale-105' : ''}`}
      onClick={onClick}
    >
      {quote.category && (
        <div className="flex items-center justify-between mb-4">
          <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium text-white bg-gradient-to-r ${getCategoryColor(quote.category)}`}>
            {getCategoryEmoji(quote.category)} {quote.category.charAt(0).toUpperCase() + quote.category.slice(1)}
          </span>
        </div>
      )}
      
      <blockquote className="text-gray-800 text-lg font-medium leading-relaxed mb-4">
        "{quoteText}"
      </blockquote>
      
      <div className="flex items-center justify-between">
        <cite className="text-gray-600 text-sm font-medium">
          — {quote.author}
        </cite>
        {showActions && (
          <div className="flex gap-2">
            <button 
              onClick={(e) => {
                e.stopPropagation()
                handleShare()
              }}
              className="text-gray-400 hover:text-blue-500 transition-colors p-1"
              title="Share quote"
            >
              📤
            </button>
            <button 
              onClick={(e) => {
                e.stopPropagation()
                handleCopy()
              }}
              className="text-gray-400 hover:text-green-500 transition-colors p-1"
              title="Copy quote"
            >
              📋
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
