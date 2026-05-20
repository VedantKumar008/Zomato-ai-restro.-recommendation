# Phase 2: Backend API Development

## Overview
This folder contains the implementation of Phase 2 for the AI-Powered Restaurant Recommendation System. Phase 2 focuses on building the core backend services including a RESTful API, data access layer, LLM integration, and recommendation engine.

## Deliverables

### 1. FastAPI Application
- **File**: `main.py`
- **Purpose**: Main FastAPI application with all endpoints
- **Endpoints**:
  - `GET /` - Root endpoint with API info
  - `GET /health` - Health check endpoint
  - `GET /locations` - Get available cities/locations
  - `GET /cuisines` - Get available cuisines
  - `POST /recommend` - Get restaurant recommendations

### 2. Data Models
- **File**: `models.py`
- **Purpose**: Pydantic models for request/response validation
- **Models**:
  - `RecommendationRequest` - User preference input
  - `RecommendationResponse` - Recommendation output
  - `Restaurant` - Restaurant data model
  - `LocationResponse` - Available locations
  - `CuisineResponse` - Available cuisines
  - `HealthResponse` - Health check status

### 3. Data Service Layer
- **File**: `data_service.py`
- **Purpose**: Data access and filtering logic
- **Features**:
  - Load processed data from Phase 1
  - Filter restaurants by location, budget, cuisine, rating
  - Get available locations and cuisines
  - Dataset statistics

### 4. LLM Integration
- **File**: `llm_service.py`
- **Purpose**: Integration with Large Language Models
- **Providers**:
  - OpenAI (GPT-3.5/GPT-4)
  - Anthropic (Claude)
  - Fallback to mock recommendations when unavailable
- **Features**:
  - Configurable provider selection
  - Error handling and retry logic
  - Response parsing and validation

### 5. Recommendation Service
- **File**: `recommendation_service.py`
- **Purpose**: Orchestrate data filtering and LLM-based recommendations
- **Features**:
  - Filter restaurants based on user preferences
  - Generate personalized explanations using LLM
  - Rank and return top recommendations
  - Fallback to basic recommendations when LLM unavailable

### 6. Prompt Templates
- **File**: `prompts.py`
- **Purpose**: LLM prompt templates for recommendation generation
- **Templates**:
  - Main recommendation prompt
  - Few-shot examples
  - System prompt

### 7. Configuration
- **File**: `.env.example`
- **Purpose**: Environment configuration template
- **Settings**:
  - LLM provider selection
  - API keys for OpenAI/Anthropic
  - API host and port
  - Data path configuration
  - Logging level

### 8. Dependencies
- **File**: `requirements.txt`
- **Purpose**: Python package dependencies
- **Key Packages**:
  - FastAPI (web framework)
  - Pydantic (data validation)
  - Pandas (data processing)
  - OpenAI/Anthropic (LLM integration)

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Completed Phase 1 (processed data available)
- OpenAI API key or Anthropic API key (optional, for LLM features)

### Installation

1. **Navigate to the Phase 2 directory**:
   ```bash
   cd phase2_backend_api
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your API keys
   # For Groq (recommended - fast and free):
   GROQ_API_KEY=your_actual_groq_api_key_here
   
   # For OpenAI:
   OPENAI_API_KEY=your_actual_api_key_here
   
   # For Anthropic (alternative):
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

5. **Ensure Phase 1 data is available**:
   The API expects processed data from Phase 1 at:
   ```
   ../phase1_data_layer/processed_data/zomato_restaurants_processed.csv
   ```
   
   If the data is in a different location, update the `DATA_PATH` in your `.env` file.

## Usage

### Running the API

Start the FastAPI server:

```bash
# Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Testing Endpoints

#### 1. Health Check
```bash
curl http://localhost:8000/health
```

#### 2. Get Available Locations
```bash
curl http://localhost:8000/locations
```

#### 3. Get Available Cuisines
```bash
curl http://localhost:8000/cuisines
```

#### 4. Get Recommendations
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Bangalore",
    "budget": 1000,
    "cuisines": ["North Indian", "Chinese"],
    "min_rating": 4.0,
    "additional_preferences": "family-friendly"
  }'
```

## API Response Format

### Recommendation Response
```json
{
  "recommendations": [
    {
      "name": "Paradise Hotel",
      "location": "Bangalore, Indiranagar",
      "city": "Bangalore",
      "cuisines": "North Indian, Biryani",
      "cost": 800.0,
      "rating": 4.5,
      "explanation": "Paradise Hotel is an excellent choice for your North Indian cuisine preference..."
    }
  ],
  "total_found": 15,
  "query_summary": {
    "location": "Bangalore",
    "budget": 1000,
    "cuisines": ["North Indian", "Chinese"],
    "min_rating": 4.0,
    "additional_preferences": "family-friendly"
  }
}
```

## Architecture

### Service Layer Architecture
```
main.py (FastAPI Application)
    ↓
recommendation_service.py (Recommendation Logic)
    ↓
    ├── data_service.py (Data Access & Filtering)
    └── llm_service.py (LLM Integration)
        ↓
    ├── Groq Provider (Recommended)
    ├── OpenAI Provider
    └── Anthropic Provider
```

### Data Flow
1. User sends recommendation request via API
2. Recommendation service validates request
3. Data service filters restaurants based on criteria
4. LLM service generates personalized explanations
5. Recommendations are ranked and returned to user

## LLM Integration

### Supported Providers

#### Groq (Recommended)
- Models: Llama3-70b-8192, Llama3-8b-8192, Mixtral-8x7b-32768
- Set `LLM_PROVIDER=groq` in `.env`
- Requires `GROQ_API_KEY`
- **Benefits**: Fast inference, free tier available, OpenAI-compatible API

#### OpenAI
- Models: GPT-3.5-turbo, GPT-4
- Set `LLM_PROVIDER=openai` in `.env`
- Requires `OPENAI_API_KEY`

#### Anthropic
- Models: Claude 3 Sonnet, Claude 3 Opus
- Set `LLM_PROVIDER=anthropic` in `.env`
- Requires `ANTHROPIC_API_KEY`

### Fallback Behavior
If LLM API is unavailable or fails, the system automatically falls back to generating basic recommendations without LLM-powered explanations. This ensures the API remains functional even without LLM access.

## Success Criteria

Phase 2 is considered complete when:
- ✓ API starts successfully without errors
- ✓ All endpoints respond correctly
- ✓ Data service loads Phase 1 processed data
- ✓ Restaurant filtering works correctly
- ✓ LLM integration produces valid recommendations (when API key provided)
- ✓ Fallback recommendations work without LLM
- ✓ Response time < 5 seconds for typical queries
- ✓ Error handling covers edge cases
- ✓ API documentation accessible via Swagger UI

## Troubleshooting

### Issue: API fails to start
**Solution**: Check that Phase 1 data is available at the configured path

### Issue: LLM recommendations fail
**Solution**: Verify API key is correctly set in `.env` file

### Issue: No restaurants found
**Solution**: Check that your filter criteria are not too restrictive

### Issue: Import errors
**Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

### Issue: CORS errors in frontend
**Solution**: Update CORS middleware configuration in `main.py`

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LLM_PROVIDER` | LLM provider to use (groq, openai, anthropic) | `groq` | No |
| `GROQ_API_KEY` | Groq API key | - | Yes (for Groq) |
| `GROQ_MODEL` | Groq model name | `llama3-70b-8192` | No |
| `OPENAI_API_KEY` | OpenAI API key | - | Yes (for OpenAI) |
| `OPENAI_MODEL` | OpenAI model name | `gpt-3.5-turbo` | No |
| `ANTHROPIC_API_KEY` | Anthropic API key | - | Yes (for Anthropic) |
| `ANTHROPIC_MODEL` | Anthropic model name | `claude-3-sonnet-20240229` | No |
| `API_HOST` | API host address | `0.0.0.0` | No |
| `API_PORT` | API port | `8000` | No |
| `DATA_PATH` | Path to processed data | `../phase1_data_layer/processed_data/zomato_restaurants_processed.csv` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |

## Next Steps

After completing Phase 2:
1. Test all API endpoints thoroughly
2. Verify LLM integration with your API key
3. Proceed to **Phase 3: Frontend Development**
4. Use the API endpoints to build the user interface

## File Structure

```
phase2_backend_api/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment configuration template
├── main.py                            # FastAPI application
├── models.py                          # Pydantic models
├── data_service.py                    # Data access layer
├── llm_service.py                     # LLM integration
├── recommendation_service.py          # Recommendation logic
└── prompts.py                         # LLM prompt templates
```

## Contact & Support

For issues or questions about Phase 2 implementation, refer to:
- Main project documentation: `../ProblemStatement.md`
- Architecture document: `../Architecture.md`
- Phase 1 documentation: `../phase1_data_layer/README.md`

## Version History

- **v1.0** (2026-05-16): Initial Phase 2 implementation
