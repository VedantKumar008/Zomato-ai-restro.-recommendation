"""
End-to-End Testing Suite
Tests complete user journey from input to recommendation
"""

import pytest
import requests
import json
from typing import Dict, List
import time


class TestE2E:
    """End-to-end test cases for the recommendation system"""
    
    BASE_URL = "http://localhost:8000"
    
    def test_complete_user_journey(self):
        """Test the complete user journey from input to recommendation"""
        # Step 1: Get available locations
        locations_response = requests.get(f"{self.BASE_URL}/api/locations")
        assert locations_response.status_code == 200
        locations = locations_response.json()
        assert len(locations) > 0
        print(f"✓ Found {len(locations)} locations")
        
        # Step 2: Get available cuisines
        cuisines_response = requests.get(f"{self.BASE_URL}/api/cuisines")
        assert cuisines_response.status_code == 200
        cuisines = cuisines_response.json()
        assert len(cuisines) > 0
        print(f"✓ Found {len(cuisines)} cuisines")
        
        # Step 3: Submit recommendation request
        recommendation_data = {
            "location": locations[0],
            "budget": 500,
            "cuisines": [cuisines[0]],
            "min_rating": 4.0,
            "preferences": "Good ambiance, family-friendly"
        }
        
        start_time = time.time()
        recommendation_response = requests.post(
            f"{self.BASE_URL}/api/recommend",
            json=recommendation_data
        )
        response_time = time.time() - start_time
        
        assert recommendation_response.status_code == 200
        recommendations = recommendation_response.json()
        assert "recommendations" in recommendations
        assert len(recommendations["recommendations"]) > 0
        print(f"✓ Got {len(recommendations['recommendations'])} recommendations in {response_time:.2f}s")
        
        # Step 4: Verify recommendation structure
        rec = recommendations["recommendations"][0]
        required_fields = ["name", "cuisine", "rating", "cost", "location"]
        for field in required_fields:
            assert field in rec, f"Missing field: {field}"
        print("✓ Recommendation structure validated")
    
    def test_filter_combinations(self):
        """Test various filter combinations"""
        locations_response = requests.get(f"{self.BASE_URL}/api/locations")
        locations = locations_response.json()
        
        cuisines_response = requests.get(f"{self.BASE_URL}/api/cuisines")
        cuisines = cuisines_response.json()
        
        test_cases = [
            {
                "location": locations[0] if locations else "Mumbai",
                "budget": 300,
                "cuisines": [cuisines[0]] if cuisines else ["North Indian"],
                "min_rating": 3.5,
                "preferences": ""
            },
            {
                "location": locations[0] if locations else "Mumbai",
                "budget": 1000,
                "cuisines": cuisines[:2] if len(cuisines) >= 2 else ["North Indian", "Chinese"],
                "min_rating": 4.5,
                "preferences": "Fine dining"
            },
            {
                "location": locations[0] if locations else "Mumbai",
                "budget": 200,
                "cuisines": [],
                "min_rating": 4.0,
                "preferences": "Budget-friendly"
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            response = requests.post(
                f"{self.BASE_URL}/api/recommend",
                json=test_case
            )
            assert response.status_code == 200, f"Test case {i+1} failed"
            print(f"✓ Filter combination {i+1} passed")
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        
        # Test 1: No results scenario
        no_results_data = {
            "location": "NonExistentCity",
            "budget": 10,
            "cuisines": ["NonExistentCuisine"],
            "min_rating": 5.0,
            "preferences": ""
        }
        response = requests.post(
            f"{self.BASE_URL}/api/recommend",
            json=no_results_data
        )
        # Should return 200 with empty recommendations or appropriate message
        assert response.status_code in [200, 404]
        print("✓ No results scenario handled")
        
        # Test 2: Extreme budget values
        extreme_budget_data = {
            "location": "Mumbai",
            "budget": 100000,  # Very high budget
            "cuisines": [],
            "min_rating": 5.0,
            "preferences": ""
        }
        response = requests.post(
            f"{self.BASE_URL}/api/recommend",
            json=extreme_budget_data
        )
        assert response.status_code == 200
        print("✓ Extreme budget value handled")
        
        # Test 3: Empty request
        empty_data = {
            "location": "",
            "budget": 0,
            "cuisines": [],
            "min_rating": 0,
            "preferences": ""
        }
        response = requests.post(
            f"{self.BASE_URL}/api/recommend",
            json=empty_data
        )
        # Should handle gracefully
        assert response.status_code in [200, 400, 422]
        print("✓ Empty request handled")
        
        # Test 4: Very long preferences text
        long_preferences = {
            "location": "Mumbai",
            "budget": 500,
            "cuisines": ["North Indian"],
            "min_rating": 4.0,
            "preferences": "A" * 1000  # Very long text
        }
        response = requests.post(
            f"{self.BASE_URL}/api/recommend",
            json=long_preferences
        )
        assert response.status_code == 200
        print("✓ Long preferences text handled")
    
    def test_pagination(self):
        """Test pagination for large result sets"""
        # Request with broad filters to get many results
        broad_filter_data = {
            "location": "Mumbai",
            "budget": 2000,
            "cuisines": [],
            "min_rating": 3.0,
            "preferences": ""
        }
        
        response = requests.post(
            f"{self.BASE_URL}/api/recommend",
            json=broad_filter_data
        )
        assert response.status_code == 200
        results = response.json()
        
        # Check if pagination is supported
        if "total" in results or "page" in results:
            print("✓ Pagination supported")
        else:
            print("✓ Pagination not implemented (results returned in single batch)")
    
    def test_data_consistency(self):
        """Test data consistency across endpoints"""
        # Get locations
        locations_response = requests.get(f"{self.BASE_URL}/api/locations")
        locations = locations_response.json()
        
        # Get cuisines
        cuisines_response = requests.get(f"{self.BASE_URL}/api/cuisines")
        cuisines = cuisines_response.json()
        
        # Make recommendation with first location and cuisine
        if locations and cuisines:
            recommendation_data = {
                "location": locations[0],
                "budget": 500,
                "cuisines": [cuisines[0]],
                "min_rating": 4.0,
                "preferences": ""
            }
            
            response = requests.post(
                f"{self.BASE_URL}/api/recommend",
                json=recommendation_data
            )
            assert response.status_code == 200
            recommendations = response.json()
            
            # Verify recommendations match the requested location and cuisine
            for rec in recommendations.get("recommendations", []):
                assert rec["location"] == locations[0] or locations[0] in rec["location"]
            
            print("✓ Data consistency verified")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
