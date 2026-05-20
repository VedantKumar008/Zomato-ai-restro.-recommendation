"""
Pydantic Models for API
Phase 2: Backend API Development
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum


class RecommendationRequest(BaseModel):
    """Request model for restaurant recommendations"""
    location: str = Field(..., description="City or location (e.g., Delhi, Bangalore)")
    budget: float = Field(..., gt=0, description="Maximum cost for two people in INR")
    cuisines: Optional[List[str]] = Field(None, description="List of preferred cuisines")
    min_rating: float = Field(default=0.0, ge=0, le=5, description="Minimum rating (0-5)")
    additional_preferences: Optional[str] = Field(None, description="Additional preferences (e.g., family-friendly)")
    
    @validator('location')
    def location_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Location cannot be empty')
        return v.strip()
    
    @validator('cuisines')
    def validate_cuisines(cls, v):
        if v is not None:
            if len(v) == 0:
                return None
            # Remove empty strings and strip whitespace
            return [c.strip() for c in v if c.strip()]
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "location": "Bangalore",
                "budget": 1000,
                "cuisines": ["North Indian", "Chinese"],
                "min_rating": 4.0,
                "additional_preferences": "family-friendly"
            }
        }


class Restaurant(BaseModel):
    """Restaurant model"""
    name: str
    location: str
    city: str
    cuisines: str
    cost: float
    rating: float
    explanation: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Paradise Hotel",
                "location": "Hyderabad, Banjara Hills",
                "city": "Hyderabad",
                "cuisines": "North Indian, Biryani",
                "cost": 800.0,
                "rating": 4.2,
                "explanation": "Great for families with excellent biryani"
            }
        }


class RecommendationResponse(BaseModel):
    """Response model for recommendations"""
    recommendations: List[Restaurant]
    total_found: int
    query_summary: Dict[str, Any]
    
    class Config:
        schema_extra = {
            "example": {
                "recommendations": [
                    {
                        "name": "Paradise Hotel",
                        "location": "Hyderabad, Banjara Hills",
                        "city": "Hyderabad",
                        "cuisines": "North Indian, Biryani",
                        "cost": 800.0,
                        "rating": 4.2,
                        "explanation": "Excellent biryani with great ambiance"
                    }
                ],
                "total_found": 15,
                "query_summary": {
                    "location": "Hyderabad",
                    "budget": 1000,
                    "cuisines": ["North Indian"],
                    "min_rating": 4.0
                }
            }
        }


class LocationResponse(BaseModel):
    """Response model for locations"""
    locations: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "locations": ["Delhi", "Mumbai", "Bangalore", "Hyderabad"]
            }
        }


class CuisineResponse(BaseModel):
    """Response model for cuisines"""
    cuisines: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "cuisines": ["North Indian", "Chinese", "Italian", "South Indian"]
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    data_service: str
    llm_service: str
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "data_service": "operational",
                "llm_service": "operational"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
    error_code: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "Data service not available",
                "error_code": "SERVICE_UNAVAILABLE"
            }
        }
