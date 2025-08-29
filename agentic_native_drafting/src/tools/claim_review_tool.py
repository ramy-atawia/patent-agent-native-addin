from src.interfaces import Tool
from src.utils.response_standardizer import create_thought_event, create_results_event, create_error_event
from typing import Dict, Any, List, Optional, AsyncGenerator
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ContentReviewTool(Tool):
    """
    Comprehensive content review and analysis tool.
    
    This tool provides:
    - Content validity assessment
    - Prior content conflict detection
    - Content improvement recommendations
    - Quality analysis
    - Content scope optimization
    """
    
    def __init__(self):
        self.max_content_items_per_review = 50
        self.content_quality_thresholds = {
            "min_words": 5,
            "max_words": 200,
            "min_technical_terms": 2,
            "max_dependent_depth": 5
        }
        
    async def run(self, content_items: List[Dict], prior_content_context: str = "", original_content: str = "", **kwargs) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Review and analyze content items comprehensively.
        
        Args:
            content_items: List of content dictionaries to review
            prior_content_context: Known prior content information
            original_content: The original content disclosure
            **kwargs: Additional parameters including:
                - review_type: Type of review ("basic", "comprehensive", "expert")
                - focus_areas: Specific areas to focus on
                - content_standards: Target content standards for compliance
        
        Yields:
            Streaming events in standardized format
        """
        try:
            # Validate inputs
            self._validate_inputs(content_items)
            
            if len(content_items) > self.max_content_items_per_review:
                logger.warning(f"Content items list exceeds maximum ({len(content_items)} > {self.max_content_items_per_review}). Truncating.")
                content_items = content_items[:self.max_content_items_per_review]
            
            # Extract parameters
            review_type = kwargs.get('review_type', 'comprehensive')
            focus_areas = kwargs.get('focus_areas', [])
            content_standards = kwargs.get('content_standards', 'General')
            
            logger.info(f"Starting content review for {len(content_items)} items. Review type: {review_type}")
            
            # Yield progress event
            yield create_thought_event(
                content=f"Starting comprehensive content review for {len(content_items)} items",
                thought_type="initialization",
                metadata={"total_content_items": len(content_items), "review_type": review_type}
            )
            
            # Perform content analysis
            yield create_thought_event(
                content="Analyzing individual content items for quality and structure...",
                thought_type="analysis"
            )
            
            content_analysis = await self._analyze_content_items(content_items, original_content)
            
            # Assess quality
            yield create_thought_event(
                content="Assessing quality and prior content conflicts...",
                thought_type="quality_assessment"
            )
            
            quality_assessment = await self._assess_quality(content_items, prior_content_context, original_content)
            
            # Generate recommendations
            yield create_thought_event(
                content="Generating improvement recommendations...",
                thought_type="recommendations"
            )
            
            recommendations = self._generate_recommendations(content_analysis, quality_assessment, focus_areas)
            
            # Risk assessment
            yield create_thought_event(
                content="Assessing potential risks and issues...",
                thought_type="risk_assessment"
            )
            
            risk_assessment = self._assess_risks(content_analysis, quality_assessment)
            
            # Create metadata
            metadata = {
                "tool_name": "ContentReviewTool",
                "review_type": review_type,
                "content_standards": content_standards,
                "total_content_items_reviewed": len(content_items),
                "timestamp": datetime.now().isoformat()
            }
            
            # Create data payload
            data = {
                "content_analysis": content_analysis,
                "quality_assessment": quality_assessment,
                "recommendations": recommendations,
                "risk_assessment": risk_assessment,
                "content_items_reviewed": content_items
            }
            
            # Generate response content
            response_content = f"Content review completed successfully. Analyzed {len(content_items)} items with {len(recommendations.get('improvements', []))} improvement recommendations."
            
            logger.info(f"Content review completed successfully for {len(content_items)} items")
            
            # Yield final results event
            yield create_results_event(
                response=response_content,
                metadata=metadata,
                data=data
            )
            
        except Exception as e:
            logger.error(f"Content review failed: {e}")
            yield create_error_event(
                error=str(e),
                context="content_review_error",
                metadata={"total_content_items": len(content_items) if content_items else 0}
            )
    
    def _validate_inputs(self, content_items: List[Dict]) -> None:
        """Validate input parameters for content review"""
        if not content_items:
            raise ValueError("Content items list cannot be empty")
        
        if not isinstance(content_items, list):
            raise ValueError("Content items must be a list")
        
        if len(content_items) > self.max_content_items_per_review:
            raise ValueError(f"Content items list exceeds maximum allowed ({self.max_content_items_per_review})")
    
    async def _analyze_content_items(self, content_items: List[Dict], original_content: str) -> Dict[str, Any]:
        """Analyze individual content items for quality and structure"""
        analysis = {
            "total_content_items": len(content_items),
            "independent_items": [],
            "dependent_items": [],
            "content_quality_scores": [],
            "structural_issues": [],
            "technical_coverage": {},
            "content_dependencies": {}
        }
        
        for i, content_item in enumerate(content_items):
            try:
                # Extract technical terms
                technical_terms = self._extract_technical_terms(content_item.get("content_text", ""))
                
                # Identify technical areas
                technical_areas = self._identify_technical_areas(content_item.get("content_text", ""))
                
                # Calculate quality score
                quality_score = self._calculate_claim_quality_score(content_item, technical_terms, technical_areas)
                
                # Identify issues
                issues = self._identify_content_issues(content_item, technical_terms)
                
                # Analyze structure
                structure = self._analyze_content_structure(content_item)
                
                # Categorize content item
                if content_item.get("content_type") == "independent":
                    analysis["independent_items"].append({
                        "index": i,
                        "content_text": content_item.get("content_text", ""),
                        "technical_terms": technical_terms,
                        "technical_areas": technical_areas,
                        "quality_score": quality_score,
                        "issues": issues,
                        "structure": structure
                    })
                else:
                    analysis["dependent_items"].append({
                        "index": i,
                        "content_text": content_item.get("content_text", ""),
                        "dependency": content_item.get("dependency", ""),
                        "technical_terms": technical_terms,
                        "technical_areas": technical_areas,
                        "quality_score": quality_score,
                        "issues": issues,
                        "structure": structure
                    })
                
                analysis["content_quality_scores"].append(quality_score)
                
                # Update technical coverage
                for area in technical_areas:
                    if area not in analysis["technical_coverage"]:
                        analysis["technical_coverage"][area] = 0
                    analysis["technical_coverage"][area] += 1
                
                # Track dependencies
                if content_item.get("dependency"):
                    dep = content_item["dependency"]
                    if dep not in analysis["content_dependencies"]:
                        analysis["content_dependencies"][dep] = []
                    analysis["content_dependencies"][dep].append(i)
                
            except Exception as e:
                logger.warning(f"Failed to analyze claim {i}: {e}")
                analysis["structural_issues"].append(f"Claim {i}: Analysis failed - {str(e)}")
                continue
        
        # Calculate summary statistics
        if analysis["content_quality_scores"]:
            analysis["average_quality_score"] = sum(analysis["content_quality_scores"]) / len(analysis["content_quality_scores"])
            analysis["min_quality_score"] = min(analysis["content_quality_scores"])
            analysis["max_quality_score"] = max(analysis["content_quality_scores"])
        
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
    
    def _identify_content_issues(self, content_item: Dict, technical_terms: List[str]) -> List[str]:
        """Identify potential issues with the content item"""
        issues = []
        
        content_text = content_item.get("content_text", "")
        if not content_text:
            issues.append("Missing content text")
            return issues
        
        # Check for basic content issues
        word_count = len(content_text.split())
        if word_count < 5:
            issues.append("Content too brief - insufficient detail")
        elif word_count > 200:
            issues.append("Content too verbose - may be unclear")
        
        # Check for technical content
        if len(technical_terms) < 2:
            issues.append("Insufficient technical terminology")
        
        # Check for structural issues
        if not content_text.strip().endswith('.'):
            issues.append("Content should end with proper punctuation")
        
        # Check for clarity issues
        if any(word in content_text.lower() for word in ["wherein", "thereof", "thereby"]):
            if word_count < 15:
                issues.append("Complex language used without sufficient context")
        
        return issues
    
    def _analyze_content_structure(self, content_item: Dict) -> Dict[str, Any]:
        """Analyze the structural elements of the content item"""
        content_text = content_item.get("content_text", "")
        
        structure = {
            "preamble": "",
            "clauses": [],
            "wherein_clauses": [],
            "dependent_elements": []
        }
        
        # Simple clause analysis
        clauses = content_text.split(',')
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
    
    async def _assess_quality(self, content_items: List[Dict], prior_content_context: str, original_content: str) -> Dict[str, Any]:
        """Assess the quality of the content items"""
        assessment = {
            "overall_quality": "unknown",
            "confidence_score": 0.5,
            "key_factors": [],
            "prior_content_risks": [],
            "recommendations": []
        }
        
        # Basic assessment based on content sufficiency
        if original_content and len(original_content.split()) > 50:
            assessment["overall_quality"] = "likely_high_quality"
            assessment["confidence_score"] = 0.7
            assessment["key_factors"].append("Sufficient content provided")
        else:
            assessment["overall_quality"] = "insufficient_content"
            assessment["confidence_score"] = 0.3
            assessment["key_factors"].append("Insufficient content for quality assessment")
            assessment["recommendations"].append("Provide more detailed content description")
        
        # Check for prior content context
        if prior_content_context:
            assessment["prior_content_risks"].append("Prior content context provided - requires detailed analysis")
            assessment["confidence_score"] = min(assessment["confidence_score"], 0.6)
        
        # Check content quality
        if content_items:
            quality_scores = []
            for content_item in content_items:
                technical_terms = self._extract_technical_terms(content_item.get("content_text", ""))
                technical_areas = self._identify_technical_areas(content_item.get("content_text", ""))
                quality_score = self._calculate_claim_quality_score(content_item, technical_terms, technical_areas)
                quality_scores.append(quality_score)
            
            if quality_scores:
                avg_quality = sum(quality_scores) / len(quality_scores)
                if avg_quality > 0.7:
                    assessment["key_factors"].append("High quality content")
                    assessment["confidence_score"] = min(1.0, assessment["confidence_score"] + 0.1)
                elif avg_quality < 0.4:
                    assessment["key_factors"].append("Low quality content")
                    assessment["confidence_score"] = max(0.1, assessment["confidence_score"] - 0.2)
                    assessment["recommendations"].append("Improve content quality and technical content")
        
        return assessment
    
    def _generate_recommendations(self, content_analysis: Dict, quality_assessment: Dict, focus_areas: List[str]) -> Dict[str, Any]:
        """Generate improvement recommendations based on analysis"""
        recommendations = {
            "improvements": [],
            "priorities": [],
            "focus_area_suggestions": {}
        }
        
        # Content quality improvements
        if content_analysis.get("average_quality_score", 0) < 0.6:
            recommendations["improvements"].append("Improve overall content quality")
            recommendations["priorities"].append("high")
        
        # Independent content items
        if len(content_analysis.get("independent_items", [])) == 0:
            recommendations["improvements"].append("Add independent content items")
            recommendations["priorities"].append("critical")
        elif len(content_analysis.get("independent_items", [])) < 2:
            recommendations["improvements"].append("Consider adding more independent content items for broader coverage")
            recommendations["priorities"].append("medium")
        
        # Dependent content items
        if len(content_analysis.get("dependent_items", [])) == 0:
            recommendations["improvements"].append("Add dependent content items for comprehensive coverage")
            recommendations["priorities"].append("high")
        
        # Technical coverage
        technical_coverage = content_analysis.get("technical_coverage", {})
        if len(technical_coverage) < 2:
            recommendations["improvements"].append("Expand technical coverage across multiple areas")
            recommendations["priorities"].append("medium")
        
        # Focus area specific recommendations
        for focus_area in focus_areas:
            if focus_area not in technical_coverage:
                recommendations["focus_area_suggestions"][focus_area] = f"Add content covering {focus_area} technology"
        
        # Quality recommendations
        if quality_assessment.get("overall_quality") == "insufficient_content":
            recommendations["improvements"].append("Enhance content with more technical details")
            recommendations["priorities"].append("critical")
        
        return recommendations
    
    def _assess_risks(self, content_analysis: Dict, quality_assessment: Dict) -> Dict[str, Any]:
        """Assess potential risks and issues"""
        risks = {
            "high_risk": [],
            "medium_risk": [],
            "low_risk": [],
            "mitigation_strategies": []
        }
        
        # Quality risks
        if content_analysis.get("average_quality_score", 0) < 0.4:
            risks["high_risk"].append("Very low content quality may lead to rejection")
            risks["mitigation_strategies"].append("Improve content drafting and technical content")
        
        # Coverage risks
        if len(content_analysis.get("independent_items", [])) == 0:
            risks["critical_risk"] = ["No independent content - fundamental content issue"]
            risks["mitigation_strategies"].append("Draft at least one strong independent content item")
        
        # Technical coverage risks
        technical_coverage = content_analysis.get("technical_coverage", {})
        if len(technical_coverage) < 2:
            risks["medium_risk"].append("Limited technical coverage may reduce content value")
            risks["mitigation_strategies"].append("Expand content to cover multiple technical aspects")
        
        # Quality risks
        if quality_assessment.get("confidence_score", 0) < 0.4:
            risks["high_risk"].append("Low quality confidence")
            risks["mitigation_strategies"].append("Conduct thorough prior content search and improve disclosure")
        
        return risks
