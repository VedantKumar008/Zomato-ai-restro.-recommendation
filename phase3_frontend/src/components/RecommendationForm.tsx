'use client';

import React, { useState, useEffect } from 'react';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Select } from './ui/select';
import { Slider } from './ui/slider';
import { Textarea } from './ui/textarea';
import { Button } from './ui/button';
import { apiService } from '../lib/api';

interface RecommendationFormProps {
  onSubmit: (data: any) => void;
  isLoading: boolean;
}

export const RecommendationForm: React.FC<RecommendationFormProps> = ({ onSubmit, isLoading }) => {
  const [location, setLocation] = useState('');
  const [budget, setBudget] = useState(1000);
  const [selectedCuisines, setSelectedCuisines] = useState<string[]>([]);
  const [minRating, setMinRating] = useState(3.5);
  const [additionalPreferences, setAdditionalPreferences] = useState('');
  
  const [locations, setLocations] = useState<string[]>([]);
  const [cuisines, setCuisines] = useState<string[]>([]);
  const [loadingOptions, setLoadingOptions] = useState(true);

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const [locs, cuis] = await Promise.all([
          apiService.getLocations(),
          apiService.getCuisines()
        ]);
        setLocations(locs);
        setCuisines(cuis);
      } catch (error) {
        console.error('Error fetching options:', error);
      } finally {
        setLoadingOptions(false);
      }
    };

    fetchOptions();
  }, []);

  const handleCuisineToggle = (cuisine: string) => {
    setSelectedCuisines(prev =>
      prev.includes(cuisine)
        ? prev.filter(c => c !== cuisine)
        : [...prev, cuisine]
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!location || !budget) {
      alert('Please fill in location and budget');
      return;
    }

    onSubmit({
      location,
      budget,
      cuisines: selectedCuisines.length > 0 ? selectedCuisines : undefined,
      min_rating: minRating,
      additional_preferences: additionalPreferences || undefined,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Location Selector */}
      <div className="space-y-2">
        <Label htmlFor="location">Location *</Label>
        <Select
          id="location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          disabled={loadingOptions || isLoading}
          required
        >
          <option value="">Select a location</option>
          {locations.map((loc) => (
            <option key={loc} value={loc}>
              {loc}
            </option>
          ))}
        </Select>
      </div>

      {/* Budget Input */}
      <div className="space-y-2">
        <Label htmlFor="budget">Budget (INR for two people) *</Label>
        <Input
          id="budget"
          type="number"
          min="100"
          step="100"
          value={budget}
          onChange={(e) => setBudget(Number(e.target.value))}
          disabled={isLoading}
          required
        />
        <p className="text-sm text-muted-foreground">
          Maximum cost for two people
        </p>
      </div>

      {/* Cuisine Multi-Select */}
      <div className="space-y-2">
        <Label>Cuisines (Optional)</Label>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2 max-h-48 overflow-y-auto p-2 border rounded-md">
          {cuisines.map((cuisine) => (
            <label
              key={cuisine}
              className="flex items-center space-x-2 cursor-pointer p-2 hover:bg-accent rounded"
            >
              <input
                type="checkbox"
                checked={selectedCuisines.includes(cuisine)}
                onChange={() => handleCuisineToggle(cuisine)}
                disabled={isLoading}
                className="rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span className="text-sm">{cuisine}</span>
            </label>
          ))}
        </div>
        <p className="text-sm text-muted-foreground">
          Select multiple cuisines you prefer
        </p>
      </div>

      {/* Rating Slider */}
      <div className="space-y-2">
        <Label htmlFor="rating">Minimum Rating: {minRating.toFixed(1)}</Label>
        <Slider
          id="rating"
          min="0"
          max="5"
          step="0.1"
          value={minRating}
          onChange={(e) => setMinRating(Number(e.target.value))}
          disabled={isLoading}
        />
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>0</span>
          <span>5</span>
        </div>
      </div>

      {/* Additional Preferences */}
      <div className="space-y-2">
        <Label htmlFor="preferences">Additional Preferences (Optional)</Label>
        <Textarea
          id="preferences"
          placeholder="e.g., family-friendly, outdoor seating, live music..."
          value={additionalPreferences}
          onChange={(e) => setAdditionalPreferences(e.target.value)}
          disabled={isLoading}
          rows={3}
        />
      </div>

      {/* Submit Button */}
      <Button
        type="submit"
        className="w-full"
        disabled={isLoading || loadingOptions}
      >
        {isLoading ? 'Getting Recommendations...' : 'Get Recommendations'}
      </Button>
    </form>
  );
};
