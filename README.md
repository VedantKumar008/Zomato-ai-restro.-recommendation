# AI-Powered Restaurant Recommendation System

A full-stack application that combines structured restaurant data from Zomato with Large Language Model (LLM) capabilities to deliver personalized, intelligent restaurant recommendations.

## 🌟 Features

- **Smart Filtering**: Filter restaurants by location, budget, cuisine type, and ratings
- **AI-Powered Recommendations**: Leverages LLMs to generate personalized restaurant suggestions
- **Intelligent Explanations**: Provides context-aware explanations for why each restaurant matches your preferences
- **Modern UI**: Clean, responsive interface built with Next.js and Tailwind CSS
- **Real-time Processing**: Fast API responses with efficient data caching
- **Comprehensive Testing**: End-to-end, performance, and error handling tests

## 🏗️ Architecture

The project follows a phased architecture with clear separation of concerns:

### Phase 1: Data Layer
- Dataset acquisition from Hugging Face (Zomato restaurant data)
- Data preprocessing and cleaning
- Efficient data storage and indexing

### Phase 2: Backend API
- FastAPI-based REST API
- Data service layer with filtering logic
- LLM integration (supports OpenAI, Anthropic, Groq)
- Recommendation engine with prompt engineering

### Phase 3: Frontend
- Next.js 14 with TypeScript
- Tailwind CSS for styling
- Responsive design for mobile and desktop
- Real-time form validation and feedback

### Phase 4: Integration & Testing
- End-to-end testing
- Performance testing and load testing
- Error handling validation
- User acceptance testing

## 🛠️ Tech Stack

### Backend
- **Python 3.9+**
- **FastAPI** - Modern, fast web framework
- **Pandas** - Data manipulation and analysis
- **Hugging Face Datasets** - Dataset management
- **LLM Providers**: OpenAI, Anthropic, Groq
- **Pydantic** - Data validation

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **Axios** - HTTP client
- **Lucide React** - Icon library

### DevOps & Testing
- **Git** - Version control
- **pytest** - Python testing
- **ESLint** - JavaScript linting
- **GitHub Actions** - CI/CD (optional)

## 📋 Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn
- API key for LLM provider (Groq recommended - free tier available)

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd M1-Zomato
```

### 2. Backend Setup (Phase 2)

Navigate to the backend directory:

```bash
cd phase2_backend_api
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
- For Groq (recommended, free): Get API key from [console.groq.com](https://console.groq.com)
- For OpenAI: Get API key from [platform.openai.com](https://platform.openai.com)
- For Anthropic: Get API key from [console.anthropic.com](https://console.anthropic.com)

Run the backend server:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 3. Frontend Setup (Phase 3)

Navigate to the frontend directory:

```bash
cd phase3_frontend
```

Install dependencies:

```bash
npm install
```

Configure environment variables:

```bash
cp .env.example .env.local
```

Edit `.env.local` if your backend runs on a different port:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Run the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Data Preparation (Phase 1) - Optional

If you need to preprocess the data:

```bash
cd phase1_data_layer
pip install -r requirements.txt
python preprocess_data.py
```

## 📁 Project Structure

```
M1-Zomato/
├── phase1_data_layer/          # Data preprocessing and storage
│   ├── processed_data/        # Cleaned restaurant data
│   ├── preprocess_data.py     # Data preprocessing script
│   └── data_exploration.ipynb # Data analysis notebook
├── phase2_backend_api/        # FastAPI backend service
│   ├── main.py               # API entry point
│   ├── data_service.py       # Data access layer
│   ├── llm_service.py        # LLM integration
│   ├── recommendation_service.py  # Recommendation logic
│   └── prompts.py            # Prompt templates
├── phase3_frontend/          # Next.js frontend application
│   ├── src/
│   │   ├── app/             # Next.js app router
│   │   ├── components/      # React components
│   │   └── lib/             # Utility functions
│   └── package.json
├── phase4_integration_testing/  # Testing suite
│   ├── e2e_tests/           # End-to-end tests
│   ├── performance_tests/   # Load testing
│   └── error_handling_tests/ # Error scenario tests
├── Architecture.md           # Detailed architecture documentation
├── ProblemStatement.md      # Project problem statement
└── README.md               # This file
```

## 🎯 Usage

1. **Start the Backend**: Run `python main.py` in `phase2_backend_api`
2. **Start the Frontend**: Run `npm run dev` in `phase3_frontend`
3. **Open the Application**: Navigate to `http://localhost:3000`
4. **Enter Preferences**:
   - Select your location (e.g., Delhi, Bangalore, Mumbai)
   - Set your budget for two people
   - Choose cuisine types
   - Set minimum rating
   - Add any additional preferences
5. **Get Recommendations**: Click "Get Recommendations" to receive AI-powered suggestions

## 🧪 Testing

### Run All Tests

```bash
cd phase4_integration_testing
python run_all_tests.py
```

### Run Specific Test Suites

```bash
# End-to-end tests
cd e2e_tests
python test_e2e.py

# Performance tests
cd performance_tests
python load_test.py

# Error handling tests
cd error_handling_tests
python test_errors.py
```

## 🔧 Configuration

### Backend Configuration (.env)

```env
# LLM Provider (groq, openai, anthropic)
LLM_PROVIDER=groq

# Groq Configuration
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama3-70b-8192

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Data Path
DATA_PATH=../phase1_data_layer/processed_data/zomato_restaurants_processed.csv
```

### Frontend Configuration (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📊 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

- `GET /api/locations` - Get available locations
- `GET /api/cuisines` - Get available cuisine types
- `POST /api/recommend` - Get personalized recommendations

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Zomato Dataset**: [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation) on Hugging Face
- **LLM Providers**: OpenAI, Anthropic, Groq
- **FastAPI** - Modern Python web framework
- **Next.js** - React framework for production

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

## 🚧 Roadmap

- [ ] User authentication and personalization
- [ ] Map integration for location visualization
- [ ] Restaurant image gallery
- [ ] Review sentiment analysis
- [ ] Real-time availability checking
- [ ] Mobile app development

---

**Built with ❤️ using AI and modern web technologies**
