# Phase 1: Data Layer Foundation

## Overview
This folder contains the implementation of Phase 1 for the AI-Powered Restaurant Recommendation System. Phase 1 focuses on establishing a robust data infrastructure by acquiring, preprocessing, and preparing the Zomato restaurant dataset for use in the recommendation system.

## Deliverables

### 1. Data Preprocessing Script
- **File**: `preprocess_data.py`
- **Purpose**: Downloads, cleans, and preprocesses the Zomato dataset from Hugging Face
- **Features**:
  - Automatic dataset download from Hugging Face
  - Data cleaning (remove duplicates, handle missing values)
  - Data normalization (cost, rating, location names)
  - Derived feature generation (budget categories, rating categories)
  - Multiple output formats (CSV, JSON)

### 2. Data Schema Documentation
- **File**: `DATA_SCHEMA.md`
- **Purpose**: Comprehensive documentation of the processed data structure
- **Contents**:
  - Field descriptions and data types
  - Data quality metrics
  - Indexing strategy recommendations
  - Usage examples

### 3. Data Exploration Notebook
- **File**: `data_exploration.ipynb`
- **Purpose**: Interactive exploration and analysis of the processed dataset
- **Analyses**:
  - Dataset overview and statistics
  - Location/city distribution
  - Cost and rating distributions
  - Cuisine analysis
  - Correlation analysis
  - Sample query demonstrations

### 4. Dependencies
- **File**: `requirements.txt`
- **Purpose**: Python package dependencies for Phase 1
- **Key Packages**:
  - pandas (data processing)
  - numpy (numerical operations)
  - datasets (Hugging Face dataset loading)
  - matplotlib & seaborn (visualization)

### 5. Processed Data Output
- **Directory**: `processed_data/` (created after running preprocessing script)
- **Files**:
  - `zomato_restaurants_processed.csv` - CSV format
  - `zomato_restaurants_processed.json` - JSON format
  - `data_schema.json` - Schema metadata
  - `data_statistics.json` - Data quality statistics

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Internet connection (for downloading dataset)

### Installation

1. **Navigate to the Phase 1 directory**:
   ```bash
   cd phase1_data_layer
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

## Usage

### Running the Preprocessing Script

Execute the preprocessing pipeline:

```bash
python preprocess_data.py
```

This will:
1. Download the Zomato dataset from Hugging Face
2. Clean and preprocess the data
3. Generate derived features
4. Save processed data in multiple formats
5. Generate data quality statistics

### Running the Exploration Notebook

1. **Start Jupyter**:
   ```bash
   jupyter notebook data_exploration.ipynb
   ```

2. **Run cells sequentially** to explore the dataset

## Data Processing Pipeline

### Step 1: Dataset Acquisition
- Downloads `ManikaSaini/zomato-restaurant-recommendation` from Hugging Face
- Verifies data integrity

### Step 2: Data Cleaning
- Removes duplicate records
- Handles missing values in critical fields
- Drops records with invalid data

### Step 3: Data Normalization
- Standardizes column names (lowercase)
- Normalizes cost values (removes currency symbols, converts to numeric)
- Extracts numeric ratings from string format
- Standardizes location and city names
- Title-cases cuisine names

### Step 4: Feature Engineering
- Creates `budget_category` (Low/Medium/High)
- Creates `rating_category` (Poor/Good/Excellent)
- Parses cuisines into `cuisine_list` array
- Calculates `cuisine_count`

### Step 5: Data Export
- Saves processed data as CSV
- Saves processed data as JSON
- Generates schema documentation
- Calculates and saves statistics

## Output Data Structure

### Core Fields
- `name`: Restaurant name
- `location`: Full location/area
- `city`: Extracted city name
- `cuisines`: Comma-separated cuisine string
- `cuisine_list`: Array of cuisine types
- `cost`: Cost for two people (INR)
- `rating`: Rating (0-5 scale)

### Derived Fields
- `budget_category`: Low/Medium/High
- `rating_category`: Poor/Good/Excellent
- `cuisine_count`: Number of cuisine types

## Success Criteria

Phase 1 is considered complete when:
- ✓ Dataset loads successfully from Hugging Face
- ✓ Data preprocessing completes without errors
- ✓ Processed data saved in CSV and JSON formats
- ✓ Data quality statistics generated
- ✓ No missing values in critical fields
- ✓ All numeric fields properly normalized
- ✓ Schema documentation complete
- ✓ Exploration notebook runs successfully

## Data Quality Metrics

After preprocessing, the dataset should have:
- **Zero missing values** in critical fields (name, location, cuisines, cost, rating)
- **No duplicate records**
- **Normalized numeric values** (cost as float, rating as float 0-5)
- **Standardized text fields** (title case, trimmed whitespace)
- **Valid city names** extracted from location

## Troubleshooting

### Issue: Dataset download fails
**Solution**: Check internet connection and Hugging Face availability

### Issue: Missing values after preprocessing
**Solution**: Review preprocessing logs to understand which records were dropped

### Issue: Memory errors with large dataset
**Solution**: Process data in chunks or increase available memory

### Issue: Jupyter notebook not found
**Solution**: Ensure jupyter is installed: `pip install jupyter`

## Next Steps

After completing Phase 1:
1. Review the processed data quality
2. Explore the data using the notebook
3. Proceed to **Phase 2: Backend API Development**
4. Use the processed data files as input for the API

## File Structure

```
phase1_data_layer/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── preprocess_data.py                 # Main preprocessing script
├── DATA_SCHEMA.md                     # Data schema documentation
├── data_exploration.ipynb            # Data exploration notebook
└── processed_data/                    # Output directory (created after running script)
    ├── zomato_restaurants_processed.csv
    ├── zomato_restaurants_processed.json
    ├── data_schema.json
    └── data_statistics.json
```

## Contact & Support

For issues or questions about Phase 1 implementation, refer to:
- Main project documentation: `../ProblemStatement.md`
- Architecture document: `../Architecture.md`
- Data schema: `DATA_SCHEMA.md`

## Version History

- **v1.0** (2026-05-16): Initial Phase 1 implementation
