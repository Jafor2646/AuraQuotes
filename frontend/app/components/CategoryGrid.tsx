'use client'

import Link from 'next/link'
import { useCategories } from '../../hooks'

export default function CategoryGrid() {
  const { categories, loading, error } = useCategories()

  const getCategoryGradient = (categoryName: string) => {
    switch (categoryName.toLowerCase()) {
      case 'motivational':
        return 'from-orange-400 to-red-500 hover:from-orange-500 hover:to-red-600'
      case 'romantic':
        return 'from-pink-400 to-red-500 hover:from-pink-500 hover:to-red-600'
      case 'funny':
        return 'from-yellow-400 to-orange-500 hover:from-yellow-500 hover:to-orange-600'
      case 'inspirational':
        return 'from-blue-400 to-purple-500 hover:from-blue-500 hover:to-purple-600'
      default:
        return 'from-gray-400 to-gray-500 hover:from-gray-500 hover:to-gray-600'
    }
  }

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-gray-200 rounded-xl p-6 shadow-lg animate-pulse">
            <div className="text-center">
              <div className="w-16 h-16 bg-gray-300 rounded-full mx-auto mb-3"></div>
              <div className="h-6 bg-gray-300 rounded mb-2"></div>
              <div className="h-4 bg-gray-300 rounded"></div>
            </div>
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
          onClick={() => window.location.reload()}
          className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors"
        >
          Try Again
        </button>
      </div>
    )
  }

  if (categories.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📂</div>
        <h3 className="text-xl font-semibold text-gray-700 mb-2">No categories found</h3>
        <p className="text-gray-500 mb-4">
          No quote categories are available at the moment.
        </p>
        <button
          onClick={() => window.location.reload()}
          className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors"
        >
          Refresh Categories
        </button>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {categories.map((category) => (
        <Link
          key={category.name}
          href={`/quotes/${category.name}`}
          className="group"
        >
          <div className={`bg-gradient-to-br ${getCategoryGradient(category.name)} text-white rounded-xl p-6 shadow-lg transition-all duration-300 transform group-hover:scale-105 group-hover:shadow-xl`}>
            <div className="text-center">
              <div className="text-4xl mb-3 group-hover:animate-bounce">
                {category.emoji}
              </div>
              <h3 className="text-xl font-bold mb-2 capitalize">
                {category.name}
              </h3>
              <p className="text-sm opacity-90 leading-relaxed">
                {category.description}
              </p>
            </div>
            
            <div className="mt-4 flex items-center justify-center">
              <span className="text-sm opacity-75 group-hover:opacity-100 transition-opacity">
                Explore quotes →
              </span>
            </div>
          </div>
        </Link>
      ))}
    </div>
  )
}
