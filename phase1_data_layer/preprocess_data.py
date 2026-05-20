"""
Data Preprocessing Script for Zomato Restaurant Recommendation System
Phase 1: Data Layer Foundation
"""

import pandas as pd
import numpy as np
from datasets import load_dataset
import json
import re
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ZomatoDataPreprocessor:
    """Handle data preprocessing for Zomato restaurant dataset"""
    
    def __init__(self, output_dir='./processed_data'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dataset = None
        self.df = None
        
    def load_dataset(self):
        """Load dataset from Hugging Face"""
        logger.info("Loading Zomato dataset from Hugging Face...")
        try:
            self.dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
            logger.info("Dataset loaded successfully")
            logger.info(f"Dataset info: {self.dataset}")
            return True
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return False
    
    def convert_to_dataframe(self):
        """Convert dataset to pandas DataFrame"""
        logger.info("Converting dataset to DataFrame...")
        try:
            # Convert train split to DataFrame
            self.df = pd.DataFrame(self.dataset['train'])
            logger.info(f"DataFrame shape: {self.df.shape}")
            logger.info(f"Columns: {self.df.columns.tolist()}")
            return True
        except Exception as e:
            logger.error(f"Error converting to DataFrame: {e}")
            return False
    
    def analyze_data_quality(self):
        """Analyze data quality and log statistics"""
        logger.info("\n=== Data Quality Analysis ===")
        logger.info(f"Total records: {len(self.df)}")
        logger.info(f"Total columns: {len(self.df.columns)}")
        
        # Missing values
        missing = self.df.isnull().sum()
        logger.info("\nMissing values per column:")
        for col, count in missing.items():
            if count > 0:
                logger.info(f"  {col}: {count} ({count/len(self.df)*100:.2f}%)")
        
        # Data types
        logger.info("\nData types:")
        logger.info(self.df.dtypes)
        
        # Basic statistics for numeric columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            logger.info("\nNumeric columns statistics:")
            logger.info(self.df[numeric_cols].describe())
        
        # Unique values for categorical columns
        categorical_cols = self.df.select_dtypes(include=['object', 'string']).columns
        logger.info("\nUnique values in categorical columns:")
        for col in categorical_cols:
            unique_count = self.df[col].nunique()
            logger.info(f"  {col}: {unique_count} unique values")
        
        return True
    
    def clean_data(self):
        """Clean and preprocess the data"""
        logger.info("\n=== Starting Data Cleaning ===")
        
        original_count = len(self.df)
        
        # 1. Remove duplicates
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            logger.info(f"Removing {duplicates} duplicate records...")
            self.df = self.df.drop_duplicates()
        
        # 2. Handle missing values
        logger.info("Handling missing values...")
        
        # For critical columns, drop rows with missing values
        critical_cols = ['name', 'location', 'cuisines', 'cost', 'rating']
        available_critical_cols = [col for col in critical_cols if col in self.df.columns]
        
        if available_critical_cols:
            before_drop = len(self.df)
            self.df = self.df.dropna(subset=available_critical_cols)
            dropped = before_drop - len(self.df)
            if dropped > 0:
                logger.info(f"Dropped {dropped} rows with missing critical values")
        
        # 3. Normalize column names
        logger.info("Normalizing column names...")
        self.df.columns = self.df.columns.str.lower().str.strip()
        
        # Rename columns to standard names
        column_mapping = {
            'rate': 'rating',
            'approx_cost(for two people)': 'cost'
        }
        self.df = self.df.rename(columns=column_mapping)
        
        # 4. Clean and normalize specific columns
        if 'cuisines' in self.df.columns:
            self.df['cuisines'] = self.df['cuisines'].str.strip()
            # Split cuisines into list for easier filtering
            self.df['cuisine_list'] = self.df['cuisines'].str.split(', ')
            self.df['cuisine_list'] = self.df['cuisine_list'].apply(
                lambda x: [c.strip().title() for c in x] if isinstance(x, list) else []
            )
        
        if 'location' in self.df.columns:
            self.df['location'] = self.df['location'].str.strip().str.title()
        
        if 'name' in self.df.columns:
            self.df['name'] = self.df['name'].str.strip()
        
        # 5. Normalize cost values
        if 'cost' in self.df.columns:
            logger.info("Normalizing cost values...")
            # Remove any currency symbols and commas
            self.df['cost'] = self.df['cost'].astype(str).str.replace('₹', '', regex=False)
            self.df['cost'] = self.df['cost'].str.replace(',', '', regex=False)
            self.df['cost'] = pd.to_numeric(self.df['cost'], errors='coerce')
            # Drop rows with invalid cost
            self.df = self.df.dropna(subset=['cost'])
            self.df['cost'] = self.df['cost'].astype(float)
        
        # 6. Normalize rating values
        if 'rating' in self.df.columns:
            logger.info("Normalizing rating values...")
            # Extract numeric rating from string (e.g., "4.5/5" -> 4.5)
            self.df['rating'] = self.df['rating'].astype(str).str.extract(r'(\d+\.?\d*)')
            self.df['rating'] = pd.to_numeric(self.df['rating'], errors='coerce')
            # Drop rows with invalid rating
            self.df = self.df.dropna(subset=['rating'])
            # Ensure rating is between 0 and 5
            self.df['rating'] = self.df['rating'].clip(0, 5)
        
        # 7. Standardize location names (city extraction)
        if 'location' in self.df.columns:
            logger.info("Standardizing location names...")
            # Extract city from location (assuming format like "City, Area" or just "City")
            self.df['city'] = self.df['location'].apply(self._extract_city)
        
        final_count = len(self.df)
        logger.info(f"\nData cleaning complete. Records: {original_count} -> {final_count}")
        
        return True
    
    def _extract_city(self, location):
        """Extract city name from location string"""
        if pd.isna(location):
            return "Unknown"
        
        location = str(location).strip()
        
        # Common city names in India
        major_cities = [
            'Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 
            'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'
        ]
        
        # Check if location contains a major city
        for city in major_cities:
            if city.lower() in location.lower():
                return city
        
        # If no major city found, use the first part before comma
        if ',' in location:
            return location.split(',')[0].strip()
        
        return location
    
    def add_derived_features(self):
        """Add derived features for better filtering"""
        logger.info("\n=== Adding Derived Features ===")
        
        # Budget category based on cost
        if 'cost' in self.df.columns:
            self.df['budget_category'] = pd.cut(
                self.df['cost'],
                bins=[0, 300, 700, float('inf')],
                labels=['Low', 'Medium', 'High']
            )
            logger.info("Added budget_category feature")
        
        # Rating category
        if 'rating' in self.df.columns:
            self.df['rating_category'] = pd.cut(
                self.df['rating'],
                bins=[0, 3, 4, 5],
                labels=['Poor', 'Good', 'Excellent']
            )
            logger.info("Added rating_category feature")
        
        # Cuisine count
        if 'cuisine_list' in self.df.columns:
            self.df['cuisine_count'] = self.df['cuisine_list'].apply(len)
            logger.info("Added cuisine_count feature")
        
        return True
    
    def save_processed_data(self):
        """Save processed data in multiple formats"""
        logger.info("\n=== Saving Processed Data ===")
        
        # Save as CSV
        csv_path = self.output_dir / 'zomato_restaurants_processed.csv'
        self.df.to_csv(csv_path, index=False)
        logger.info(f"Saved CSV to: {csv_path}")
        
        # Save as JSON
        json_path = self.output_dir / 'zomato_restaurants_processed.json'
        self.df.to_json(json_path, orient='records', indent=2)
        logger.info(f"Saved JSON to: {json_path}")
        
        # Save data schema
        schema_path = self.output_dir / 'data_schema.json'
        schema = {
            'columns': self.df.columns.tolist(),
            'dtypes': {col: str(dtype) for col, dtype in self.df.dtypes.items()},
            'shape': self.df.shape,
            'sample_record': self.df.iloc[0].to_dict()
        }
        with open(schema_path, 'w') as f:
            json.dump(schema, f, indent=2)
        logger.info(f"Saved schema to: {schema_path}")
        
        # Save statistics
        stats_path = self.output_dir / 'data_statistics.json'
        stats = {
            'total_records': len(self.df),
            'unique_locations': self.df['location'].nunique() if 'location' in self.df.columns else 0,
            'unique_cities': self.df['city'].nunique() if 'city' in self.df.columns else 0,
            'unique_cuisines': self._get_unique_cuisines(),
            'cost_range': {
                'min': float(self.df['cost'].min()) if 'cost' in self.df.columns else 0,
                'max': float(self.df['cost'].max()) if 'cost' in self.df.columns else 0,
                'mean': float(self.df['cost'].mean()) if 'cost' in self.df.columns else 0
            },
            'rating_range': {
                'min': float(self.df['rating'].min()) if 'rating' in self.df.columns else 0,
                'max': float(self.df['rating'].max()) if 'rating' in self.df.columns else 0,
                'mean': float(self.df['rating'].mean()) if 'rating' in self.df.columns else 0
            }
        }
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
        logger.info(f"Saved statistics to: {stats_path}")
        
        return True
    
    def _get_unique_cuisines(self):
        """Get list of all unique cuisines"""
        if 'cuisine_list' not in self.df.columns:
            return []
        
        all_cuisines = set()
        for cuisine_list in self.df['cuisine_list']:
            if isinstance(cuisine_list, list):
                all_cuisines.update(cuisine_list)
        
        return sorted(list(all_cuisines))
    
    def run_pipeline(self):
        """Execute the complete preprocessing pipeline"""
        logger.info("="*60)
        logger.info("Starting Zomato Data Preprocessing Pipeline")
        logger.info("="*60)
        
        steps = [
            ("Load Dataset", self.load_dataset),
            ("Convert to DataFrame", self.convert_to_dataframe),
            ("Analyze Data Quality", self.analyze_data_quality),
            ("Clean Data", self.clean_data),
            ("Add Derived Features", self.add_derived_features),
            ("Save Processed Data", self.save_processed_data)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"\n{'='*60}")
            logger.info(f"Step: {step_name}")
            logger.info(f"{'='*60}")
            try:
                if not step_func():
                    logger.error(f"Failed at step: {step_name}")
                    return False
            except Exception as e:
                logger.error(f"Error in step '{step_name}': {e}")
                import traceback
                traceback.print_exc()
                return False
        
        logger.info("\n" + "="*60)
        logger.info("Preprocessing Pipeline Completed Successfully!")
        logger.info("="*60)
        return True


def main():
    """Main execution function"""
    preprocessor = ZomatoDataPreprocessor(output_dir='./processed_data')
    success = preprocessor.run_pipeline()
    
    if success:
        logger.info("\n✓ All preprocessing steps completed successfully!")
        logger.info("✓ Processed data saved to 'processed_data' directory")
    else:
        logger.error("\n✗ Preprocessing pipeline failed!")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
