"""
Main FastAPI Application
Phase 2: Backend API Development
Zomato Restaurant Recommendation System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from data_service import DataService
from recommendation_service import RecommendationService
from models import (
    RecommendationRequest,
    RecommendationResponse,
    LocationResponse,
    CuisineResponse,
    HealthResponse
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global services
data_service = None
recommendation_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global data_service, recommendation_service
    
    # Startup
    logger.info("Starting up application...")
    try:
        # Initialize data service
        data_path = Path('../phase1_data_layer/processed_data/zomato_restaurants_processed.csv')
        if not data_path.exists():
            logger.warning(f"Processed data not found at {data_path}")
            logger.warning("Please run Phase 1 preprocessing first")
            data_service = DataService()
        else:
            data_service = DataService(data_path=str(data_path))
            logger.info("Data service initialized successfully")
        
        # Initialize recommendation service
        recommendation_service = RecommendationService(data_service=data_service)
        logger.info("Recommendation service initialized successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title="Zomato Restaurant Recommendation API",
    description="AI-powered restaurant recommendation system using LLM",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "Zomato Restaurant Recommendation API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    data_status = "operational" if data_service and data_service.is_loaded else "not_loaded"
    llm_status = "operational" if recommendation_service else "not_initialized"
    
    return HealthResponse(
        status="healthy",
        data_service=data_status,
        llm_service=llm_status
    )


@app.get("/locations", response_model=LocationResponse)
async def get_locations():
    """Get all available cities/locations"""
    if not data_service or not data_service.is_loaded:
        raise HTTPException(status_code=503, detail="Data service not available")
    
    try:
        locations = data_service.get_available_locations()
        return LocationResponse(locations=locations)
    except Exception as e:
        logger.error(f"Error fetching locations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cuisines", response_model=CuisineResponse)
async def get_cuisines():
    """Get all available cuisines"""
    if not data_service or not data_service.is_loaded:
        raise HTTPException(status_code=503, detail="Data service not available")
    
    try:
        cuisines = data_service.get_available_cuisines()
        return CuisineResponse(cuisines=cuisines)
    except Exception as e:
        logger.error(f"Error fetching cuisines: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get restaurant recommendations based on user preferences"""
    if not data_service or not data_service.is_loaded:
        raise HTTPException(status_code=503, detail="Data service not available")
    
    if not recommendation_service:
        raise HTTPException(status_code=503, detail="Recommendation service not available")
    
    try:
        logger.info(f"Received recommendation request: {request}")
        recommendations = await recommendation_service.generate_recommendations(request)
        return recommendations
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
