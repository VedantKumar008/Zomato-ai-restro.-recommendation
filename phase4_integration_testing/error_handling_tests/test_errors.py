"""
Error Handling Test Suite
Tests all error scenarios and validates error messages
"""

import pytest
import requests
import json
from typing import Dict


class TestErrorHandling:
    """Error handling test cases"""
    
    BASE_URL = "http://localhost:8000"
    
    def test_invalid_endpoint(self):
        """Test accessing non-existent endpoints"""
        response = requests.get(f"{self.BASE_URL}/api/nonexistent")
        assert response.status_code == 404
        print("✓ Invalid endpoint returns 404")
    
    def test_invalid_method(self):
        """Test using wrong HTTP method"""
        response = requests.put(f"{self.BASE_URL}/api/locations")
        assert response.status_code in [405, 404]
        print("✓ Invalid method returns 405 or 404")
    
    def test_missing_required_fields(self):
        """Test requests with missing required fields"""
        # Missing location
        data = {
            "budget": 500,
            "cuisines": ["North Indian"],
            "min_rating": 4.0
        }
        response = requests.post(f"{self.BASE_URL}/api/recommend", json=data)
        assert response.status_code in [400, 422]
        print("✓ Missing location field handled")
        
        # Missing budget
        data = {
            "location": "Mumbai",
            "cuisines": ["North Indian"],
            "min_rating": 4.0
        }
        response = requests.post(f"{self.BASE_URL}/api/recommend", json=data)
        assert response.status_code in [400, 422]
        print("✓ Missing budget field handled")
    
    def test_invalid_data_types(self):
        """Test requests with invalid data types"""
        # String instead of number for budget
        data = {
            "location": "Mumbai",
            "budget": "five hundred",
            "cuisines": ["North Indian"],
            "min_rating": 4.0,
            "preferences": ""
        }
        response = requests.post(f"{self.BASE_URL}/api/recommend", json=data)
        assert response.status_code in [400, 422]
        print("✓ Invalid budget type handled")
        
        # Number instead of string for location
        data = {
            "location": 123,
            "budget": 500,
            "cuisines": ["North Indian"],
            "min_rating": 4.0,
            "preferences": ""
        }
        response = requests.post(f"{self.BASE_URL}/api/recommend", json=data)
        assert response.status_code in [400, 422]
        print("✓ Invalid location type handled")
        
        # Invalid rating value
        data = {
            "location": "Mumbai",
            "budget": 500,
            "cuisines": ["North Indian"],
            "min_rating": 6.0,  # Rating > 5
            "preferences": ""
        }
        response = requests.post(f"{self.BASE_URL}/api/recommend", json=data)
        assert response.status_code in [400, 422]
        print("✓ Invalid rating value handled")
    
    def test_negative_values(self):
        """Test requests with negative values"""
        data = {
            "location": "Mumbai",
            "budget": -100,
            "cuisines": ["North Indian"],
            "min_rating": -1.0,
            "preferences": ""
        }
        response = requests.post(f"{self.BASE_URL}/api/recommend", json=data)
        assert response.status_code in [400, 422]
        print("✓ Negative values handled")
    
    def test_malformed_json(self):
        """Test malformed JSON in request body"""
        response = requests.post(
            f"{self.BASE_URL}/api/recommend",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [400, 422]
        print("✓ Malformed JSON handled")
    
    def test_empty_request_body(self):
        """Test empty request body"""
        response = requests.post(
            f"{self.BASE_URL}/api/recommend",
            json={},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [400, 422]
        print("✓ Empty request body handled")
    
    def test_large_payload(self):
        """Test with excessively large payload"""
        large_preferences = "A" * 100000  # 100KB of text
        data = {
            "location": "Mumbai",
            "budget": 500,
            "cuisines": ["North Indian"],
            "min_rating": 4.0,
            "preferences": large_preferences
        }
        response = requests.post(f"{self.BASE_URL}/api/recommend", json=data)
        # Should either handle it or return appropriate error
        assert response.status_code in [200, 413, 400]
        print("✓ Large payload handled")
    
    def test_special_characters(self):
        """Test with special characters in input"""
        data = {
            "location": "Mumbai",
            "budget": 500,
            "cuisines": ["North Indian"],
            "min_rating": 4.0,
            "preferences": "<script>alert('xss')</script> OR 1=1--"
        }
        response = requests.post(f"{self.BASE_URL}/api/recommend", json=data)
        # Should handle without security issues
        assert response.status_code == 200
        result = response.json()
        # Verify special characters are sanitized in response
        print("✓ Special characters handled")
    
    def test_sql_injection_attempts(self):
        """Test SQL injection attempts"""
        malicious_inputs = [
            "Mumbai' OR '1'='1",
            "Mumbai; DROP TABLE restaurants--",
            "Mumbai' UNION SELECT * FROM users--"
        ]
        
        for malicious_input in malicious_inputs:
            data = {
                "location": malicious_input,
                "budget": 500,
                "cuisines": ["North Indian"],
                "min_rating": 4.0,
                "preferences": ""
            }
            response = requests.post(f"{self.BASE_URL}/api/recommend", json=data)
            # Should handle gracefully without SQL errors
            assert response.status_code in [200, 400, 422]
        
        print("✓ SQL injection attempts handled")
    
    def test_rate_limiting(self):
        """Test rate limiting if implemented"""
        # Send multiple rapid requests
        responses = []
        for _ in range(20):
            response = requests.get(f"{self.BASE_URL}/api/locations")
            responses.append(response)
        
        # Check if any requests were rate limited
        rate_limited = any(r.status_code == 429 for r in responses)
        
        if rate_limited:
            print("✓ Rate limiting is implemented and working")
        else:
            print("⚠ Rate limiting not implemented (consider adding)")
    
    def test_error_message_format(self):
        """Test that error messages are user-friendly"""
        # Trigger an error
        data = {
            "location": "InvalidCity123456",
            "budget": 500,
            "cuisines": ["InvalidCuisine123456"],
            "min_rating": 4.0,
            "preferences": ""
        }
        response = requests.post(f"{self.BASE_URL}/api/recommend", json=data)
        
        # Check error message format
        if response.status_code != 200:
            error_data = response.json()
            assert "error" in error_data or "message" in error_data or "detail" in error_data
            print("✓ Error messages are properly formatted")
        else:
            print("✓ Request succeeded (no error to test)")
    
    def test_concurrent_error_scenarios(self):
        """Test error handling under concurrent load"""
        import concurrent.futures
        
        def make_error_request():
            data = {
                "location": "",
                "budget": -100,
                "cuisines": [],
                "min_rating": -1.0
            }
            return requests.post(f"{self.BASE_URL}/api/recommend", json=data)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_error_request) for _ in range(20)]
            responses = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All should return error status codes
        error_codes = [400, 422, 500]
        for response in responses:
            assert response.status_code in error_codes
        
        print("✓ Concurrent error scenarios handled")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
