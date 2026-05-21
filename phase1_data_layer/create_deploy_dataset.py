"""
Create Deployment-Friendly Dataset
Phase 1: Data Layer
Samples from existing processed dataset to create a memory-optimized subset for Render deployment
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def stratified_sample(df: pd.DataFrame, target_size: int = 30000) -> pd.DataFrame:
    """
    Create a stratified sample that preserves diversity across:
    - Locations (city)
    - Restaurant types (rest_type)
    - Budget categories
    - Rating categories
    
    Args:
        df: Original dataframe
        target_size: Target number of rows (default 30k)
    
    Returns:
        Sampled dataframe
    """
    logger.info(f"Original dataset size: {len(df)} rows")
    logger.info(f"Target sample size: {target_size} rows")
    
    # Calculate sampling ratio
    sampling_ratio = target_size / len(df)
    logger.info(f"Sampling ratio: {sampling_ratio:.2%}")
    
    # Stratify by multiple columns to preserve diversity
    # We'll use a combination of city, rest_type, and budget_category
    try:
        # Create a composite stratification key
        df['strata_key'] = df['city'].astype(str) + '_' + \
                           df['rest_type'].astype(str) + '_' + \
                           df['budget_category'].astype(str)
        
        # Get strata counts
        strata_counts = df['strata_key'].value_counts()
        logger.info(f"Number of unique strata: {len(strata_counts)}")
        
        # For each stratum, sample proportionally
        sampled_dfs = []
        for stratum, count in strata_counts.items():
            stratum_df = df[df['strata_key'] == stratum]
            # Calculate sample size for this stratum (minimum 1 to preserve diversity)
            sample_size = max(1, int(count * sampling_ratio))
            # Cap at actual stratum size
            sample_size = min(sample_size, count)
            
            # Sample from this stratum
            if sample_size < count:
                stratum_sample = stratum_df.sample(n=sample_size, random_state=42)
            else:
                stratum_sample = stratum_df
            
            sampled_dfs.append(stratum_sample)
        
        # Combine all samples
        sampled_df = pd.concat(sampled_dfs, ignore_index=True)
        
        # Remove the temporary strata key
        sampled_df = sampled_df.drop(columns=['strata_key'])
        
        logger.info(f"Initial stratified sample size: {len(sampled_df)} rows")
        
        # If we're still under target, add more rows randomly
        if len(sampled_df) < target_size:
            remaining_needed = target_size - len(sampled_df)
            logger.info(f"Adding {remaining_needed} more rows via random sampling")
            
            # Get rows not already in sample
            remaining_df = df[~df.index.isin(sampled_df.index)]
            additional_sample = remaining_df.sample(n=min(remaining_needed, len(remaining_df)), random_state=42)
            sampled_df = pd.concat([sampled_df, additional_sample], ignore_index=True)
        
        # If we're over target, randomly remove excess
        elif len(sampled_df) > target_size:
            excess = len(sampled_df) - target_size
            logger.info(f"Removing {excess} excess rows via random sampling")
            sampled_df = sampled_df.sample(n=target_size, random_state=42)
        
        # Reset index
        sampled_df = sampled_df.reset_index(drop=True)
        
        logger.info(f"Final sample size: {len(sampled_df)} rows")
        return sampled_df
        
    except Exception as e:
        logger.error(f"Error in stratified sampling: {e}")
        logger.info("Falling back to simple random sampling")
        # Fallback to simple random sampling
        return df.sample(n=target_size, random_state=42)


def verify_diversity(df: pd.DataFrame, original_stats: dict) -> dict:
    """
    Verify that the sampled dataset preserves diversity
    
    Args:
        df: Sampled dataframe
        original_stats: Statistics from original dataset
    
    Returns:
        Dictionary with diversity metrics
    """
    stats = {
        'total_records': len(df),
        'unique_locations': df['city'].nunique() if 'city' in df.columns else 0,
        'unique_rest_types': df['rest_type'].nunique() if 'rest_type' in df.columns else 0,
        'unique_cuisines': len(df['cuisines'].str.split(',').explode().str.strip().unique()) if 'cuisines' in df.columns else 0,
        'budget_distribution': df['budget_category'].value_counts().to_dict() if 'budget_category' in df.columns else {},
        'rating_distribution': df['rating_category'].value_counts().to_dict() if 'rating_category' in df.columns else {},
    }
    
    logger.info("=== Sampled Dataset Diversity ===")
    logger.info(f"Total records: {stats['total_records']}")
    logger.info(f"Unique locations: {stats['unique_locations']} (original: {original_stats['unique_locations']})")
    logger.info(f"Unique restaurant types: {stats['unique_rest_types']}")
    logger.info(f"Unique cuisines: {stats['unique_cuisines']}")
    logger.info(f"Budget distribution: {stats['budget_distribution']}")
    logger.info(f"Rating distribution: {stats['rating_distribution']}")
    
    return stats


def main():
    """Main function to create deployment dataset"""
    logger.info("=== Creating Deployment-Friendly Dataset ===")
    
    # Paths
    base_dir = Path(__file__).parent
    processed_dir = base_dir / "processed_data"
    input_file = processed_dir / "zomato_restaurants_processed.csv"
    output_file = processed_dir / "zomato_restaurants_processed_deploy.csv"
    
    logger.info(f"Input file: {input_file}")
    logger.info(f"Output file: {output_file}")
    
    # Load original dataset
    logger.info("Loading original dataset...")
    df = pd.read_csv(input_file)
    logger.info(f"Loaded {len(df)} rows with {len(df.columns)} columns")
    
    # Store original statistics
    original_stats = {
        'total_records': len(df),
        'unique_locations': df['city'].nunique() if 'city' in df.columns else 0,
    }
    
    # Create stratified sample (target 30k rows - middle of 25k-40k range)
    logger.info("\nCreating stratified sample...")
    sampled_df = stratified_sample(df, target_size=30000)
    
    # Verify diversity
    logger.info("\nVerifying diversity preservation...")
    sample_stats = verify_diversity(sampled_df, original_stats)
    
    # Save sampled dataset
    logger.info(f"\nSaving deployment dataset to {output_file}...")
    sampled_df.to_csv(output_file, index=False)
    logger.info(f"✅ Deployment dataset saved successfully")
    
    # Calculate file size
    file_size_mb = output_file.stat().st_size / (1024 * 1024)
    logger.info(f"File size: {file_size_mb:.2f} MB")
    
    # Calculate memory usage
    memory_usage_mb = sampled_df.memory_usage(deep=True).sum() / (1024 * 1024)
    logger.info(f"Estimated memory usage: {memory_usage_mb:.2f} MB")
    
    logger.info("\n=== Deployment Dataset Creation Complete ===")
    logger.info(f"✅ Sampled {len(sampled_df)} rows from original {len(df)} rows")
    logger.info(f"✅ Reduction: {(1 - len(sampled_df)/len(df)):.1%}")
    logger.info(f"✅ Output: {output_file}")
    logger.info(f"✅ File size: {file_size_mb:.2f} MB")
    logger.info(f"✅ Memory usage: {memory_usage_mb:.2f} MB")
    logger.info("✅ Ready for Render free-tier deployment")


if __name__ == "__main__":
    main()
