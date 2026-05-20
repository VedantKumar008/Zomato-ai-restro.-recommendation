'use client';

import React from 'react';
import { RestaurantCard } from './RestaurantCard';
import { LoadingSkeleton } from './LoadingSkeleton';
import { AlertCircle } from 'lucide-react';

interface ResultsDisplayProps {
  recommendations: any[];
  totalFound: number;
  isLoading: boolean;
  error: string | null;
}

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({
  recommendations,
  totalFound,
  isLoading,
  error,
}) => {
  if (isLoading) {
    return <LoadingSkeleton />;
  }

  if (error) {
    return (
      <div className="flex items-center gap-3 p-4 bg-destructive/10 text-destructive rounded-lg">
        <AlertCircle className="h-5 w-5" />
        <p>{error}</p>
      </div>
    );
  }

  if (recommendations.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground text-lg">
          No restaurants found matching your criteria.
        </p>
        <p className="text-muted-foreground text-sm mt-2">
          Try adjusting your filters or increasing your budget.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Recommendations</h2>
        <p className="text-muted-foreground">
          Found {totalFound} restaurants
        </p>
      </div>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {recommendations.map((restaurant, index) => (
          <RestaurantCard key={index} restaurant={restaurant} />
        ))}
      </div>
    </div>
  );
};
