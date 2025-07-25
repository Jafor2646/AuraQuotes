'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-2xl">✨</span>
            <span className="text-2xl font-bold text-gray-900">AuraQuotes</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              Home
            </Link>
            <Link href="/quotes/motivational" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              💪 Motivational
            </Link>
            <Link href="/quotes/romantic" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              💖 Romantic
            </Link>
            <Link href="/quotes/funny" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              😂 Funny
            </Link>
            <Link href="/quotes/inspirational" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              ✨ Inspirational
            </Link>
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Toggle menu"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {isMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t">
            <div className="flex flex-col space-y-2">
              <Link href="/" className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded">
                Home
              </Link>
              <Link href="/quotes/motivational" className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded">
                💪 Motivational
              </Link>
              <Link href="/quotes/romantic" className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded">
                💖 Romantic
              </Link>
              <Link href="/quotes/funny" className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded">
                😂 Funny
              </Link>
              <Link href="/quotes/inspirational" className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded">
                ✨ Inspirational
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
