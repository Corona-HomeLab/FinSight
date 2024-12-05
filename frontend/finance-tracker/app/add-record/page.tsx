'use client'

import { useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { addRecord } from '@/lib/api'
import Navigation from '@/components/Navigation'
import IndividualSelector from '@/components/IndividualSelector'

export default function AddRecord() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [selectedIndividual, setSelectedIndividual] = useState(
    searchParams.get('individual') || ''
  )
  const [amount, setAmount] = useState('')
  const [category, setCategory] = useState<'Income' | 'Expense'>('Income')
  const [description, setDescription] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!selectedIndividual) {
      setError('Please select an individual')
      return
    }

    try {
      await addRecord(selectedIndividual, {
        amount: parseFloat(amount),
        category,
        description,
      })
      router.push(`/view-records?individual=${selectedIndividual}`)
    } catch (error) {
      setError('Failed to add record')
    }
  }

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-background">
        <div className="max-w-4xl mx-auto p-8">
          <h1 className="text-3xl font-bold mb-8 text-primary-dark">Add Record</h1>

          <IndividualSelector
            selectedIndividual={selectedIndividual}
            onSelect={setSelectedIndividual}
          />

          {error && (
            <div className="mb-4 p-4 bg-error/10 text-error rounded-lg">{error}</div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-xl shadow-md">
            <div>
              <label className="block mb-2 text-gray-medium">Amount</label>
              <input
                type="number"
                step="0.01"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="w-full p-2 border rounded"
                required
              />
            </div>

            <div>
              <label className="block mb-2 text-gray-medium">Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value as 'Income' | 'Expense')}
                className="w-full p-2 border rounded"
              >
                <option value="Income">Income</option>
                <option value="Expense">Expense</option>
              </select>
            </div>

            <div>
              <label className="block mb-2 text-gray-medium">Description</label>
              <input
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full p-2 border rounded"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full bg-primary text-white py-2 rounded hover:bg-primary-dark"
            >
              Add Record
            </button>
          </form>
        </div>
      </div>
    </>
  )
}
