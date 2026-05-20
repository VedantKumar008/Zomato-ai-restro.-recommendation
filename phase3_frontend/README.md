# Phase 3: Frontend Development

## Overview
This is the frontend application for the Zomato Restaurant Recommendation System. It provides a user-friendly interface for users to input their preferences and receive AI-powered restaurant recommendations.

## Tech Stack
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **UI Components**: Custom components built with Tailwind CSS

## Prerequisites
- Node.js 18+ installed
- Backend API running on `http://localhost:8000` (Phase 2)
- Phase 1 data layer completed

## Installation

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment Variables
Copy the example environment file:
```bash
cp .env.example .env.local
```

Edit `.env.local` if your backend API is running on a different port:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Development Server
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Project Structure
```
phase3_frontend/
├── src/
│   ├── app/
│   │   ├── globals.css       # Global styles with Tailwind
│   │   ├── layout.tsx         # Root layout component
│   │   └── page.tsx           # Main page component
│   ├── components/
│   │   ├── ui/                # Reusable UI components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── label.tsx
│   │   │   ├── select.tsx
│   │   │   ├── slider.tsx
│   │   │   └── textarea.tsx
│   │   ├── LoadingSkeleton.tsx    # Loading state component
│   │   ├── RecommendationForm.tsx # Main form component
│   │   ├── RestaurantCard.tsx     # Restaurant display card
│   │   └── ResultsDisplay.tsx    # Results container
│   └── lib/
│       ├── api.ts             # API service layer
│       └── utils.ts          # Utility functions
├── public/                   # Static assets
├── package.json              # Dependencies
├── tsconfig.json             # TypeScript config
├── tailwind.config.ts        # Tailwind CSS config
└── next.config.js            # Next.js config
```

## Features

### Input Form
- **Location Selector**: Dropdown with search for available cities
- **Budget Input**: Numeric input with validation for cost for two people
- **Cuisine Multi-Select**: Checkbox grid for selecting preferred cuisines
- **Rating Slider**: Visual slider for minimum rating preference (0-5)
- **Additional Preferences**: Text area for custom preferences

### Results Display
- **Restaurant Cards**: Beautiful cards showing restaurant details
  - Name and location
  - Rating with star icon
  - Cuisine types
  - Cost for two people
  - AI-generated explanation
- **Loading States**: Skeleton loaders during API calls
- **Error Handling**: User-friendly error messages
- **Empty States**: Helpful messages when no results found

### Responsive Design
- Mobile-first approach
- Responsive grid layout
- Touch-friendly controls
- Optimized for all screen sizes

## API Integration

The frontend communicates with the backend API through the following endpoints:

- `GET /health` - Health check
- `GET /locations` - Get available locations
- `GET /cuisines` - Get available cuisines
- `POST /recommend` - Get restaurant recommendations

## Build for Production

```bash
npm run build
npm start
```

## Component Library

### UI Components
All UI components are located in `src/components/ui/` and follow a consistent design system:
- **Button**: Multiple variants (default, destructive, outline, secondary, ghost, link)
- **Card**: Container components for content grouping
- **Input**: Form input with validation styling
- **Label**: Form label component
- **Select**: Dropdown select component
- **Slider**: Range slider for numeric inputs
- **Textarea**: Multi-line text input

### Feature Components
- **RecommendationForm**: Main form with all input fields
- **RestaurantCard**: Individual restaurant display
- **ResultsDisplay**: Container for results with loading/error states
- **LoadingSkeleton**: Animated placeholder during loading

## Styling

The application uses Tailwind CSS with a custom design system:
- Custom color palette defined in `tailwind.config.ts`
- CSS variables for theming
- Responsive breakpoints
- Dark mode support (ready for implementation)

## Error Handling

The application handles various error scenarios:
- API connection failures
- Invalid input validation
- Empty result sets
- Network timeouts

All errors are displayed with user-friendly messages and appropriate actions.

## Success Criteria (from Architecture.md)
- ✅ All input fields function correctly
- ✅ Results display properly with all required fields
- ✅ Application works on mobile and desktop
- ✅ User can complete full recommendation flow

## Next Steps
- Phase 4: Integration & Testing
- Phase 5: Deployment & Documentation
