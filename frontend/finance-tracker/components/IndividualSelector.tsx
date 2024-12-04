'use client'
import { useState, useEffect } from 'react'
import { getIndividuals, addIndividual } from '../lib/api'

interface Props {
  selectedIndividual: string
  onSelect: (individual: string) => void
}

const IndividualSelector = ({ selectedIndividual, onSelect }: Props) => {
  const [individuals, setIndividuals] = useState<string[]>([])
  const [isAdding, setIsAdding] = useState(false)
  const [newName, setNewName] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    loadIndividuals()
  }, [])

  async function loadIndividuals() {
    try {
      setError('')
      const data = await getIndividuals()
      
      if (Array.isArray(data)) {
        setIndividuals(data)
        if (data.length && !selectedIndividual) {
          onSelect(data[0])
        }
      } else {
        throw new Error('Invalid response format')
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to load individuals'
      setError(message)
      console.error('Failed to load individuals:', error)
    }
  }

  async function handleAdd() {
    try {
      setError('')
      if (!newName.trim()) {
        setError('Name cannot be empty')
        return
      }
      await addIndividual(newName)
      setNewName('')
      setIsAdding(false)
      await loadIndividuals()
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to add individual'
      setError(message)
      console.error('Failed to add individual:', error)
    }
  }

  return (
    <div className="mb-6">
      {error && (
        <div className="mb-4 p-4 bg-error/10 text-error rounded-lg">
          {error}
        </div>
      )}
      
      <div className="flex items-center gap-4">
        <select
          value={selectedIndividual}
          onChange={(e) => onSelect(e.target.value)}
          className="p-2 border rounded"
        >
          {individuals.length === 0 && (
            <option value="">No individuals available</option>
          )}
          {individuals.map((name) => (
            <option key={name} value={name}>
              {name}
            </option>
          ))}
        </select>
        <button
          onClick={() => setIsAdding(true)}
          className="bg-primary text-white px-4 py-2 rounded"
        >
          Add Individual
        </button>
      </div>

      {isAdding && (
        <div className="mt-4 flex gap-2">
          <input
            type="text"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            placeholder="Enter name"
            className="p-2 border rounded"
          />
          <button
            onClick={handleAdd}
            className="bg-success text-white px-4 py-2 rounded"
          >
            Save
          </button>
          <button
            onClick={() => {
              setIsAdding(false)
              setNewName('')
              setError('')
            }}
            className="bg-gray-medium text-white px-4 py-2 rounded"
          >
            Cancel
          </button>
        </div>
      )}
    </div>
  )
}

export default IndividualSelector
