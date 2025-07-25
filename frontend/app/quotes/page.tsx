'use client'

import Navbar from '../components/Navbar'
import QuotesGrid from '../components/QuotesGrid'

export default function QuotesPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            All Quotes
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Discover wisdom, motivation, and inspiration from our complete collection of quotes
          </p>
        </div>

        <QuotesGrid />
      </div>
    </div>
  )
}
