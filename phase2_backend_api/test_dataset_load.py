"""
Test script to verify the optimized dataset loads successfully
"""

import sys
from pathlib import Path

# Add parent directory to path to import data_service
sys.path.insert(0, str(Path(__file__).parent))

from data_service import DataService

def test_optimized_dataset():
    """Test that the optimized dataset loads successfully"""
    
    # Path to optimized dataset
    data_path = Path(__file__).parent.parent / 'phase1_data_layer' / 'processed_data' / 'zomato_restaurants_deployment.csv'
    
    print(f"Testing dataset load from: {data_path}")
    print(f"File exists: {data_path.exists()}")
    
    if not data_path.exists():
        print("ERROR: Dataset file not found!")
        return False
    
    # Load dataset
    data_service = DataService(data_path=str(data_path.absolute()))
    
    if not data_service.is_loaded:
        print("ERROR: Dataset failed to load!")
        return False
    
    print("✅ Dataset loaded successfully!")
    print(f"Row count: {len(data_service.df)}")
    print(f"Columns: {list(data_service.df.columns)}")
    print(f"Memory usage: {data_service.df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    # Test essential functionality
    locations = data_service.get_available_locations()
    print(f"Unique locations: {len(locations)}")
    
    cuisines = data_service.get_available_cuisines()
    print(f"Unique cuisines: {len(cuisines)}")
    
    stats = data_service.get_statistics()
    print(f"Statistics: {stats}")
    
    # Test filtering
    if locations:
        filtered = data_service.filter_restaurants(
            location=locations[0],
            budget=1000,
            min_rating=3.5
        )
        print(f"Filter test returned {len(filtered)} restaurants")
    
    print("\n✅ All tests passed!")
    return True

if __name__ == "__main__":
    success = test_optimized_dataset()
    sys.exit(0 if success else 1)
