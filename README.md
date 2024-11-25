# FinSight

A modern personal finance tracking application with both web and API interfaces. Built with Next.js for the frontend and Flask for the backend.

## Features

- Track income and expenses with detailed records
- Calculate and monitor net worth in real-time
- Modern, responsive UI with dark mode support
- Edit and delete financial records
- Comprehensive financial overview dashboard

## Tech Stack

### Frontend
- Next.js 15.0
- TypeScript
- Tailwind CSS
- Heroicons
- Custom color system with light/dark mode

### Backend
- Flask
- Python
- CSV-based data storage

## Getting Started

### Frontend Setup
1. Navigate to the frontend directory:

```bash
cd frontend/finance-tracker
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Backend Setup
1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the Flask server:
```bash
python run.py
```

The backend API will be available at `http://localhost:5000`

## Project Structure

### Frontend
- `/app` - Next.js pages and layouts
- `/components` - Reusable React components
- `/lib` - API utilities and helpers
- `/types` - TypeScript type definitions

### Backend
- `/app/routes` - Flask route handlers
- `/app/models` - Data models and business logic
- `/app/templates` - HTML templates

## Features in Detail

### Financial Records
- Add income and expense records with descriptions
- View all financial records in a sortable table
- Edit existing records
- Delete unwanted records

### Net Worth Tracking
- Real-time calculation of total income and expenses
- Current net worth display
- Visual representation of financial health

### User Interface
- Responsive design that works on mobile and desktop
- Dark mode support for comfortable viewing
- Intuitive navigation and data entry
- Clean, modern aesthetic with consistent styling

## Environment Variables

Create a `.env` file in the frontend directory with:
```
API_BASE=http://localhost:5000
NEXT_PUBLIC_API_BASE=http://localhost:5000
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
