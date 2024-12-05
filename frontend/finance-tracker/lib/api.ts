import { FinancialRecord, NetWorthData } from '../types/index'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:5000/api'

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.message || 'An error occurred')
  }
  return response.json()
}

export async function getIndividuals(): Promise<string[]> {
  const response = await fetch(`${API_BASE}/individuals`)
  return handleResponse(response)
}

export async function addIndividual(name: string): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE}/individuals`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name }),
  })
  return handleResponse(response)
}

export async function getRecords(individual: string, type?: 'income' | 'expense'): Promise<FinancialRecord[]> {
  const params = type ? `?type=${type}` : ''
  const response = await fetch(`${API_BASE}/records/${individual}${params}`)
  return handleResponse(response)
}

export async function addRecord(individual: string, record: Omit<FinancialRecord, 'date'>): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE}/records/${individual}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(record),
  })
  return handleResponse(response)
}

export async function getNetWorth(individual: string): Promise<NetWorthData> {
  const response = await fetch(`${API_BASE}/net-worth/${individual}`)
  return handleResponse(response)
}

export async function editRecord(individual: string, index: number, record: Omit<FinancialRecord, 'date'>): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE}/records/${individual}/${index}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(record),
  })
  return handleResponse(response)
}

export async function deleteRecord(individual: string, index: number): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE}/records/${individual}/${index}`, {
    method: 'DELETE',
  })
  return handleResponse(response)
}