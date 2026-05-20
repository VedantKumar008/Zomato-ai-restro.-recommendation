'use client';

import React, { useState } from 'react';
import { RecommendationForm } from '@/components/RecommendationForm';
import { ResultsDisplay } from '@/components/ResultsDisplay';
import { apiService } from '@/lib/api';
import { Utensils, Sparkles } from 'lucide-react';

export default function Home() {
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [totalFound, setTotalFound] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleFormSubmit = async (formData: any) => {
    setIsLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const response = await apiService.getRecommendations(formData);
      setRecommendations(response.recommendations);
      setTotalFound(response.total_found);
    } catch (err: any) {
      console.error('Error fetching recommendations:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to fetch recommendations. Please try again.');
      setRecommendations([]);
      setTotalFound(0);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white border-b shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="bg-primary/10 p-2 rounded-lg">
              <Utensils className="h-8 w-8 text-primary" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Zomato Restaurant Recommendations
              </h1>
              <p className="text-sm text-muted-foreground">
                AI-powered personalized suggestions
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-lg p-6 border">
              <div className="flex items-center gap-2 mb-6">
                <Sparkles className="h-5 w-5 text-primary" />
                <h2 className="text-xl font-semibold">Find Your Perfect Restaurant</h2>
              </div>
              <RecommendationForm onSubmit={handleFormSubmit} isLoading={isLoading} />
            </div>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {!hasSearched ? (
              <div className="bg-white rounded-xl shadow-lg p-12 border text-center">
                <div className="bg-primary/10 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Utensils className="h-10 w-10 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Ready to Explore?</h3>
                <p className="text-muted-foreground">
                  Fill in your preferences on the left to get personalized restaurant recommendations powered by AI.
                </p>
              </div>
            ) : (
              <ResultsDisplay
                recommendations={recommendations}
                totalFound={totalFound}
                isLoading={isLoading}
                error={error}
              />
            )}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
          <p>Phase 3: Frontend Development - Zomato Restaurant Recommendation System</p>
        </div>
      </footer>
    </main>
  );
}
