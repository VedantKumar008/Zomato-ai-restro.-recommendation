"""
Main FastAPI Application
Phase 2: Backend API Development
Zomato Restaurant Recommendation System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import traceback
import os
import requests
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
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Script location: {__file__}")
    
    try:
        # Initialize data service with robust absolute path
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        # Navigate to the processed data file relative to the script
        # Use memory-optimized deployment dataset for Render free-tier
        data_path = script_dir.parent / 'phase1_data_layer' / 'processed_data' / 'zomato_restaurants_deployment.csv'
        
        logger.info("=" * 60)
        logger.info("DATASET CONFIGURATION")
        logger.info("=" * 60)
        logger.info(f"Expected dataset filename: zomato_restaurants_deployment.csv")
        logger.info(f"Resolved data path: {data_path}")
        logger.info(f"Absolute data path: {data_path.absolute()}")
        logger.info(f"Data file exists: {data_path.exists()}")
        logger.info(f"Data file extension: {data_path.suffix}")
        if data_path.suffix == '.csv':
            logger.info("✅ Configured to use memory-optimized deployment dataset (0.95 MB for Render free tier)")
        logger.info("=" * 60)
        
        if not data_path.exists():
            logger.warning(f"Processed data not found at {data_path.absolute()}")
            logger.warning(f"Checked path: {data_path}")
            
            # Try to download from external URL if provided (for Render deployment)
            dataset_url = os.getenv("DATASET_URL")
            if dataset_url:
                logger.info(f"Attempting to download dataset from: {dataset_url}")
                try:
                    # Ensure the directory exists
                    data_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    logger.info(f"Downloading dataset (this may take a while for large files)...")
                    response = requests.get(dataset_url, stream=True)
                    response.raise_for_status()
                    
                    with open(data_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    logger.info(f"Dataset downloaded successfully to: {data_path.absolute()}")
                except Exception as download_error:
                    logger.error(f"Failed to download dataset: {download_error}")
                    logger.error(f"Download error traceback: {traceback.format_exc()}")
                    logger.error("DATASET_URL environment variable may be invalid or inaccessible")
            
            # If still not available, try to use sample data
            if not data_path.exists():
                logger.warning("Dataset file still not available after download attempt")
                logger.warning("Initializing data service without dataset (endpoints will return empty data)")
                data_service = DataService()
            else:
                logger.info(f"Loading data from: {data_path.absolute()}")
                data_service = DataService(data_path=str(data_path.absolute()))
                logger.info(f"Data service initialized successfully, is_loaded: {data_service.is_loaded}")
        else:
            logger.info(f"Loading data from: {data_path.absolute()}")
            data_service = DataService(data_path=str(data_path.absolute()))
            logger.info(f"Data service initialized successfully, is_loaded: {data_service.is_loaded}")
        
        # Initialize recommendation service
        recommendation_service = RecommendationService(data_service=data_service)
        logger.info("Recommendation service initialized successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
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
    # Log debugging information
    logger.info(f"=== /locations endpoint called ===")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Data service exists: {data_service is not None}")
    if data_service:
        logger.info(f"Data service is_loaded: {data_service.is_loaded}")
        logger.info(f"Data service data_path: {data_service.data_path}")
        if data_service.data_path:
            logger.info(f"Data file exists: {Path(data_service.data_path).exists()}")
    
    if not data_service or not data_service.is_loaded:
        error_msg = "Data service not available"
        logger.error(error_msg)
        logger.error(f"data_service is None: {data_service is None}")
        logger.error(f"data_service.is_loaded: {data_service.is_loaded if data_service else 'N/A'}")
        traceback.print_exc()
        raise HTTPException(status_code=503, detail=error_msg)
    
    try:
        locations = data_service.get_available_locations()
        return LocationResponse(locations=locations)
    except Exception as e:
        logger.error(f"Error fetching locations: {e}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/cuisines", response_model=CuisineResponse)
async def get_cuisines():
    """Get all available cuisines"""
    # Log debugging information
    logger.info(f"=== /cuisines endpoint called ===")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Data service exists: {data_service is not None}")
    if data_service:
        logger.info(f"Data service is_loaded: {data_service.is_loaded}")
        logger.info(f"Data service data_path: {data_service.data_path}")
        if data_service.data_path:
            logger.info(f"Data file exists: {Path(data_service.data_path).exists()}")
    
    if not data_service or not data_service.is_loaded:
        error_msg = "Data service not available"
        logger.error(error_msg)
        logger.error(f"data_service is None: {data_service is None}")
        logger.error(f"data_service.is_loaded: {data_service.is_loaded if data_service else 'N/A'}")
        traceback.print_exc()
        raise HTTPException(status_code=503, detail=error_msg)
    
    try:
        cuisines = data_service.get_available_cuisines()
        return CuisineResponse(cuisines=cuisines)
    except Exception as e:
        logger.error(f"Error fetching cuisines: {e}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


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
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
