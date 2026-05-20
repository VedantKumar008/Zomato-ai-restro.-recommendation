'use client';

import React from 'react';
import { Card, CardContent, CardHeader } from './ui/card';

export const LoadingSkeleton: React.FC = () => {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map((i) => (
        <Card key={i} className="animate-pulse">
          <CardHeader>
            <div className="h-6 bg-muted rounded w-3/4 mb-2"></div>
            <div className="h-4 bg-muted rounded w-1/2"></div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="h-5 bg-muted rounded w-1/4"></div>
            <div className="h-4 bg-muted rounded w-full"></div>
            <div className="h-4 bg-muted rounded w-3/4"></div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};
