#!/usr/bin/env python3
"""Score individual test case reports based on quality criteria"""

import json
import sys

def score_report(report_preview, test_case_info):
    """Score a report based on quality criteria"""
    
    score = 0
    max_score = 100
    feedback = []
    
    # Criterion 1: Patent Relevance (25 points)
    # Check if domain-related terms appear in the report
    domain_terms = test_case_info['domain'].lower().split()
    domain_found = any(term.lower() in report_preview.lower() for term in domain_terms)
    
    if domain_found:
        score += 15
        feedback.append("✅ Domain relevance: Good")
    else:
        # Check for broader technology terms
        tech_terms = ['5G', 'AI', 'machine learning', 'blockchain', 'quantum', 'spectrum', 'telecommunications']
        tech_found = any(term.lower() in report_preview.lower() for term in tech_terms)
        if tech_found:
            score += 10
            feedback.append("✅ Domain relevance: Technology terms found")
        else:
            feedback.append("⚠️ Domain relevance: Could be better")
    
    if "Patent ID:" in report_preview:
        score += 10
        feedback.append("✅ Patent identification: Present")
    else:
        feedback.append("❌ Patent identification: Missing")
    
    # Criterion 2: Report Structure (25 points)
    # Check for executive summary (various formats)
    if any(term in report_preview for term in ["EXECUTIVE SUMMARY", "Executive Summary", "executive summary"]):
        score += 10
        feedback.append("✅ Executive summary: Present")
    else:
        feedback.append("❌ Executive summary: Missing")
    
    # Check for risk assessment (various formats)
    if any(term in report_preview for term in ["RISK ASSESSMENT", "Risk Assessment", "risk assessment", "Risk Level:"]):
        score += 10
        feedback.append("✅ Risk assessment: Present")
    else:
        feedback.append("❌ Risk assessment: Missing")
    
    # Check for business/technical analysis (various formats)
    analysis_terms = ["BUSINESS RECOMMENDATIONS", "TECHNICAL ANALYSIS", "Business Recommendations", 
                     "Technical Analysis", "business recommendations", "technical analysis",
                     "Licensing Strategy", "Development Strategy", "Cost-Benefit"]
    if any(term in report_preview for term in analysis_terms):
        score += 5
        feedback.append("✅ Business/Technical analysis: Present")
    else:
        feedback.append("⚠️ Business/Technical analysis: Could be better")
    
    # Criterion 3: Content Quality (25 points)
    if len(report_preview) > 5000:
        score += 15
        feedback.append("✅ Content length: Comprehensive (>5000 chars)")
    elif len(report_preview) > 3000:
        score += 10
        feedback.append("✅ Content length: Good (>3000 chars)")
    else:
        feedback.append("⚠️ Content length: Could be longer")
    
    # Check for risk levels (various formats)
    risk_indicators = ["Risk Level:", "Risk Level", "High", "Medium", "Low", "🔴", "🟡", "🟢"]
    if any(indicator in report_preview for indicator in risk_indicators):
        score += 10
        feedback.append("✅ Risk assessment: Clear risk levels")
    else:
        feedback.append("❌ Risk assessment: Missing risk levels")
    
    # Criterion 4: Actionability (25 points)
    # Check for action items (various formats)
    action_terms = ["Action Required", "Next Steps", "next steps", "What You Need to Do", 
                   "Timeline", "timeline", "Week 1", "Month 1", "Month 3"]
    if any(term in report_preview for term in action_terms):
        score += 15
        feedback.append("✅ Actionability: Clear next steps")
    else:
        feedback.append("⚠️ Actionability: Could be clearer")
    
    # Check for business focus (various formats)
    business_terms = ["Business Impact", "business impact", "Cost", "cost", "Licensing", 
                     "licensing", "Estimated Costs", "estimated costs"]
    if any(term in report_preview for term in business_terms):
        score += 10
        feedback.append("✅ Business focus: Clear business impact")
    else:
        feedback.append("⚠️ Business focus: Could be stronger")
    
    return score, feedback

def analyze_and_score_reports():
    """Analyze and score all test case reports"""
    
    try:
        # Load the test results
        with open('comprehensive_test_results_20250819_143020.json', 'r') as f:
            data = json.load(f)
        
        print("📊 INDIVIDUAL REPORT QUALITY SCORING")
        print("=" * 100)
        print(f"\n🔍 SCORING CRITERIA:")
        print(f"   • Patent Relevance (25 points)")
        print(f"   • Report Structure (25 points)")
        print(f"   • Content Quality (25 points)")
        print(f"   • Actionability (25 points)")
        print(f"   • Total: 100 points")
        
        print("\n📋 INDIVIDUAL REPORT SCORES:")
        print("-" * 100)
        
        total_score = 0
        scores = []
        
        for i, test_case in enumerate(data['test_cases'], 1):
            tc = test_case['test_case']
            preview = test_case['result_preview']
            
            # Score this report
            score, feedback = score_report(preview, tc)
            scores.append(score)
            total_score += score
            
            print(f"\n🧪 TEST CASE {i}: {tc['name']}")
            print(f"   Query: \"{tc['query']}\"")
            print(f"   Domain: {tc['domain']}")
            print(f"   Report Length: {test_case['result_length']} characters")
            print(f"   📊 SCORE: {score}/100")
            
            # Grade
            if score >= 90:
                grade = "🏆 A+ (Excellent)"
            elif score >= 80:
                grade = "🥇 A (Very Good)"
            elif score >= 70:
                grade = "🥈 B+ (Good)"
            elif score >= 60:
                grade = "🥉 B (Satisfactory)"
            else:
                grade = "⚠️ C (Needs Improvement)"
            
            print(f"   🎯 GRADE: {grade}")
            
            # Feedback
            print(f"   📝 FEEDBACK:")
            for fb in feedback:
                print(f"      {fb}")
            
            print("   " + "-" * 80)
        
        # Overall statistics
        avg_score = total_score / len(scores)
        print(f"\n📊 OVERALL STATISTICS:")
        print("-" * 50)
        print(f"   Total Reports: {len(scores)}")
        print(f"   Average Score: {avg_score:.1f}/100")
        print(f"   Highest Score: {max(scores)}/100")
        print(f"   Lowest Score: {min(scores)}/100")
        
        # Grade distribution
        print(f"\n🏆 GRADE DISTRIBUTION:")
        a_plus = sum(1 for s in scores if s >= 90)
        a = sum(1 for s in scores if 80 <= s < 90)
        b_plus = sum(1 for s in scores if 70 <= s < 80)
        b = sum(1 for s in scores if 60 <= s < 70)
        c = sum(1 for s in scores if s < 60)
        
        print(f"   A+ (90-100): {a_plus} reports")
        print(f"   A  (80-89):  {a} reports")
        print(f"   B+ (70-79):  {b_plus} reports")
        print(f"   B  (60-69):  {b} reports")
        print(f"   C  (<60):    {c} reports")
        
        print(f"\n💾 Results saved to: comprehensive_test_results_20250819_143020.json")
        
    except FileNotFoundError:
        print("❌ Test results file not found!")
        print("Run the comprehensive test function first.")
    except Exception as e:
        print(f"❌ Error analyzing results: {e}")

if __name__ == "__main__":
    analyze_and_score_reports()
