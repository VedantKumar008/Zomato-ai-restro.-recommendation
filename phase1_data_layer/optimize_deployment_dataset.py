"""
Optimize dataset for deployment on Render free-tier
Reduces memory usage by removing unnecessary columns and limiting row count
"""

import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_memory_usage(df: pd.DataFrame):
    """Analyze memory usage by column"""
    logger.info("=" * 60)
    logger.info("MEMORY USAGE ANALYSIS BY COLUMN")
    logger.info("=" * 60)
    
    mem_usage = df.memory_usage(deep=True).sort_values(ascending=False)
    total_mem = mem_usage.sum() / 1024 / 1024
    
    for col, mem in mem_usage.items():
        logger.info(f"{col:25s}: {mem / 1024 / 1024:8.2f} MB ({mem / total_mem / 1024 / 1024 * 100:5.1f}%)")
    
    logger.info(f"{'TOTAL':25s}: {total_mem:8.2f} MB")
    logger.info("=" * 60)
    
    return mem_usage

def create_optimized_dataset():
    """Create deployment-optimized dataset"""
    
    # Load original dataset
    input_path = Path("processed_data/zomato_restaurants_processed.csv")
    logger.info(f"Loading original dataset from {input_path}")
    
    df = pd.read_csv(input_path)
    logger.info(f"Original dataset: {len(df)} rows, {len(df.columns)} columns")
    
    # Analyze memory usage
    analyze_memory_usage(df)
    
    # Columns to keep (essential for app functionality)
    # Based on data_service.py usage:
    # - name: for restaurant display
    # - city: for location dropdowns and filtering
    # - cuisines: for cuisine dropdowns and filtering
    # - cost: for budget filtering
    # - rating: for rating filtering and sorting
    essential_columns = ['name', 'city', 'cuisines', 'cost', 'rating']
    
    logger.info(f"Essential columns: {essential_columns}")
    logger.info(f"Columns to remove: {set(df.columns) - set(essential_columns)}")
    
    # Create optimized dataframe with only essential columns
    df_optimized = df[essential_columns].copy()
    
    # Remove rows with missing essential data
    df_optimized = df_optimized.dropna(subset=['name', 'city', 'cuisines', 'cost', 'rating'])
    
    # For Render free-tier, use a reasonable row count
    # Free tier has 512MB RAM, aim for ~50MB dataset to leave room for app
    # With 5 columns, we can keep more rows than with 22 columns
    target_rows = 15000  # Reasonable for free-tier while maintaining diversity
    
    if len(df_optimized) > target_rows:
        logger.info(f"Sampling {target_rows} rows from {len(df_optimized)} available rows")
        # Stratified sampling by city to maintain location diversity
        # Use as_index=False to keep city as a column
        samples = []
        for city_name, group in df_optimized.groupby('city'):
            n_samples = min(len(group), max(1, target_rows // df_optimized['city'].nunique()))
            samples.append(group.sample(n=n_samples, random_state=42))
        
        df_optimized = pd.concat(samples, ignore_index=True)
        
        # If still too many rows, take random sample
        if len(df_optimized) > target_rows:
            df_optimized = df_optimized.sample(n=target_rows, random_state=42).reset_index(drop=True)
    
    logger.info(f"Optimized dataset: {len(df_optimized)} rows, {len(df_optimized.columns)} columns")
    
    # Analyze optimized memory usage
    analyze_memory_usage(df_optimized)
    
    # Save optimized dataset
    output_path = Path("processed_data/zomato_restaurants_deployment.csv")
    df_optimized.to_csv(output_path, index=False)
    logger.info(f"Saved optimized dataset to {output_path}")
    
    # Log summary
    logger.info("=" * 60)
    logger.info("OPTIMIZATION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Original rows: {len(df)}")
    logger.info(f"Optimized rows: {len(df_optimized)}")
    logger.info(f"Row reduction: {(1 - len(df_optimized) / len(df)) * 100:.1f}%")
    logger.info(f"Original columns: {len(df.columns)}")
    logger.info(f"Optimized columns: {len(df_optimized.columns)}")
    logger.info(f"Column reduction: {(1 - len(df_optimized.columns) / len(df.columns)) * 100:.1f}%")
    logger.info(f"Original memory: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    logger.info(f"Optimized memory: {df_optimized.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    logger.info(f"Memory reduction: {(1 - df_optimized.memory_usage(deep=True).sum() / df.memory_usage(deep=True).sum()) * 100:.1f}%")
    logger.info("=" * 60)
    
    # Log unique counts
    logger.info(f"Unique locations: {df_optimized['city'].nunique()}")
    logger.info(f"Unique cuisines: {len(set(', '.join(df_optimized['cuisines'].dropna()).split(', ')))}")
    logger.info(f"Rating range: {df_optimized['rating'].min():.1f} - {df_optimized['rating'].max():.1f}")
    logger.info(f"Cost range: {df_optimized['cost'].min():.0f} - {df_optimized['cost'].max():.0f}")
    
    return df_optimized

if __name__ == "__main__":
    create_optimized_dataset()
