import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Restaurant {
  name: string;
  location: string;
  city: string;
  cuisines: string;
  cost: number;
  rating: number;
  explanation?: string;
}

export interface RecommendationRequest {
  location: string;
  budget: number;
  cuisines?: string[];
  min_rating?: number;
  additional_preferences?: string;
}

export interface RecommendationResponse {
  recommendations: Restaurant[];
  total_found: number;
  query_summary: {
    location: string;
    budget: number;
    cuisines?: string[];
    min_rating?: number;
  };
}

export const apiService = {
  getHealth: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  getLocations: async (): Promise<string[]> => {
    const response = await api.get('/locations');
    return response.data.locations;
  },

  getCuisines: async (): Promise<string[]> => {
    const response = await api.get('/cuisines');
    return response.data.cuisines;
  },

  getRecommendations: async (request: RecommendationRequest): Promise<RecommendationResponse> => {
    const response = await api.post('/recommend', request);
    return response.data;
  },
};
