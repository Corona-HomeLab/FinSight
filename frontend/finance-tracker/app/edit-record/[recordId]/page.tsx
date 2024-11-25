'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import type { FinancialRecord } from '@/types/index'

export default function EditRecord({ params }: { params: { recordId: string } }) {
  const router = useRouter()
  const [formData, setFormData] = useState({
    category: 'Income' as 'Income' | 'Expense',
    description: '',
    amount: ''
  })
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!params.recordId) return

    fetch(`http://localhost:5000/api/records/${params.recordId}`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch record')
        return res.json()
      })
      .then((record: FinancialRecord) => {
        setFormData({
          category: record.amount > 0 ? 'Income' : 'Expense',
          description: record.description,
          amount: Math.abs(record.amount).toString()
        })
      })
      .catch(err => {
        console.error('Error:', err)
        setError('Error loading record')
      })
      .finally(() => {
        setIsLoading(false)
      })
  }, [params.recordId])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const response = await fetch(`http://localhost:5000/api/records/${params.recordId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          amount: formData.category === 'Income' 
            ? parseFloat(formData.amount) 
            : -parseFloat(formData.amount)
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to update record')
      }

      router.push('/view-records')
      router.refresh()
    } catch (err) {
      console.error('Error:', err)
      setError('Failed to update record')
    }
  }

  if (isLoading) return <div>Loading...</div>
  if (error) return <div className="text-red-500 p-4">{error}</div>

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto mt-8 p-4">
      <h1 className="text-2xl font-bold mb-6">Edit Record</h1>
      <div className="mb-4">
        <label className="block mb-2 font-medium">Category</label>
        <select
          value={formData.category}
          onChange={(e) => setFormData({...formData, category: e.target.value as 'Income' | 'Expense'})}
          className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
        >
          <option value="Income">Income</option>
          <option value="Expense">Expense</option>
        </select>
      </div>
      <div className="mb-4">
        <label className="block mb-2 font-medium">Description</label>
        <input
          type="text"
          value={formData.description}
          onChange={(e) => setFormData({...formData, description: e.target.value})}
          className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block mb-2 font-medium">Amount</label>
        <input
          type="number"
          value={formData.amount}
          onChange={(e) => setFormData({...formData, amount: e.target.value})}
          className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
          min="0"
          step="0.01"
          required
        />
      </div>
      <div className="flex gap-4">
        <button 
          type="submit" 
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Update Record
        </button>
        <button 
          type="button" 
          onClick={() => router.back()} 
          className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
        >
          Cancel
        </button>
      </div>
    </form>
  )
}
