'use client'

import Navigation from '@/components/Navigation'
import Link from 'next/link'

export default function Home() {
  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-background">
        <div className="max-w-6xl mx-auto p-8">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold mb-4 text-primary-dark">Welcome to FinSight</h1>
            <p className="text-xl text-gray-medium">Take control of your financial future</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-xl transition-shadow border border-primary-light/20">
              <h2 className="text-2xl font-semibold mb-4 text-primary-dark">Add Record</h2>
              <p className="text-gray-medium mb-6">Track your daily transactions with ease.</p>
              <Link 
                href="/add-record"
                className="inline-block bg-primary text-white px-6 py-3 rounded-lg hover:bg-primary-dark transition-colors"
              >
                Add Record
              </Link>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-xl transition-shadow border border-primary-light/20">
              <h2 className="text-2xl font-semibold mb-4 text-primary-dark">View Records</h2>
              <p className="text-gray-medium mb-6">Monitor all your transactions in one place.</p>
              <Link 
                href="/view-records"
                className="inline-block bg-success text-white px-6 py-3 rounded-lg hover:bg-success-dark transition-colors"
              >
                View Records
              </Link>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-xl transition-shadow border border-primary-light/20">
              <h2 className="text-2xl font-semibold mb-4 text-primary-dark">Net Worth</h2>
              <p className="text-gray-medium mb-6">Track your wealth building progress.</p>
              <Link 
                href="/net-worth"
                className="inline-block bg-accent-purple text-white px-6 py-3 rounded-lg hover:bg-purple-800 transition-colors"
              >
                View Net Worth
              </Link>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-gradient-to-br from-primary-light/10 to-white p-8 rounded-xl shadow-md">
              <h2 className="text-2xl font-semibold mb-6 text-primary-dark">Why Use FinSight?</h2>
              <ul className="space-y-4 text-gray-medium">
                <li className="flex items-center">
                  <span className="text-success mr-2">●</span>
                  Easy and intuitive financial tracking
                </li>
                <li className="flex items-center">
                  <span className="text-success mr-2">●</span>
                  Comprehensive net worth monitoring
                </li>
                <li className="flex items-center">
                  <span className="text-success mr-2">●</span>
                  Simple income and expense management
                </li>
                <li className="flex items-center">
                  <span className="text-success mr-2">●</span>
                  Clear financial overview
                </li>
              </ul>
            </div>

            <div className="bg-gradient-to-br from-primary-light/10 to-white p-8 rounded-xl shadow-md">
              <h2 className="text-2xl font-semibold mb-6 text-primary-dark">Getting Started</h2>
              <ol className="space-y-4 text-gray-medium list-decimal list-inside">
                <li>Add your first income or expense record</li>
                <li>Track your transactions regularly</li>
                <li>Monitor your net worth growth</li>
                <li>Make informed financial decisions</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
