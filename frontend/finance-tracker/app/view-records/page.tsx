'use client'

import { useState, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import Navigation from '../../components/Navigation'
import IndividualSelector from '../../components/IndividualSelector'
import { getRecords } from '../../lib/api'
import type { FinancialRecord } from '../../types'

export default function ViewRecords() {
  const searchParams = useSearchParams()
  const [selectedIndividual, setSelectedIndividual] = useState(
    searchParams.get('individual') || ''
  )
  const [records, setRecords] = useState<FinancialRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (selectedIndividual) {
      loadRecords()
    }
  }, [selectedIndividual])

  async function loadRecords() {
    try {
      setLoading(true)
      setError('')
      const data = await getRecords(selectedIndividual)
      console.log('Loaded records:', data)  // Debug log
      setRecords(data)
    } catch (error) {
      console.error('Failed to load records:', error)
      setError('Failed to load records')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-background">
        <div className="max-w-6xl mx-auto p-8">
          <h1 className="text-3xl font-bold mb-8 text-primary-dark">View Records</h1>

          <IndividualSelector
            selectedIndividual={selectedIndividual}
            onSelect={setSelectedIndividual}
          />

          {error && (
            <div className="mb-4 p-4 bg-error/10 text-error rounded-lg">{error}</div>
          )}

          {loading ? (
            <div className="text-center py-8">Loading...</div>
          ) : (
            <div className="mt-8">
              {records.length === 0 ? (
                <p className="text-center text-gray-medium">No records found</p>
              ) : (
                <table className="w-full">
                  <thead>
                    <tr>
                      <th className="text-left p-2">Date</th>
                      <th className="text-left p-2">Category</th>
                      <th className="text-left p-2">Description</th>
                      <th className="text-right p-2">Amount</th>
                    </tr>
                  </thead>
                  <tbody>
                    {records.map((record, index) => (
                      <tr key={index} className="border-t">
                        <td className="p-2">{record.date}</td>
                        <td className="p-2">{record.category}</td>
                        <td className="p-2">{record.description}</td>
                        <td className={`p-2 text-right ${
                          record.amount >= 0 ? 'text-success' : 'text-error'
                        }`}>
                          {record.amount.toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  )
}
