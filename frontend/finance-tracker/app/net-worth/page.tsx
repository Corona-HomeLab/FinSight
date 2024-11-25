'use client'

import { useEffect, useState } from 'react'
import { NetWorthData } from '@/types'
import { getNetWorth } from '@/lib/api'
import Navigation from '@/components/Navigation'

export default function NetWorth() {
  const [data, setData] = useState<NetWorthData | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetchNetWorth() {
      try {
        const netWorthData = await getNetWorth()
        setData(netWorthData)
      } catch (error) {
        setError('Failed to fetch net worth data')
        console.error('Error:', error)
      }
    }
    fetchNetWorth()
  }, [])

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-background">
        <div className="max-w-4xl mx-auto p-8">
          <h1 className="text-3xl font-bold mb-8 text-primary-dark">Net Worth Overview</h1>
          {error ? (
            <div className="text-error bg-error/10 p-4 rounded-lg">{error}</div>
          ) : !data ? (
            <div className="text-primary p-4">Loading...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-xl shadow-md border border-primary-light/20">
                <h2 className="text-xl font-semibold mb-2 text-primary-dark">Net Worth</h2>
                <p className="text-3xl font-bold text-primary">${data.net_worth.toFixed(2)}</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md border border-primary-light/20">
                <h2 className="text-xl font-semibold mb-2 text-primary-dark">Total Income</h2>
                <p className="text-3xl font-bold text-success">${data.total_income.toFixed(2)}</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md border border-primary-light/20">
                <h2 className="text-xl font-semibold mb-2 text-primary-dark">Total Expenses</h2>
                <p className="text-3xl font-bold text-error">${data.total_expenses.toFixed(2)}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  )
}
