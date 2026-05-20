'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Star, MapPin, Utensils, IndianRupee } from 'lucide-react';

interface RestaurantCardProps {
  restaurant: {
    name: string;
    location: string;
    city: string;
    cuisines: string;
    cost: number;
    rating: number;
    explanation?: string;
  };
}

export const RestaurantCard: React.FC<RestaurantCardProps> = ({ restaurant }) => {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <CardTitle className="text-xl">{restaurant.name}</CardTitle>
        <CardDescription className="flex items-center gap-2">
          <MapPin className="h-4 w-4" />
          {restaurant.location}, {restaurant.city}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Rating */}
        <div className="flex items-center gap-2">
          <Star className="h-5 w-5 fill-yellow-400 text-yellow-400" />
          <span className="font-semibold text-lg">{restaurant.rating.toFixed(1)}</span>
          <span className="text-sm text-muted-foreground">/ 5.0</span>
        </div>

        {/* Cuisines */}
        <div className="flex items-start gap-2">
          <Utensils className="h-5 w-5 text-muted-foreground mt-0.5" />
          <div>
            <p className="text-sm font-medium">Cuisines</p>
            <p className="text-sm text-muted-foreground">{restaurant.cuisines}</p>
          </div>
        </div>

        {/* Cost */}
        <div className="flex items-center gap-2">
          <IndianRupee className="h-5 w-5 text-muted-foreground" />
          <div>
            <p className="text-sm font-medium">Cost for two</p>
            <p className="text-sm text-muted-foreground">{restaurant.cost.toFixed(0)} INR</p>
          </div>
        </div>

        {/* Explanation */}
        {restaurant.explanation && (
          <div className="pt-3 border-t">
            <p className="text-sm text-muted-foreground italic">
              "{restaurant.explanation}"
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
