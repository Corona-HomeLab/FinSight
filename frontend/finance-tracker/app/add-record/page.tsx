'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { addRecord } from '@/lib/api'
import Navigation from '@/components/Navigation'

export default function AddRecord() {
  const router = useRouter()
  const [category, setCategory] = useState<'Income' | 'Expense'>('Income')
  const [amount, setAmount] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    try {
      await addRecord({
        amount: parseFloat(amount),
        category,
        description,
      })
      router.push('/view-records')
    } catch (error) {
      setError('Failed to add record')
    }
  }

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto p-8">
          <h1 className="text-3xl font-bold mb-8 text-primary-dark">Add New Record</h1>
          {error && <div className="text-error bg-error/10 p-4 rounded-lg">{error}</div>}
          <div className="bg-white p-8 rounded-xl shadow-md border border-primary-light/20">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block mb-2 font-semibold text-primary-dark">Type</label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value as 'Income' | 'Expense')}
                  className={`w-full p-3 border border-primary-light rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-white text-lg font-medium ${
                    category === 'Income' ? 'text-success-dark' : 'text-error'
                  }`}
                >
                  <option value="Income">Income</option>
                  <option value="Expense">Expense</option>
                </select>
              </div>
              <div>
                <label className="block mb-2 font-semibold text-primary-dark">Amount</label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-primary-dark">$</span>
                  <input
                    type="number"
                    step="0.01"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    className="w-full p-3 pl-7 border border-primary-light rounded-lg focus:ring-2 focus:ring-primary focus:border-primary text-primary-dark"
                    required
                  />
                </div>
              </div>
              <div>
                <label className="block mb-2 font-semibold text-primary-dark">Description</label>
                <input
                  type="text"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full p-3 border border-primary-light rounded-lg focus:ring-2 focus:ring-primary focus:border-primary text-primary-dark"
                  required
                />
              </div>
              <button
                type="submit"
                className={`w-full py-3 px-6 rounded-lg text-white font-medium transition-colors ${
                  category === 'Income' 
                    ? 'bg-success hover:bg-success-dark' 
                    : 'bg-error hover:bg-error/80'
                }`}
              >
                Add {category}
              </button>
            </form>
          </div>
        </div>
      </div>
    </>
  )
}
