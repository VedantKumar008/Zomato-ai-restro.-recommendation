"""
Performance Testing Suite
Load tests API endpoints and measures response times
"""

import requests
import time
import statistics
from typing import List, Dict
import concurrent.futures
import json


class PerformanceTester:
    """Performance testing utilities"""
    
    BASE_URL = "http://localhost:8000"
    
    def __init__(self):
        self.results = []
    
    def measure_endpoint(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Measure response time for a single endpoint call"""
        url = f"{self.BASE_URL}{endpoint}"
        start_time = time.time()
        
        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            return {
                "endpoint": endpoint,
                "method": method,
                "status_code": response.status_code,
                "response_time_ms": response_time,
                "success": response.status_code == 200
            }
        except Exception as e:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return {
                "endpoint": endpoint,
                "method": method,
                "status_code": None,
                "response_time_ms": response_time,
                "success": False,
                "error": str(e)
            }
    
    def load_test_endpoint(self, endpoint: str, method: str = "GET", 
                          data: Dict = None, num_requests: int = 100, 
                          concurrent_users: int = 10) -> Dict:
        """Load test an endpoint with concurrent requests"""
        print(f"\nLoad testing {endpoint} with {num_requests} requests, {concurrent_users} concurrent users")
        
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = []
            for _ in range(num_requests):
                future = executor.submit(self.measure_endpoint, endpoint, method, data)
                futures.append(future)
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)
        
        # Calculate statistics
        successful_results = [r for r in results if r["success"]]
        failed_results = [r for r in results if not r["success"]]
        
        response_times = [r["response_time_ms"] for r in successful_results]
        
        stats = {
            "endpoint": endpoint,
            "total_requests": num_requests,
            "successful_requests": len(successful_results),
            "failed_requests": len(failed_results),
            "success_rate": (len(successful_results) / num_requests) * 100,
            "avg_response_time_ms": statistics.mean(response_times) if response_times else 0,
            "min_response_time_ms": min(response_times) if response_times else 0,
            "max_response_time_ms": max(response_times) if response_times else 0,
            "median_response_time_ms": statistics.median(response_times) if response_times else 0,
            "p95_response_time_ms": statistics.quantiles(response_times, n=20)[18] if len(response_times) >= 20 else 0,
            "p99_response_time_ms": statistics.quantiles(response_times, n=100)[98] if len(response_times) >= 100 else 0,
            "errors": [r.get("error") for r in failed_results if r.get("error")]
        }
        
        return stats
    
    def test_llm_performance(self, num_requests: int = 20) -> Dict:
        """Test LLM endpoint performance specifically"""
        print("\nTesting LLM recommendation endpoint performance")
        
        # Get sample data
        locations_response = requests.get(f"{self.BASE_URL}/api/locations")
        locations = locations_response.json() if locations_response.status_code == 200 else ["Mumbai"]
        
        cuisines_response = requests.get(f"{self.BASE_URL}/api/cuisines")
        cuisines = cuisines_response.json() if cuisines_response.status_code == 200 else ["North Indian"]
        
        test_data = {
            "location": locations[0] if locations else "Mumbai",
            "budget": 500,
            "cuisines": [cuisines[0]] if cuisines else ["North Indian"],
            "min_rating": 4.0,
            "preferences": "Good ambiance"
        }
        
        return self.load_test_endpoint(
            "/api/recommend",
            method="POST",
            data=test_data,
            num_requests=num_requests,
            concurrent_users=5
        )
    
    def test_data_endpoints(self) -> Dict:
        """Test data retrieval endpoints performance"""
        print("\nTesting data endpoints performance")
        
        endpoints = [
            ("/api/locations", "GET"),
            ("/api/cuisines", "GET")
        ]
        
        results = {}
        for endpoint, method in endpoints:
            stats = self.load_test_endpoint(endpoint, method, num_requests=50, concurrent_users=10)
            results[endpoint] = stats
        
        return results
    
    def generate_report(self, results: Dict) -> str:
        """Generate performance test report"""
        report = []
        report.append("=" * 80)
        report.append("PERFORMANCE TEST REPORT")
        report.append("=" * 80)
        report.append(f"Test Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        if "llm_performance" in results:
            report.append("LLM Endpoint Performance:")
            report.append("-" * 80)
            stats = results["llm_performance"]
            report.append(f"  Total Requests: {stats['total_requests']}")
            report.append(f"  Success Rate: {stats['success_rate']:.2f}%")
            report.append(f"  Avg Response Time: {stats['avg_response_time_ms']:.2f}ms")
            report.append(f"  Min Response Time: {stats['min_response_time_ms']:.2f}ms")
            report.append(f"  Max Response Time: {stats['max_response_time_ms']:.2f}ms")
            report.append(f"  Median Response Time: {stats['median_response_time_ms']:.2f}ms")
            report.append(f"  P95 Response Time: {stats['p95_response_time_ms']:.2f}ms")
            report.append(f"  P99 Response Time: {stats['p99_response_time_ms']:.2f}ms")
            report.append("")
        
        if "data_endpoints" in results:
            report.append("Data Endpoints Performance:")
            report.append("-" * 80)
            for endpoint, stats in results["data_endpoints"].items():
                report.append(f"\n  {endpoint}:")
                report.append(f"    Success Rate: {stats['success_rate']:.2f}%")
                report.append(f"    Avg Response Time: {stats['avg_response_time_ms']:.2f}ms")
                report.append(f"    P95 Response Time: {stats['p95_response_time_ms']:.2f}ms")
            report.append("")
        
        report.append("=" * 80)
        return "\n".join(report)


def main():
    """Run performance tests"""
    tester = PerformanceTester()
    results = {}
    
    # Test data endpoints
    results["data_endpoints"] = tester.test_data_endpoints()
    
    # Test LLM endpoint
    results["llm_performance"] = tester.test_llm_performance(num_requests=20)
    
    # Generate and print report
    report = tester.generate_report(results)
    print(report)
    
    # Save report to file
    with open("../reports/performance_report.txt", "w") as f:
        f.write(report)
    
    print("\nReport saved to ../reports/performance_report.txt")
    
    # Save JSON results
    with open("../reports/performance_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("JSON results saved to ../reports/performance_results.json")


if __name__ == "__main__":
    main()
