# Data Schema Documentation

## Overview
This document describes the schema and structure of the processed Zomato restaurant dataset after Phase 1 preprocessing.

## Data Source
- **Dataset**: ManikaSaini/zomato-restaurant-recommendation
- **Source**: Hugging Face
- **Original Format**: Hugging Face Dataset

## Processed Data Schema

### Core Fields

| Field Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| `name` | string | Restaurant name | "Paradise Hotel" |
| `location` | string | Full location/area | "Hyderabad, Banjara Hills" |
| `city` | string | Extracted city name | "Hyderabad" |
| `cuisines` | string | Cuisines as comma-separated string | "North Indian, Biryani, Chinese" |
| `cuisine_list` | array | Cuisines as list of strings | ["North Indian", "Biryani", "Chinese"] |
| `cost` | float | Cost for two people (in INR) | 800.0 |
| `rating` | float | Restaurant rating (0-5 scale) | 4.2 |

### Derived Fields

| Field Name | Data Type | Description | Values |
|------------|-----------|-------------|--------|
| `budget_category` | category | Budget classification | "Low", "Medium", "High" |
| `rating_category` | category | Rating classification | "Poor", "Good", "Excellent" |
| `cuisine_count` | integer | Number of cuisine types offered | 1-10+ |

## Field Details

### name
- **Type**: String
- **Constraints**: Non-null, trimmed whitespace
- **Description**: Official name of the restaurant
- **Usage**: Display name in recommendations

### location
- **Type**: String
- **Constraints**: Non-null, title case
- **Description**: Full location including area/neighborhood
- **Usage**: Location-based filtering and display

### city
- **Type**: String
- **Constraints**: Non-null, standardized city name
- **Description**: Extracted city from location field
- **Possible Values**: Delhi, Mumbai, Bangalore, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad, Jaipur, Lucknow, etc.
- **Usage**: Primary location filter

### cuisines
- **Type**: String
- **Constraints**: Non-null, comma-separated
- **Description**: All cuisine types offered by restaurant
- **Usage**: Display purposes

### cuisine_list
- **Type**: Array of strings
- **Constraints**: Non-empty array, title case
- **Description**: Parsed list of cuisine types
- **Usage**: Cuisine filtering and matching
- **Example**: ["North Indian", "Biryani", "Chinese"]

### cost
- **Type**: Float
- **Constraints**: Non-null, positive value
- **Description**: Average cost for two people in INR
- **Range**: Typically ₹100 - ₹5000+
- **Usage**: Budget filtering
- **Note**: Currency symbols and commas removed during preprocessing

### rating
- **Type**: Float
- **Constraints**: Non-null, 0.0 - 5.0
- **Description**: Restaurant rating on 5-point scale
- **Range**: 0.0 - 5.0
- **Usage**: Quality filtering and sorting
- **Note**: Extracted from string format (e.g., "4.5/5" → 4.5)

### budget_category
- **Type**: Categorical
- **Values**: 
  - "Low": Cost < ₹300
  - "Medium": ₹300 ≤ Cost ≤ ₹700
  - "High": Cost > ₹700
- **Usage**: Quick budget filtering

### rating_category
- **Type**: Categorical
- **Values**:
  - "Poor": Rating < 3.0
  - "Good": 3.0 ≤ Rating < 4.0
  - "Excellent": Rating ≥ 4.0
- **Usage**: Quick quality filtering

### cuisine_count
- **Type**: Integer
- **Range**: 1 - 10+
- **Description**: Number of different cuisine types
- **Usage**: Diversity analysis

## Data Quality Metrics

### Preprocessing Steps Applied
1. **Duplicate Removal**: Removed exact duplicate records
2. **Missing Value Handling**: Dropped records with missing critical fields
3. **Normalization**: 
   - Column names converted to lowercase
   - Whitespace trimmed from string fields
   - Cost values converted to numeric (removed ₹ and commas)
   - Rating values extracted and converted to numeric
4. **Standardization**: 
   - City names standardized
   - Cuisine names title-cased
   - Location names title-cased

### Data Statistics
- **Total Records**: [Generated after preprocessing]
- **Unique Locations**: [Generated after preprocessing]
- **Unique Cities**: [Generated after preprocessing]
- **Unique Cuisines**: [Generated after preprocessing]
- **Cost Range**: [Generated after preprocessing]
- **Rating Range**: [Generated after preprocessing]

## Indexing Strategy

### Recommended Indexes for Query Performance
1. **City Index**: For location-based filtering
2. **Cost Index**: For budget range queries
3. **Rating Index**: For quality filtering
4. **Cuisine Index**: For cuisine-based matching
5. **Composite Index**: (city, cost, rating) for common query patterns

## File Formats

### Output Files
1. **CSV**: `zomato_restaurants_processed.csv`
   - Format: Comma-separated values
   - Encoding: UTF-8
   - Usage: Easy import into databases and analysis tools

2. **JSON**: `zomato_restaurants_processed.json`
   - Format: JSON array of objects
   - Encoding: UTF-8
   - Usage: API responses and web applications

3. **Schema**: `data_schema.json`
   - Format: JSON
   - Content: Column names, data types, sample record
   - Usage: Schema validation and documentation

4. **Statistics**: `data_statistics.json`
   - Format: JSON
   - Content: Data quality metrics and statistics
   - Usage: Monitoring and validation

## Usage Examples

### Python Example
```python
import pandas as pd

# Load processed data
df = pd.read_csv('processed_data/zomato_restaurants_processed.csv')

# Filter by city
bangalore_restaurants = df[df['city'] == 'Bangalore']

# Filter by budget
budget_restaurants = df[df['cost'] <= 500]

# Filter by rating
high_rated = df[df['rating'] >= 4.0]

# Filter by cuisine
north_indian = df[df['cuisines'].str.contains('North Indian', case=False)]
```

### API Integration Example
```python
import json

# Load JSON data
with open('processed_data/zomato_restaurants_processed.json', 'r') as f:
    restaurants = json.load(f)

# Filter restaurants
filtered = [
    r for r in restaurants 
    if r['city'] == 'Delhi' 
    and r['cost'] <= 1000 
    and r['rating'] >= 4.0
]
```

## Notes
- All currency values are in Indian Rupees (INR)
- Ratings are on a 5-point scale
- Location data may include neighborhood/area information
- Cuisine names are standardized to title case
- Some restaurants may have multiple cuisine types

## Future Enhancements
- Add geolocation coordinates (latitude/longitude)
- Include restaurant operating hours
- Add restaurant contact information
- Include image URLs
- Add review count and sentiment scores
