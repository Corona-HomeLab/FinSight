import { FinancialRecord, NetWorthData } from '../types/index'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:5000/api'

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.message || 'An error occurred')
  }
  return response.json()
}

export async function addRecord(record: Omit<FinancialRecord, 'date'>): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE}/records`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(record),
  })
  
  return handleResponse(response)
}

export async function getRecords(type?: 'income' | 'expense'): Promise<FinancialRecord[]> {
  const params = type ? `?type=${type}` : ''
  const response = await fetch(`${API_BASE}/records${params}`)
  
  return handleResponse(response)
}

export async function getNetWorth(): Promise<NetWorthData> {
  const response = await fetch(`${API_BASE}/net-worth`)
  
  return handleResponse(response)
}

export async function editRecord(index: number, record: FinancialRecord): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE}/records/${index}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(record),
  })
  
  return handleResponse(response)
}

export async function deleteRecord(index: number): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE}/records/${index}`, {
    method: 'DELETE',
  })
  
  return handleResponse(response)
}