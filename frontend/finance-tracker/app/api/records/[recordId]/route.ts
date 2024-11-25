import { NextResponse } from 'next/server'

export async function GET(
  request: Request,
  { params }: { params: { recordId: string } }
) {
  try {
    const response = await fetch(`${process.env.API_BASE}/records/${params.recordId}`)
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch record' }, { status: 500 })
  }
}

export async function PUT(
  request: Request,
  { params }: { params: { recordId: string } }
) {
  try {
    const body = await request.json()
    const response = await fetch(`${process.env.API_BASE}/records/${params.recordId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json({ error: 'Failed to update record' }, { status: 500 })
  }
}