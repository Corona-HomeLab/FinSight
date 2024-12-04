'use client'
import { useState } from 'react'
import Navigation from '../components/Navigation'
import IndividualSelector from '../components/IndividualSelector'

export default function Home() {
  const [selectedIndividual, setSelectedIndividual] = useState('')

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-background">
        <div className="max-w-6xl mx-auto p-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-primary-dark">
              Personal Finance Tracker
            </h1>
          </div>

          <IndividualSelector
            selectedIndividual={selectedIndividual}
            onSelect={setSelectedIndividual}
          />
          
          {/* Add other components or content here */}
        </div>
      </div>
    </>
  )
}
