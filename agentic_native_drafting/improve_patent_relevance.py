#!/usr/bin/env python3
"""
Script to test different optimization strategies for retrieving more relevant patents.
This will help us understand what changes have the biggest impact on relevance.
"""

import sys
import time
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.append('src')

from prior_art_search import search_prior_art_optimized, OptimizedPatentsViewAPI

def test_max_results_impact():
    """Test the impact of increasing max_results on patent retrieval"""
    
    print("🔍 TESTING MAX RESULTS IMPACT")
    print("=" * 60)
    
    test_query = "5G dynamic spectrum sharing"
    max_results_options = [5, 10, 20, 30, 50]
    
    results = {}
    
    for max_results in max_results_options:
        print(f"\n📊 Testing max_results={max_results}")
        print("-" * 40)
        
        start_time = time.time()
        
        try:
            result = search_prior_art_optimized(test_query, max_results=max_results)
            
            execution_time = time.time() - start_time
            
            if result and result.patents:
                total_claims = sum(len(p.claims) for p in result.patents)
                avg_relevance = sum(p.relevance_score for p in result.patents) / len(result.patents)
                
                results[max_results] = {
                    'patents_found': len(result.patents),
                    'total_claims': total_claims,
                    'avg_relevance': avg_relevance,
                    'execution_time': execution_time,
                    'patent_ids': [p.patent_id for p in result.patents]
                }
                
                print(f"✅ Patents found: {len(result.patents)}")
                print(f"📋 Total claims: {total_claims}")
                print(f"⭐ Average relevance: {avg_relevance:.3f}")
                print(f"⏱️  Execution time: {execution_time:.2f}s")
                print(f"🆔 Patent IDs: {', '.join(result.patents[:3])}...")
                
            else:
                results[max_results] = {
                    'patents_found': 0,
                    'total_claims': 0,
                    'avg_relevance': 0,
                    'execution_time': execution_time,
                    'patent_ids': []
                }
                print("❌ No patents found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            results[max_results] = {
                'patents_found': 0,
                'total_claims': 0,
                'avg_relevance': 0,
                'execution_time': 0,
                'patent_ids': [],
                'error': str(e)
            }
    
    return results

def test_query_strategy_impact():
    """Test different query strategies for the same search terms"""
    
    print("\n🔍 TESTING QUERY STRATEGY IMPACT")
    print("=" * 60)
    
    base_query = "5G dynamic spectrum sharing"
    
    # Different query strategies
    query_strategies = [
        ("Exact phrase", "5G dynamic spectrum sharing"),
        ("Broken down", "5G AND dynamic AND spectrum AND sharing"),
        ("Technical terms", "fifth generation dynamic spectrum sharing"),
        ("Abbreviations", "5G NR dynamic spectrum sharing"),
        ("Related terms", "5G spectrum allocation sharing"),
        ("Broader scope", "5G spectrum management")
    ]
    
    results = {}
    
    for strategy_name, query in query_strategies:
        print(f"\n📝 Strategy: {strategy_name}")
        print(f"Query: {query}")
        print("-" * 40)
        
        start_time = time.time()
        
        try:
            result = search_prior_art_optimized(query, max_results=20)
            
            execution_time = time.time() - start_time
            
            if result and result.patents:
                total_claims = sum(len(p.claims) for p in result.patents)
                avg_relevance = sum(p.relevance_score for p in result.patents) / len(result.patents)
                
                results[strategy_name] = {
                    'query': query,
                    'patents_found': len(result.patents),
                    'total_claims': total_claims,
                    'avg_relevance': avg_relevance,
                    'execution_time': execution_time,
                    'patent_ids': [p.patent_id for p in result.patents]
                }
                
                print(f"✅ Patents found: {len(result.patents)}")
                print(f"📋 Total claims: {total_claims}")
                print(f"⭐ Average relevance: {avg_relevance:.3f}")
                print(f"⏱️  Execution time: {execution_time:.2f}s")
                
            else:
                results[strategy_name] = {
                    'query': query,
                    'patents_found': 0,
                    'total_claims': 0,
                    'avg_relevance': 0,
                    'execution_time': execution_time,
                    'patent_ids': []
                }
                print("❌ No patents found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            results[strategy_name] = {
                'query': query,
                'patents_found': 0,
                'total_claims': 0,
                'avg_relevance': 0,
                'execution_time': 0,
                'patent_ids': [],
                'error': str(e)
            }
    
    return results

def test_domain_specific_queries():
    """Test queries across different technology domains"""
    
    print("\n🔍 TESTING DOMAIN-SPECIFIC QUERIES")
    print("=" * 60)
    
    domain_queries = [
        ("Telecom - 5G", "5G network slicing architecture"),
        ("Telecom - Spectrum", "dynamic spectrum sharing 5G"),
        ("AI/ML", "machine learning algorithm optimization"),
        ("IoT", "internet of things device management"),
        ("Blockchain", "distributed ledger smart contracts"),
        ("Software", "cloud computing microservices")
    ]
    
    results = {}
    
    for domain, query in domain_queries:
        print(f"\n🌐 Domain: {domain}")
        print(f"Query: {query}")
        print("-" * 40)
        
        start_time = time.time()
        
        try:
            result = search_prior_art_optimized(query, max_results=20)
            
            execution_time = time.time() - start_time
            
            if result and result.patents:
                total_claims = sum(len(p.claims) for p in result.patents)
                avg_relevance = sum(p.relevance_score for p in result.patents) / len(result.patents)
                
                results[domain] = {
                    'query': query,
                    'patents_found': len(result.patents),
                    'total_claims': total_claims,
                    'avg_relevance': avg_relevance,
                    'execution_time': execution_time,
                    'patent_ids': [p.patent_id for p in result.patents]
                }
                
                print(f"✅ Patents found: {len(result.patents)}")
                print(f"📋 Total claims: {total_claims}")
                print(f"⭐ Average relevance: {avg_relevance:.3f}")
                print(f"⏱️  Execution time: {execution_time:.2f}s")
                
            else:
                results[domain] = {
                    'query': query,
                    'patents_found': 0,
                    'total_claims': 0,
                    'avg_relevance': 0,
                    'execution_time': execution_time,
                    'patent_ids': []
                }
                print("❌ No patents found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            results[domain] = {
                'query': query,
                'patents_found': 0,
                'total_claims': 0,
                'avg_relevance': 0,
                'execution_time': 0,
                'patent_ids': [],
                'error': str(e)
            }
    
    return results

def generate_optimization_report(max_results_results, query_strategy_results, domain_results):
    """Generate a comprehensive optimization report"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"patent_optimization_report_{timestamp}.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Patent Retrieval Optimization Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        # Max Results Impact
        f.write("## 📊 Max Results Impact Analysis\n\n")
        f.write("| Max Results | Patents Found | Total Claims | Avg Relevance | Execution Time |\n")
        f.write("|-------------|---------------|--------------|---------------|----------------|\n")
        
        for max_results in sorted(max_results_results.keys()):
            data = max_results_results[max_results]
            f.write(f"| {max_results} | {data['patents_found']} | {data['total_claims']} | {data['avg_relevance']:.3f} | {data['execution_time']:.2f}s |\n")
        
        f.write("\n### Key Insights:\n")
        f.write("- **Optimal max_results**: Based on relevance vs. time trade-off\n")
        f.write("- **Claims retrieval efficiency**: How claims scale with patent count\n")
        f.write("- **Performance impact**: Time scaling with result count\n\n")
        
        # Query Strategy Impact
        f.write("## 🎯 Query Strategy Impact Analysis\n\n")
        f.write("| Strategy | Query | Patents | Claims | Relevance | Time |\n")
        f.write("|----------|-------|---------|--------|-----------|------|\n")
        
        for strategy, data in query_strategy_results.items():
            f.write(f"| {strategy} | {data['query'][:30]}... | {data['patents_found']} | {data['total_claims']} | {data['avg_relevance']:.3f} | {data['execution_time']:.2f}s |\n")
        
        f.write("\n### Key Insights:\n")
        f.write("- **Most effective strategy**: Which approach yields best results\n")
        f.write("- **Query precision**: Balance between specificity and coverage\n")
        f.write("- **Term effectiveness**: Which search terms work best\n\n")
        
        # Domain Performance
        f.write("## 🌐 Domain Performance Analysis\n\n")
        f.write("| Domain | Query | Patents | Claims | Relevance | Time |\n")
        f.write("|--------|-------|---------|--------|-----------|------|\n")
        
        for domain, data in domain_results.items():
            f.write(f"| {domain} | {data['query'][:30]}... | {data['patents_found']} | {data['total_claims']} | {data['avg_relevance']:.3f} | {data['execution_time']:.2f}s |\n")
        
        f.write("\n### Key Insights:\n")
        f.write("- **Domain coverage**: Which technology areas work best\n")
        f.write("- **Query effectiveness**: Domain-specific query strategies\n")
        f.write("- **Performance variation**: Time differences across domains\n\n")
        
        # Recommendations
        f.write("## 🚀 Optimization Recommendations\n\n")
        f.write("### 1. Immediate Improvements\n")
        f.write("- Increase default max_results to 20-30\n")
        f.write("- Implement query strategy selection based on domain\n")
        f.write("- Add fallback search strategies\n\n")
        
        f.write("### 2. Medium-term Enhancements\n")
        f.write("- Develop domain-specific query templates\n")
        f.write("- Implement intelligent query expansion\n")
        f.write("- Add relevance-based result filtering\n\n")
        
        f.write("### 3. Long-term Optimizations\n")
        f.write("- Machine learning-based query optimization\n")
        f.write("- Patent clustering and deduplication\n")
        f.write("- Advanced relevance scoring algorithms\n\n")
    
    print(f"\n📋 Optimization report saved: {report_file}")
    return report_file

def main():
    """Main function to run all optimization tests"""
    
    print("🚀 PATENT RETRIEVAL OPTIMIZATION ANALYSIS")
    print("=" * 80)
    print("This script will test different strategies to improve patent relevance")
    print("=" * 80)
    
    # Test 1: Max Results Impact
    print("\n🔍 PHASE 1: Testing max_results impact...")
    max_results_results = test_max_results_impact()
    
    # Test 2: Query Strategy Impact
    print("\n🔍 PHASE 2: Testing query strategies...")
    query_strategy_results = test_query_strategy_impact()
    
    # Test 3: Domain Performance
    print("\n🔍 PHASE 3: Testing domain-specific queries...")
    domain_results = test_domain_specific_queries()
    
    # Generate Report
    print("\n📋 Generating optimization report...")
    report_file = generate_optimization_report(max_results_results, query_strategy_results, domain_results)
    
    print(f"\n🎉 OPTIMIZATION ANALYSIS COMPLETE!")
    print(f"📁 Report saved: {report_file}")
    print("\n💡 Key findings:")
    
    # Show top performers
    if max_results_results:
        best_max = max(max_results_results.keys(), key=lambda x: max_results_results[x]['patents_found'])
        print(f"   📊 Best max_results: {best_max} (found {max_results_results[best_max]['patents_found']} patents)")
    
    if query_strategy_results:
        best_strategy = max(query_strategy_results.keys(), key=lambda x: query_strategy_results[x]['avg_relevance'])
        print(f"   🎯 Best query strategy: {best_strategy} (relevance: {query_strategy_results[best_strategy]['avg_relevance']:.3f})")
    
    if domain_results:
        best_domain = max(domain_results.keys(), key=lambda x: domain_results[x]['patents_found'])
        print(f"   🌐 Best performing domain: {best_domain} (found {domain_results[best_domain]['patents_found']} patents)")

if __name__ == "__main__":
    main()
