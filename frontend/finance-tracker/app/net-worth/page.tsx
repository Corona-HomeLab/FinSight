'use client'

import { useState, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import { getNetWorth } from '@/lib/api'
import Navigation from '@/components/Navigation'
import IndividualSelector from '@/components/IndividualSelector'
import type { NetWorthData } from '@/types'

export default function NetWorth() {
  const searchParams = useSearchParams()
  const [selectedIndividual, setSelectedIndividual] = useState(
    searchParams.get('individual') || ''
  )
  const [data, setData] = useState<NetWorthData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (selectedIndividual) {
      loadNetWorth()
    }
  }, [selectedIndividual])

  async function loadNetWorth() {
    try {
      setLoading(true)
      const netWorthData = await getNetWorth(selectedIndividual)
      setData(netWorthData)
      setError('')
    } catch (error) {
      setError('Failed to fetch net worth data')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-background">
        <div className="max-w-4xl mx-auto p-8">
          <h1 className="text-3xl font-bold mb-8 text-primary-dark">Net Worth Overview</h1>

          <IndividualSelector
            selectedIndividual={selectedIndividual}
            onSelect={setSelectedIndividual}
          />

          {error && (
            <div className="mb-4 p-4 bg-error/10 text-error rounded-lg">{error}</div>
          )}

          {loading ? (
            <div className="text-center p-8">Loading...</div>
          ) : data && (
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
                <p className="text-3xl font-bold text-error">${Math.abs(data.total_expenses).toFixed(2)}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  )
}
