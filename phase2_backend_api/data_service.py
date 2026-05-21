"""
Data Service Layer
Phase 2: Backend API Development
Handles data access and filtering logic
"""

import pandas as pd
import logging
import traceback
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import json

logger = logging.getLogger(__name__)


class DataService:
    """Service for data access and filtering"""
    
    def __init__(self, data_path: Optional[str] = None):
        self.data_path = data_path
        self.df = None
        self.is_loaded = False
        
        if data_path:
            self.load_data()
    
    def load_data(self):
        """Load processed data from CSV or compressed file"""
        logger.info(f"=== load_data called ===")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Data path: {self.data_path}")
        
        try:
            if self.data_path:
                data_file_path = Path(self.data_path)
                logger.info(f"Absolute path: {data_file_path.absolute()}")
                logger.info(f"File exists: {data_file_path.exists()}")
                
                if data_file_path.exists():
                    logger.info(f"✅ Data file found at {self.data_path}")
                    
                    # Detect compression type from file extension
                    compression = None
                    if data_file_path.suffix == '.zip':
                        compression = 'zip'
                        logger.info("✅ Detected ZIP compression, using pandas compression support")
                        logger.info("✅ Reading directly from ZIP without full extraction (memory-efficient)")
                    elif data_file_path.suffix == '.gz':
                        compression = 'gzip'
                        logger.info("Detected GZIP compression, using pandas compression support")
                    elif data_file_path.suffix == '.csv':
                        compression = None
                        logger.info("Loading uncompressed CSV file")
                    
                    # Load data with appropriate compression
                    logger.info("📊 Loading data into pandas DataFrame...")
                    self.df = pd.read_csv(self.data_path, compression=compression)
                    self.is_loaded = True
                    logger.info(f"✅ Data loaded successfully: {len(self.df)} records")
                    logger.info(f"✅ DataFrame columns: {list(self.df.columns)}")
                    logger.info(f"✅ Memory usage: {self.df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
                else:
                    logger.warning(f"Data file not found at {self.data_path}")
                    logger.warning(f"Absolute path checked: {data_file_path.absolute()}")
                    self.df = pd.DataFrame()
                    self.is_loaded = False
            else:
                logger.warning("No data path provided")
                self.df = pd.DataFrame()
                self.is_loaded = False
        except FileNotFoundError as e:
            logger.error(f"File not found error loading data: {e}")
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            traceback.print_exc()
            self.df = pd.DataFrame()
            self.is_loaded = False
        except pd.errors.EmptyDataError as e:
            logger.error(f"Empty data file error: {e}")
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            traceback.print_exc()
            self.df = pd.DataFrame()
            self.is_loaded = False
        except pd.errors.ParserError as e:
            logger.error(f"CSV parsing error: {e}")
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            traceback.print_exc()
            self.df = pd.DataFrame()
            self.is_loaded = False
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            traceback.print_exc()
            self.df = pd.DataFrame()
            self.is_loaded = False
    
    def get_available_locations(self) -> List[str]:
        """Get list of available cities/locations"""
        if not self.is_loaded or self.df is None:
            return []
        
        try:
            if 'city' in self.df.columns:
                locations = sorted(self.df['city'].unique().tolist())
                return [loc for loc in locations if pd.notna(loc) and loc != 'Unknown']
            return []
        except Exception as e:
            logger.error(f"Error getting locations: {e}")
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            return []
    
    def get_available_cuisines(self) -> List[str]:
        """Get list of available cuisines"""
        if not self.is_loaded or self.df is None:
            return []
        
        try:
            if 'cuisines' in self.df.columns:
                # Parse all cuisines from the cuisines column
                all_cuisines = set()
                for cuisine_str in self.df['cuisines'].dropna():
                    cuisines = [c.strip() for c in str(cuisine_str).split(',')]
                    all_cuisines.update(cuisines)
                
                return sorted(list(all_cuisines))
            return []
        except Exception as e:
            logger.error(f"Error getting cuisines: {e}")
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            return []
    
    def filter_restaurants(
        self,
        location: str,
        budget: float,
        cuisines: Optional[List[str]] = None,
        min_rating: float = 0.0
    ) -> pd.DataFrame:
        """
        Filter restaurants based on user criteria
        
        Args:
            location: City or location name
            budget: Maximum cost for two people
            cuisines: List of preferred cuisines (optional)
            min_rating: Minimum rating threshold
            
        Returns:
            Filtered DataFrame of restaurants
        """
        if not self.is_loaded or self.df is None:
            logger.error("Data not loaded")
            return pd.DataFrame()
        
        try:
            filtered_df = self.df.copy()
            
            # Filter by location (city)
            if 'city' in filtered_df.columns:
                # Case-insensitive partial match for city
                location_lower = location.lower()
                filtered_df = filtered_df[
                    filtered_df['city'].str.lower().str.contains(location_lower, na=False)
                ]
                logger.info(f"After location filter: {len(filtered_df)} records")
            
            # Filter by budget (cost <= budget)
            if 'cost' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['cost'] <= budget]
                logger.info(f"After budget filter: {len(filtered_df)} records")
            
            # Filter by minimum rating
            if 'rating' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['rating'] >= min_rating]
                logger.info(f"After rating filter: {len(filtered_df)} records")
            
            # Filter by cuisines (if specified)
            if cuisines and 'cuisines' in filtered_df.columns:
                # Check if any of the specified cuisines match
                cuisine_pattern = '|'.join([c.lower() for c in cuisines])
                filtered_df = filtered_df[
                    filtered_df['cuisines'].str.lower().str.contains(cuisine_pattern, na=False)
                ]
                logger.info(f"After cuisine filter: {len(filtered_df)} records")
            
            # Sort by rating (descending) and then by cost (ascending)
            if 'rating' in filtered_df.columns and 'cost' in filtered_df.columns:
                filtered_df = filtered_df.sort_values(['rating', 'cost'], ascending=[False, True])
            
            logger.info(f"Final filtered count: {len(filtered_df)} records")
            return filtered_df
            
        except Exception as e:
            logger.error(f"Error filtering restaurants: {e}")
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            return pd.DataFrame()
    
    def get_restaurant_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific restaurant by name"""
        if not self.is_loaded or self.df is None:
            return None
        
        try:
            restaurant = self.df[self.df['name'].str.lower() == name.lower()]
            if not restaurant.empty:
                return restaurant.iloc[0].to_dict()
            return None
        except Exception as e:
            logger.error(f"Error getting restaurant by name: {e}")
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get dataset statistics"""
        if not self.is_loaded or self.df is None:
            return {}
        
        try:
            stats = {
                'total_records': len(self.df),
                'unique_locations': self.df['city'].nunique() if 'city' in self.df.columns else 0,
                'unique_cuisines': len(self.get_available_cuisines()),
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
            return stats
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            return {}
    
    def get_sample_restaurants(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get sample restaurants for testing"""
        if not self.is_loaded or self.df is None:
            return []
        
        try:
            sample = self.df.head(n)
            return sample.to_dict('records')
        except Exception as e:
            logger.error(f"Error getting sample restaurants: {e}")
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            return []
