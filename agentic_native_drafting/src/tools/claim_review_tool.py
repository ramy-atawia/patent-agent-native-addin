from src.interfaces import Tool
from src.utils.response_standardizer import create_thought_event, create_results_event, create_error_event
from typing import Dict, Any, List, Optional, AsyncGenerator
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ClaimReviewTool(Tool):
    """
    Comprehensive patent claim review and analysis tool.
    
    This tool provides:
    - Claim validity assessment
    - Prior art conflict detection
    - Claim improvement recommendations
    - Patentability analysis
    - Claim scope optimization
    """
    
    def __init__(self):
        self.max_claims_per_review = 50
        self.claim_quality_thresholds = {
            "min_words": 5,
            "max_words": 200,
            "min_technical_terms": 2,
            "max_dependent_depth": 5
        }
        
    async def run(self, claims: List[Dict], prior_art_context: str = "", invention_disclosure: str = "", **kwargs) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Review and analyze patent claims comprehensively.
        
        Args:
            claims: List of claim dictionaries to review
            prior_art_context: Known prior art information
            invention_disclosure: The original invention disclosure
            **kwargs: Additional parameters including:
                - review_type: Type of review ("basic", "comprehensive", "expert")
                - focus_areas: Specific areas to focus on
                - patent_office: Target patent office for compliance
        
        Yields:
            Streaming events in standardized format
        """
        try:
            # Validate inputs
            self._validate_inputs(claims)
            
            if len(claims) > self.max_claims_per_review:
                logger.warning(f"Claims list exceeds maximum ({len(claims)} > {self.max_claims_per_review}). Truncating.")
                claims = claims[:self.max_claims_per_review]
            
            # Extract parameters
            review_type = kwargs.get('review_type', 'comprehensive')
            focus_areas = kwargs.get('focus_areas', [])
            patent_office = kwargs.get('patent_office', 'USPTO')
            
            logger.info(f"Starting claim review for {len(claims)} claims. Review type: {review_type}")
            
            # Yield progress event
            yield create_thought_event(
                content=f"Starting comprehensive claim review for {len(claims)} claims",
                thought_type="initialization",
                metadata={"total_claims": len(claims), "review_type": review_type}
            )
            
            # Perform claim analysis
            yield create_thought_event(
                content="Analyzing individual claims for quality and structure...",
                thought_type="analysis"
            )
            
            claim_analysis = await self._analyze_claims(claims, invention_disclosure)
            
            # Assess patentability
            yield create_thought_event(
                content="Assessing patentability and prior art conflicts...",
                thought_type="patentability_assessment"
            )
            
            patentability_assessment = await self._assess_patentability(claims, prior_art_context, invention_disclosure)
            
            # Generate recommendations
            yield create_thought_event(
                content="Generating improvement recommendations...",
                thought_type="recommendations"
            )
            
            recommendations = self._generate_recommendations(claim_analysis, patentability_assessment, focus_areas)
            
            # Risk assessment
            yield create_thought_event(
                content="Assessing potential risks and issues...",
                thought_type="risk_assessment"
            )
            
            risk_assessment = self._assess_risks(claim_analysis, patentability_assessment)
            
            # Create metadata
            metadata = {
                "tool_name": "ClaimReviewTool",
                "review_type": review_type,
                "patent_office": patent_office,
                "total_claims_reviewed": len(claims),
                "timestamp": datetime.now().isoformat()
            }
            
            # Create data payload
            data = {
                "claim_analysis": claim_analysis,
                "patentability_assessment": patentability_assessment,
                "recommendations": recommendations,
                "risk_assessment": risk_assessment,
                "claims_reviewed": claims
            }
            
            # Generate response content
            response_content = f"Claim review completed successfully. Analyzed {len(claims)} claims with {len(recommendations.get('improvements', []))} improvement recommendations."
            
            logger.info(f"Claim review completed successfully for {len(claims)} claims")
            
            # Yield final results event
            yield create_results_event(
                response=response_content,
                metadata=metadata,
                data=data
            )
            
        except Exception as e:
            logger.error(f"Claim review failed: {e}")
            yield create_error_event(
                error=str(e),
                context="claim_review_error",
                metadata={"total_claims": len(claims) if claims else 0}
            )
    
    def _validate_inputs(self, claims: List[Dict]) -> None:
        """Validate input parameters for claim review"""
        if not claims:
            raise ValueError("Claims list cannot be empty")
        
        if not isinstance(claims, list):
            raise ValueError("Claims must be a list")
        
        if len(claims) > self.max_claims_per_review:
            raise ValueError(f"Claims list exceeds maximum allowed ({self.max_claims_per_review})")
    
    async def _analyze_claims(self, claims: List[Dict], invention_disclosure: str) -> Dict[str, Any]:
        """Analyze individual claims for quality and structure"""
        analysis = {
            "total_claims": len(claims),
            "independent_claims": [],
            "dependent_claims": [],
            "claim_quality_scores": [],
            "structural_issues": [],
            "technical_coverage": {},
            "claim_dependencies": {}
        }
        
        for i, claim in enumerate(claims):
            try:
                # Extract technical terms
                technical_terms = self._extract_technical_terms(claim.get("claim_text", ""))
                
                # Identify technical areas
                technical_areas = self._identify_technical_areas(claim.get("claim_text", ""))
                
                # Calculate quality score
                quality_score = self._calculate_claim_quality_score(claim, technical_terms, technical_areas)
                
                # Identify issues
                issues = self._identify_claim_issues(claim, technical_terms)
                
                # Analyze structure
                structure = self._analyze_claim_structure(claim)
                
                # Categorize claim
                if claim.get("claim_type") == "independent":
                    analysis["independent_claims"].append({
                        "index": i,
                        "claim_text": claim.get("claim_text", ""),
                        "technical_terms": technical_terms,
                        "technical_areas": technical_areas,
                        "quality_score": quality_score,
                        "issues": issues,
                        "structure": structure
                    })
                else:
                    analysis["dependent_claims"].append({
                        "index": i,
                        "claim_text": claim.get("claim_text", ""),
                        "dependency": claim.get("dependency", ""),
                        "technical_terms": technical_terms,
                        "technical_areas": technical_areas,
                        "quality_score": quality_score,
                        "issues": issues,
                        "structure": structure
                    })
                
                analysis["claim_quality_scores"].append(quality_score)
                
                # Update technical coverage
                for area in technical_areas:
                    if area not in analysis["technical_coverage"]:
                        analysis["technical_coverage"][area] = 0
                    analysis["technical_coverage"][area] += 1
                
                # Track dependencies
                if claim.get("dependency"):
                    dep = claim["dependency"]
                    if dep not in analysis["claim_dependencies"]:
                        analysis["claim_dependencies"][dep] = []
                    analysis["claim_dependencies"][dep].append(i)
                
            except Exception as e:
                logger.warning(f"Failed to analyze claim {i}: {e}")
                analysis["structural_issues"].append(f"Claim {i}: Analysis failed - {str(e)}")
                continue
        
        # Calculate summary statistics
        if analysis["claim_quality_scores"]:
            analysis["average_quality_score"] = sum(analysis["claim_quality_scores"]) / len(analysis["claim_quality_scores"])
            analysis["min_quality_score"] = min(analysis["claim_quality_scores"])
            analysis["max_quality_score"] = max(analysis["claim_quality_scores"])
        
        return analysis
    
    def _extract_technical_terms(self, claim_text: str) -> List[str]:
        """Extract technical terms from claim text"""
        technical_indicators = [
            "method", "system", "apparatus", "device", "process", "technique",
            "algorithm", "protocol", "interface", "component", "module",
            "data", "signal", "network", "communication", "processing",
            "wireless", "sensor", "controller", "database", "server"
        ]
        
        text_lower = claim_text.lower()
        found_terms = [term for term in technical_indicators if term in text_lower]
        return found_terms
    
    def _identify_technical_areas(self, claim_text: str) -> List[str]:
        """Identify technical areas covered by the claim"""
        area_keywords = {
            "wireless_communication": ["wireless", "radio", "antenna", "frequency", "signal"],
            "data_processing": ["data", "process", "algorithm", "computation", "analysis"],
            "network_systems": ["network", "protocol", "routing", "packet", "connection"],
            "sensor_technology": ["sensor", "detector", "measurement", "monitoring"],
            "control_systems": ["controller", "automation", "regulation", "feedback"]
        }
        
        text_lower = claim_text.lower()
        identified_areas = []
        
        for area, keywords in area_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                identified_areas.append(area)
        
        return identified_areas
    
    def _calculate_claim_quality_score(self, claim: Dict, technical_terms: List[str], technical_areas: List[str]) -> float:
        """Calculate a quality score for the claim"""
        score = 0.0
        
        # Base score for having content
        if claim.get("claim_text"):
            score += 0.2
        
        # Technical terms bonus
        if len(technical_terms) >= 2:
            score += 0.3
        elif len(technical_terms) >= 1:
            score += 0.2
        
        # Technical areas coverage
        if len(technical_areas) >= 2:
            score += 0.2
        elif len(technical_areas) >= 1:
            score += 0.1
        
        # Claim type bonus
        if claim.get("claim_type") == "independent":
            score += 0.1
        
        # Length appropriateness
        claim_text = claim.get("claim_text", "")
        word_count = len(claim_text.split())
        if 10 <= word_count <= 100:
            score += 0.2
        elif 5 <= word_count <= 150:
            score += 0.1
        
        return min(1.0, score)
    
    def _identify_claim_issues(self, claim: Dict, technical_terms: List[str]) -> List[str]:
        """Identify potential issues with the claim"""
        issues = []
        claim_text = claim.get("claim_text", "")
        
        # Check length
        word_count = len(claim_text.split())
        if word_count < self.claim_quality_thresholds["min_words"]:
            issues.append("Claim is too short")
        elif word_count > self.claim_quality_thresholds["max_words"]:
            issues.append("Claim is too long")
        
        # Check technical content
        if len(technical_terms) < self.claim_quality_thresholds["min_technical_terms"]:
            issues.append("Insufficient technical terminology")
        
        # Check for proper ending
        if not claim_text.strip().endswith('.'):
            issues.append("Claim should end with a period")
        
        # Check for placeholder text
        placeholder_indicators = ["[describe", "[list", "[insert", "[specify"]
        if any(indicator in claim_text.lower() for indicator in placeholder_indicators):
            issues.append("Contains placeholder text")
        
        return issues
    
    def _analyze_claim_structure(self, claim: Dict) -> Dict[str, Any]:
        """Analyze the structural elements of the claim"""
        claim_text = claim.get("claim_text", "")
        
        structure = {
            "preamble": "",
            "clauses": [],
            "wherein_clauses": [],
            "dependent_elements": []
        }
        
        # Simple clause analysis
        clauses = claim_text.split(',')
        if clauses:
            structure["preamble"] = clauses[0].strip()
            structure["clauses"] = [clause.strip() for clause in clauses[1:] if clause.strip()]
        
        # Look for wherein clauses
        wherein_clauses = [clause for clause in structure["clauses"] if "wherein" in clause.lower()]
        structure["wherein_clauses"] = wherein_clauses
        
        # Look for dependent elements
        dependent_elements = [clause for clause in structure["clauses"] if any(word in clause.lower() for word in ["further", "additional", "wherein"])]
        structure["dependent_elements"] = dependent_elements
        
        return structure
    
    async def _assess_patentability(self, claims: List[Dict], prior_art_context: str, invention_disclosure: str) -> Dict[str, Any]:
        """Assess the patentability of the claims"""
        assessment = {
            "overall_patentability": "unknown",
            "confidence_score": 0.5,
            "key_factors": [],
            "prior_art_risks": [],
            "recommendations": []
        }
        
        # Basic assessment based on disclosure sufficiency
        if invention_disclosure and len(invention_disclosure.split()) > 50:
            assessment["overall_patentability"] = "likely_patentable"
            assessment["confidence_score"] = 0.7
            assessment["key_factors"].append("Sufficient disclosure provided")
        else:
            assessment["overall_patentability"] = "insufficient_disclosure"
            assessment["confidence_score"] = 0.3
            assessment["key_factors"].append("Insufficient disclosure for patentability assessment")
            assessment["recommendations"].append("Provide more detailed invention description")
        
        # Check for prior art context
        if prior_art_context:
            assessment["prior_art_risks"].append("Prior art context provided - requires detailed analysis")
            assessment["confidence_score"] = min(assessment["confidence_score"], 0.6)
        
        # Check claim quality
        if claims:
            quality_scores = []
            for claim in claims:
                technical_terms = self._extract_technical_terms(claim.get("claim_text", ""))
                technical_areas = self._identify_technical_areas(claim.get("claim_text", ""))
                quality_score = self._calculate_claim_quality_score(claim, technical_terms, technical_areas)
                quality_scores.append(quality_score)
            
            if quality_scores:
                avg_quality = sum(quality_scores) / len(quality_scores)
                if avg_quality > 0.7:
                    assessment["key_factors"].append("High quality claims")
                    assessment["confidence_score"] = min(1.0, assessment["confidence_score"] + 0.1)
                elif avg_quality < 0.4:
                    assessment["key_factors"].append("Low quality claims")
                    assessment["confidence_score"] = max(0.1, assessment["confidence_score"] - 0.2)
                    assessment["recommendations"].append("Improve claim quality and technical content")
        
        return assessment
    
    def _generate_recommendations(self, claim_analysis: Dict, patentability_assessment: Dict, focus_areas: List[str]) -> Dict[str, Any]:
        """Generate improvement recommendations based on analysis"""
        recommendations = {
            "improvements": [],
            "priorities": [],
            "focus_area_suggestions": {}
        }
        
        # Claim quality improvements
        if claim_analysis.get("average_quality_score", 0) < 0.6:
            recommendations["improvements"].append("Improve overall claim quality")
            recommendations["priorities"].append("high")
        
        # Independent claims
        if len(claim_analysis.get("independent_claims", [])) == 0:
            recommendations["improvements"].append("Add independent claims")
            recommendations["priorities"].append("critical")
        elif len(claim_analysis.get("independent_claims", [])) < 2:
            recommendations["improvements"].append("Consider adding more independent claims for broader coverage")
            recommendations["priorities"].append("medium")
        
        # Dependent claims
        if len(claim_analysis.get("dependent_claims", [])) == 0:
            recommendations["improvements"].append("Add dependent claims for comprehensive coverage")
            recommendations["priorities"].append("high")
        
        # Technical coverage
        technical_coverage = claim_analysis.get("technical_coverage", {})
        if len(technical_coverage) < 2:
            recommendations["improvements"].append("Expand technical coverage across multiple areas")
            recommendations["priorities"].append("medium")
        
        # Focus area specific recommendations
        for focus_area in focus_areas:
            if focus_area not in technical_coverage:
                recommendations["focus_area_suggestions"][focus_area] = f"Add claims covering {focus_area} technology"
        
        # Patentability recommendations
        if patentability_assessment.get("overall_patentability") == "insufficient_disclosure":
            recommendations["improvements"].append("Enhance invention disclosure with more technical details")
            recommendations["priorities"].append("critical")
        
        return recommendations
    
    def _assess_risks(self, claim_analysis: Dict, patentability_assessment: Dict) -> Dict[str, Any]:
        """Assess potential risks and issues"""
        risks = {
            "high_risk": [],
            "medium_risk": [],
            "low_risk": [],
            "mitigation_strategies": []
        }
        
        # Quality risks
        if claim_analysis.get("average_quality_score", 0) < 0.4:
            risks["high_risk"].append("Very low claim quality may lead to rejection")
            risks["mitigation_strategies"].append("Improve claim drafting and technical content")
        
        # Coverage risks
        if len(claim_analysis.get("independent_claims", [])) == 0:
            risks["critical_risk"] = ["No independent claims - fundamental patent issue"]
            risks["mitigation_strategies"].append("Draft at least one strong independent claim")
        
        # Technical coverage risks
        technical_coverage = claim_analysis.get("technical_coverage", {})
        if len(technical_coverage) < 2:
            risks["medium_risk"].append("Limited technical coverage may reduce patent value")
            risks["mitigation_strategies"].append("Expand claims to cover multiple technical aspects")
        
        # Patentability risks
        if patentability_assessment.get("confidence_score", 0) < 0.4:
            risks["high_risk"].append("Low patentability confidence")
            risks["mitigation_strategies"].append("Conduct thorough prior art search and improve disclosure")
        
        return risks
