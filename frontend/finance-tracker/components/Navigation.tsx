import Link from 'next/link'

export default function Navigation() {
  return (
    <nav className="bg-primary-dark text-white shadow-lg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="text-xl font-bold hover:text-primary-light">
            FinSight
          </Link>
          <div className="flex space-x-4">
            <Link href="/add-record" className="hover:text-primary-light px-3 py-2 rounded-md transition-colors">
              Add Record
            </Link>
            <Link href="/view-records" className="hover:text-primary-light px-3 py-2 rounded-md transition-colors">
              View Records
            </Link>
            <Link href="/net-worth" className="hover:text-primary-light px-3 py-2 rounded-md transition-colors">
              Net Worth
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}