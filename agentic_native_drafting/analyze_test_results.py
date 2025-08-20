#!/usr/bin/env python3
"""Analyze comprehensive test results and display in table format"""

import json
import sys

def analyze_test_results():
    """Analyze and display test results"""
    
    try:
        # Load the test results
        with open('comprehensive_test_results_20250819_143020.json', 'r') as f:
            data = json.load(f)
        
        print("📊 COMPREHENSIVE TEST RESULTS ANALYSIS")
        print("=" * 120)
        print(f"\n🔍 TEST SUMMARY:")
        print(f"   Total Tests: {len(data['test_cases'])}")
        print(f"   Timestamp: {data['timestamp']}")
        
        successful_tests = sum(1 for tc in data['test_cases'] if tc['search_successful'])
        print(f"   Successful: {successful_tests}")
        print(f"   Failed: {len(data['test_cases']) - successful_tests}")
        print(f"   Success Rate: {(successful_tests/len(data['test_cases']))*100:.1f}%")
        
        print("\n📋 DETAILED RESULTS FOR EACH TEST CASE:")
        print("-" * 120)
        
        for i, test_case in enumerate(data['test_cases'], 1):
            tc = test_case['test_case']
            status = "✅ SUCCESS" if test_case['search_successful'] else "❌ FAILED"
            
            print(f"\n🧪 TEST CASE {i}: {tc['name']}")
            print(f"   Query: \"{tc['query']}\"")
            print(f"   Domain: {tc['domain']}")
            print(f"   Status: {status}")
            print(f"   Report Length: {test_case['result_length']} characters")
            print(f"   Timestamp: {test_case['timestamp']}")
            
            # Extract key information from preview
            preview = test_case['result_preview']
            if "Patent ID:" in preview:
                # Try to extract patent IDs
                lines = preview.split('\n')
                patent_lines = [line for line in lines if "Patent ID:" in line]
                if patent_lines:
                    print(f"   Key Patents Found:")
                    for patent_line in patent_lines[:3]:  # Show first 3
                        print(f"     {patent_line.strip()}")
            
            print("   " + "-" * 80)
        
        print(f"\n💾 Results saved to: comprehensive_test_results_20250819_143020.json")
        
    except FileNotFoundError:
        print("❌ Test results file not found!")
        print("Run the comprehensive test function first.")
    except Exception as e:
        print(f"❌ Error analyzing results: {e}")

if __name__ == "__main__":
    analyze_test_results()
