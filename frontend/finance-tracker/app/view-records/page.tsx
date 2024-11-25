'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { FinancialRecord } from '@/types'
import { getRecords, editRecord, deleteRecord } from '@/lib/api'
import Navigation from '@/components/Navigation'
import { TrashIcon, PencilIcon } from '@heroicons/react/24/outline'

export default function ViewRecords() {
  const router = useRouter()
  const [records, setRecords] = useState<FinancialRecord[]>([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [editingRecord, setEditingRecord] = useState<{ index: number; record: FinancialRecord } | null>(null)

  useEffect(() => {
    fetchRecords()
  }, [])

  async function fetchRecords() {
    try {
      const data = await getRecords()
      setRecords(data)
    } catch (error) {
      setError('Failed to fetch records')
    } finally {
      setLoading(false)
    }
  }

  async function handleEditSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!editingRecord) return

    try {
      await editRecord(editingRecord.index, editingRecord.record)
      setEditingRecord(null)
      fetchRecords()
    } catch (error) {
      setError('Failed to update record')
    }
  }

  async function handleDelete(index: number) {
    if (!confirm('Are you sure you want to delete this record?')) return
    
    try {
      await deleteRecord(index)
      fetchRecords()
    } catch (error) {
      setError('Failed to delete record')
    }
  }

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-background">
        <div className="max-w-6xl mx-auto p-8">
          <h1 className="text-3xl font-bold mb-8 text-primary-dark">Financial Records</h1>
          {error ? (
            <div className="text-error bg-error/10 p-4 rounded-lg">{error}</div>
          ) : loading ? (
            <div className="text-primary">Loading...</div>
          ) : records.length === 0 ? (
            <div className="text-primary">No records found</div>
          ) : (
            <div className="bg-white rounded-xl shadow-md border border-primary-light/20 overflow-hidden">
              <table className="min-w-full">
                <thead className="bg-primary-light/10">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-primary-dark">Date</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-primary-dark">Description</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-primary-dark">Amount</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-primary-dark">Category</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-primary-dark">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-primary-light/20">
                  {records.map((record, index) => {
                    const formattedDate = new Date(record.date).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric'
                    })

                    return (
                      <tr key={index} className="hover:bg-primary-light/5">
                        <td className="px-6 py-4 text-gray-medium">{formattedDate}</td>
                        <td className="px-6 py-4 text-gray-medium">{record.description}</td>
                        <td className={`px-6 py-4 text-lg font-semibold ${
                          record.amount > 0 
                            ? 'text-success-dark bg-success-light/10' 
                            : 'text-error bg-error/10'
                        }`}>
                          <span className="inline-block px-3 py-1 rounded">
                            ${Math.abs(record.amount).toFixed(2)}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-gray-medium">{record.category}</td>
                        <td className="px-6 py-4 flex gap-3">
                          <button
                            onClick={() => setEditingRecord({ index, record: { ...record } })}
                            className="text-primary hover:text-primary-dark"
                          >
                            <PencilIcon className="h-5 w-5" />
                          </button>
                          <button
                            onClick={() => handleDelete(index)}
                            className="text-error hover:text-error/80"
                          >
                            <TrashIcon className="h-5 w-5" />
                          </button>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Edit Modal */}
      {editingRecord && (
        <div className="fixed inset-0 bg-foreground/50 flex items-center justify-center">
          <div className="bg-white p-8 rounded-xl max-w-md w-full mx-4 shadow-lg">
            <h2 className="text-2xl font-bold mb-6 text-primary-dark">Edit Record</h2>
            <form onSubmit={handleEditSubmit} className="space-y-4">
              <div className="mb-4">
                <label className="block mb-2">
                  Date
                  <input
                    type="date"
                    value={editingRecord.record.date}
                    onChange={(e) => setEditingRecord({ ...editingRecord, record: { ...editingRecord.record, date: e.target.value } })}
                    className="mt-1 block w-full"
                  />
                </label>
              </div>
              <div className="mb-4">
                <label className="block mb-2">
                  Description
                  <input
                    type="text"
                    value={editingRecord.record.description}
                    onChange={(e) => setEditingRecord({ ...editingRecord, record: { ...editingRecord.record, description: e.target.value } })}
                    className="mt-1 block w-full"
                  />
                </label>
              </div>
              <div className="mb-4">
                <label className="block mb-2">
                  Amount
                  <input
                    type="number"
                    step="0.01"
                    value={editingRecord.record.amount}
                    onChange={(e) => setEditingRecord({ ...editingRecord, record: { ...editingRecord.record, amount: Number(e.target.value) } })}
                    className="mt-1 block w-full"
                  />
                </label>
              </div>
              <div className="mb-4">
                <label className="block mb-2">
                  Category
                  <input
                    type="text"
                    value={editingRecord.record.category}
                    onChange={(e) => setEditingRecord({ ...editingRecord, record: { ...editingRecord.record, category: e.target.value } })}
                    className="mt-1 block w-full"
                  />
                </label>
              </div>
              <div className="flex justify-end gap-4 mt-6">
                <button
                  type="button"
                  onClick={() => setEditingRecord(null)}
                  className="px-4 py-2 text-gray-medium hover:text-primary-dark"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  )
}
