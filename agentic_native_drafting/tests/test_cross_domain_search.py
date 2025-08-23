#!/usr/bin/env python3
"""
Cross-Domain Patent Search Testing
Tests the enhanced search system across different technology domains
to verify robustness and repeatability
"""

import asyncio
import json
from datetime import datetime
from prior_art_search import PatentSearchEngine

# Test cases across diverse technology domains
TEST_CASES = [
    {
        "domain": "5G Wireless",
        "query": "5G dynamic spectrum sharing",
        "expected_min_patents": 8,
        "expected_min_relevance": 0.7
    },
    {
        "domain": "Artificial Intelligence",
        "query": "machine learning neural network optimization",
        "expected_min_patents": 10,
        "expected_min_relevance": 0.6
    },
    {
        "domain": "Blockchain",
        "query": "blockchain smart contract consensus",
        "expected_min_patents": 5,
        "expected_min_relevance": 0.6
    },
    {
        "domain": "Autonomous Vehicles",
        "query": "autonomous vehicle perception lidar",
        "expected_min_patents": 8,
        "expected_min_relevance": 0.7
    },
    {
        "domain": "Quantum Computing",
        "query": "quantum computing qubit error correction",
        "expected_min_patents": 5,
        "expected_min_relevance": 0.6
    },
    {
        "domain": "Medical Devices",
        "query": "medical imaging ultrasound beamforming",
        "expected_min_patents": 6,
        "expected_min_relevance": 0.7
    },
    {
        "domain": "Renewable Energy",
        "query": "solar cell photovoltaic efficiency",
        "expected_min_patents": 8,
        "expected_min_relevance": 0.6
    },
    {
        "domain": "Augmented Reality",
        "query": "augmented reality display optical waveguide",
        "expected_min_patents": 6,
        "expected_min_relevance": 0.6
    }
]

class CrossDomainTester:
    """Test patent search across multiple technology domains"""
    
    def __init__(self):
        self.search_engine = PatentSearchEngine()
        self.results = []
        self.start_time = datetime.now()
    
    async def run_comprehensive_test(self):
        """Run tests across all technology domains"""
        print("🔬 Cross-Domain Patent Search Testing")
        print("="*60)
        print(f"Testing {len(TEST_CASES)} technology domains...")
        print(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        for i, test_case in enumerate(TEST_CASES, 1):
            print(f"📋 Test {i}/{len(TEST_CASES)}: {test_case['domain']}")
            print(f"   Query: '{test_case['query']}'")
            
            try:
                # Run the search
                search_result = await self.search_engine.search(test_case['query'])
                
                # Analyze results
                analysis = self._analyze_search_result(search_result, test_case)
                self.results.append(analysis)
                
                # Print summary
                self._print_test_summary(analysis)
                print()
                
            except Exception as e:
                print(f"   ❌ Test failed: {e}")
                self.results.append({
                    "domain": test_case['domain'],
                    "query": test_case['query'],
                    "status": "FAILED",
                    "error": str(e)
                })
                print()
        
        # Generate comprehensive summary
        self._generate_final_summary()
    
    def _analyze_search_result(self, search_result, test_case):
        """Analyze search results against test expectations"""
        patents_found = len(search_result.patents)
        avg_relevance = sum(p.relevance_score for p in search_result.patents) / len(search_result.patents) if search_result.patents else 0.0
        
        # Check if expectations are met
        patents_pass = patents_found >= test_case['expected_min_patents']
        relevance_pass = avg_relevance >= test_case['expected_min_relevance']
        overall_pass = patents_pass and relevance_pass
        
        # Extract key metrics
        top_assignees = {}
        technology_domains = {}
        
        for patent in search_result.patents:
            # Count assignees
            for assignee in patent.assignees:
                top_assignees[assignee] = top_assignees.get(assignee, 0) + 1
            
            # Count technology domains
            tech_domain = patent.technical_analysis.get('technology_domain', 'Unknown')
            technology_domains[tech_domain] = technology_domains.get(tech_domain, 0) + 1
        
        # Get top 3 assignees and domains
        top_3_assignees = sorted(top_assignees.items(), key=lambda x: x[1], reverse=True)[:3]
        top_3_domains = sorted(technology_domains.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "domain": test_case['domain'],
            "query": test_case['query'],
            "status": "PASS" if overall_pass else "FAIL",
            "metrics": {
                "patents_found": patents_found,
                "expected_patents": test_case['expected_min_patents'],
                "patents_pass": patents_pass,
                "avg_relevance": round(avg_relevance, 3),
                "expected_relevance": test_case['expected_min_relevance'],
                "relevance_pass": relevance_pass,
                "strategies_executed": len(search_result.search_strategies),
                "unique_patents_discovered": search_result.metadata.get('unique_patents_found', 0)
            },
            "quality_indicators": {
                "top_assignees": top_3_assignees,
                "technology_domains": top_3_domains,
                "highest_relevance": max((p.relevance_score for p in search_result.patents), default=0.0),
                "patent_years": [p.patent_year for p in search_result.patents if p.patent_year]
            },
            "sample_patents": [
                {
                    "id": p.patent_id,
                    "title": p.title[:80] + "..." if len(p.title) > 80 else p.title,
                    "relevance": p.relevance_score,
                    "assignee": p.assignees[0] if p.assignees else "Unknown"
                }
                for p in search_result.patents[:3]  # Top 3 patents
            ]
        }
    
    def _print_test_summary(self, analysis):
        """Print summary of individual test results"""
        status_icon = "✅" if analysis["status"] == "PASS" else "❌"
        print(f"   {status_icon} Status: {analysis['status']}")
        
        metrics = analysis["metrics"]
        print(f"   📊 Patents: {metrics['patents_found']} (expected ≥{metrics['expected_patents']}) {'✅' if metrics['patents_pass'] else '❌'}")
        print(f"   🎯 Relevance: {metrics['avg_relevance']} (expected ≥{metrics['expected_relevance']}) {'✅' if metrics['relevance_pass'] else '❌'}")
        print(f"   🔍 Strategies: {metrics['strategies_executed']}")
        print(f"   🌐 Total discovered: {metrics['unique_patents_discovered']}")
        
        # Show top assignees if available
        if analysis["quality_indicators"]["top_assignees"]:
            top_assignee = analysis["quality_indicators"]["top_assignees"][0]
            print(f"   🏢 Top assignee: {top_assignee[0]} ({top_assignee[1]} patents)")
        
        # Show sample patent
        if analysis["sample_patents"]:
            sample = analysis["sample_patents"][0]
            print(f"   📄 Sample: {sample['title']} (relevance: {sample['relevance']})")
    
    def _generate_final_summary(self):
        """Generate comprehensive test summary"""
        print("🎯 COMPREHENSIVE TEST RESULTS")
        print("="*60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.get("status") == "PASS")
        failed_tests = total_tests - passed_tests
        
        print(f"📈 Overall Results:")
        print(f"   Total tests: {total_tests}")
        print(f"   Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"   Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        print()
        
        # Domain-by-domain results
        print(f"📋 Domain Results:")
        for result in self.results:
            if result.get("status") in ["PASS", "FAIL"]:
                status_icon = "✅" if result["status"] == "PASS" else "❌"
                metrics = result.get("metrics", {})
                patents = metrics.get("patents_found", 0)
                relevance = metrics.get("avg_relevance", 0.0)
                print(f"   {status_icon} {result['domain']}: {patents} patents, {relevance:.3f} relevance")
            else:
                print(f"   ❌ {result['domain']}: FAILED - {result.get('error', 'Unknown error')}")
        print()
        
        # System performance metrics
        if passed_tests > 0:
            successful_results = [r for r in self.results if r.get("status") == "PASS"]
            
            avg_patents = sum(r["metrics"]["patents_found"] for r in successful_results) / len(successful_results)
            avg_relevance = sum(r["metrics"]["avg_relevance"] for r in successful_results) / len(successful_results)
            avg_strategies = sum(r["metrics"]["strategies_executed"] for r in successful_results) / len(successful_results)
            
            print(f"🔧 System Performance (Successful Tests):")
            print(f"   Average patents found: {avg_patents:.1f}")
            print(f"   Average relevance score: {avg_relevance:.3f}")
            print(f"   Average strategies executed: {avg_strategies:.1f}")
            print()
        
        # Technology coverage analysis
        all_assignees = {}
        all_domains = {}
        
        for result in self.results:
            if result.get("quality_indicators"):
                for assignee, count in result["quality_indicators"].get("top_assignees", []):
                    all_assignees[assignee] = all_assignees.get(assignee, 0) + count
                
                for domain, count in result["quality_indicators"].get("technology_domains", []):
                    all_domains[domain] = all_domains.get(domain, 0) + count
        
        if all_assignees:
            print(f"🏢 Top Patent Assignees Across All Domains:")
            top_assignees = sorted(all_assignees.items(), key=lambda x: x[1], reverse=True)[:5]
            for assignee, count in top_assignees:
                print(f"   - {assignee}: {count} patents")
            print()
        
        if all_domains:
            print(f"🔬 Technology Domains Discovered:")
            top_domains = sorted(all_domains.items(), key=lambda x: x[1], reverse=True)[:5]
            for domain, count in top_domains:
                print(f"   - {domain}: {count} patents")
            print()
        
        # Time summary
        end_time = datetime.now()
        duration = end_time - self.start_time
        print(f"⏱️  Test Duration: {duration}")
        print(f"📅 Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Save detailed results
        self._save_detailed_results()
    
    def _save_detailed_results(self):
        """Save detailed test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cross_domain_test_results_{timestamp}.json"
        
        test_summary = {
            "test_metadata": {
                "timestamp": timestamp,
                "start_time": self.start_time.isoformat(),
                "total_tests": len(self.results),
                "passed_tests": sum(1 for r in self.results if r.get("status") == "PASS"),
                "failed_tests": sum(1 for r in self.results if r.get("status") == "FAIL")
            },
            "test_results": self.results,
            "test_cases": TEST_CASES
        }
        
        with open(filename, 'w') as f:
            json.dump(test_summary, f, indent=2, default=str)
        
        print(f"💾 Detailed results saved to: {filename}")

async def main():
    """Run the cross-domain testing suite"""
    tester = CrossDomainTester()
    await tester.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())
