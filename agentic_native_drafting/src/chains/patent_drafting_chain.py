from src.interfaces import Chain
from src.tools.disclosure_tools import DisclosureAssessmentTool
from src.tools.claim_drafting_tool import ClaimDraftingTool
from src.tools.claim_review_tool import ClaimReviewTool
from typing import Dict, Any, AsyncGenerator, List, Optional
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class PatentDraftingChain(Chain):
    """
    Comprehensive patent drafting workflow chain.
    
    This chain orchestrates:
    1. Disclosure assessment and sufficiency check
    2. Claim drafting based on disclosure
    3. Claim review and quality assessment
    4. Iterative improvement recommendations
    
    The chain provides a complete workflow from invention disclosure
    to draft patent claims ready for review.
    """
    
    def __init__(self):
        self.disclosure_tool = DisclosureAssessmentTool()
        self.claim_drafting_tool = ClaimDraftingTool()
        self.claim_review_tool = ClaimReviewTool()
        
        # Chain configuration
        self.max_iterations = 3
        self.quality_threshold = 0.7
        self.enable_iterative_improvement = True
        
    async def execute(
        self, 
        invention_disclosure: str, 
        document_context: str = "", 
        conversation_history: str = "",
        **kwargs
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Execute the complete patent drafting workflow.
        
        Args:
            invention_disclosure: The invention disclosure text
            document_context: Additional document context
            conversation_history: Previous conversation context
            **kwargs: Additional parameters including:
                - max_claims: Maximum number of claims to draft
                - claim_types: Types of claims to include
                - focus_areas: Specific technical areas to focus on
                - prior_art_context: Known prior art information
                - enable_iterative_improvement: Whether to enable iterative improvement
        
        Yields:
            Dict containing workflow progress, intermediate results, and final output
        """
        try:
            # Initialize workflow state
            workflow_state = {
                "start_time": datetime.now().isoformat(),
                "current_step": "initialized",
                "disclosure_assessment": None,
                "drafted_claims": None,
                "claim_review": None,
                "iterations": [],
                "final_result": None,
                "errors": []
            }
            
            logger.info(f"Starting patent drafting chain for disclosure of length {len(invention_disclosure)}")
            
            # Step 1: Disclosure Assessment
            yield await self._yield_progress("disclosure_assessment", "Assessing disclosure sufficiency...", workflow_state)
            
            try:
                disclosure_result = await self.disclosure_tool.run(
                    invention_disclosure, 
                    document_context, 
                    conversation_history
                )
                workflow_state["disclosure_assessment"] = disclosure_result
                workflow_state["current_step"] = "disclosure_assessed"
                
                yield await self._yield_progress("disclosure_assessed", "Disclosure assessment completed", workflow_state)
                
                # Check if disclosure is sufficient
                if disclosure_result.get("status") == "success":
                    sufficiency_score = disclosure_result.get("assessment", {}).get("sufficiency_score", 0.0)
                    if sufficiency_score < 0.5:
                        yield await self._yield_progress(
                            "disclosure_warning", 
                            f"Disclosure sufficiency score is low ({sufficiency_score:.2f}). Consider enhancing the disclosure.",
                            workflow_state
                        )
                else:
                    yield await self._yield_progress(
                        "disclosure_error", 
                        "Disclosure assessment failed. Proceeding with basic assessment.",
                        workflow_state
                    )
                    
            except Exception as e:
                error_msg = f"Disclosure assessment failed: {str(e)}"
                logger.error(error_msg)
                workflow_state["errors"].append(error_msg)
                yield await self._yield_progress("disclosure_error", error_msg, workflow_state)
            
            # Step 2: Claim Drafting
            yield await self._yield_progress("claim_drafting", "Drafting patent claims...", workflow_state)
            
            try:
                # Extract parameters for claim drafting
                max_claims = kwargs.get('max_claims', 20)
                claim_types = kwargs.get('claim_types', ["independent", "dependent"])
                focus_areas = kwargs.get('focus_areas', [])
                prior_art_context = kwargs.get('prior_art_context', "")
                
                # Get disclosure assessment insights for claim drafting
                disclosure_insights = ""
                if workflow_state["disclosure_assessment"]:
                    assessment = workflow_state["disclosure_assessment"].get("assessment", {})
                    if assessment.get("recommendations"):
                        disclosure_insights = f"Disclosure insights: {'; '.join(assessment['recommendations'])}"
                
                # Draft claims
                claims_result = await self.claim_drafting_tool.run(
                    invention_disclosure,
                    document_context,
                    conversation_history,
                    max_claims=max_claims,
                    claim_types=claim_types,
                    focus_areas=focus_areas,
                    prior_art_context=prior_art_context,
                    assess_disclosure=False  # Already done above
                )
                
                workflow_state["drafted_claims"] = claims_result
                workflow_state["current_step"] = "claims_drafted"
                
                if claims_result.get("status") == "success":
                    claims_count = claims_result.get("claims_generated", 0)
                    yield await self._yield_progress(
                        "claims_drafted", 
                        f"Successfully drafted {claims_count} claims",
                        workflow_state
                    )
                else:
                    yield await self._yield_progress(
                        "claims_error", 
                        "Claim drafting failed. No claims generated.",
                        workflow_state
                    )
                    
            except Exception as e:
                error_msg = f"Claim drafting failed: {str(e)}"
                logger.error(error_msg)
                workflow_state["errors"].append(error_msg)
                yield await self._yield_progress("claims_error", error_msg, workflow_state)
            
            # Step 3: Claim Review
            yield await self._yield_progress("claim_review", "Reviewing drafted claims...", workflow_state)
            
            try:
                if workflow_state["drafted_claims"] and workflow_state["drafted_claims"].get("claims"):
                    claims = workflow_state["drafted_claims"]["claims"]
                    
                    review_result = await self.claim_review_tool.run(
                        claims,
                        prior_art_context=kwargs.get('prior_art_context', ""),
                        invention_disclosure=invention_disclosure,
                        review_type="comprehensive"
                    )
                    
                    workflow_state["claim_review"] = review_result
                    workflow_state["current_step"] = "claims_reviewed"
                    
                    if review_result.get("status") == "success":
                        quality_score = review_result.get("summary", {}).get("overall_quality_score", 0.0)
                        yield await self._yield_progress(
                            "claims_reviewed", 
                            f"Claim review completed. Overall quality score: {quality_score:.2f}",
                            workflow_state
                        )
                    else:
                        yield await self._yield_progress(
                            "review_error", 
                            "Claim review failed. Proceeding without detailed review.",
                            workflow_state
                        )
                else:
                    yield await self._yield_progress(
                        "review_skipped", 
                        "No claims to review. Skipping review step.",
                        workflow_state
                    )
                    
            except Exception as e:
                error_msg = f"Claim review failed: {str(e)}"
                logger.error(error_msg)
                workflow_state["errors"].append(error_msg)
                yield await self._yield_progress("review_error", error_msg, workflow_state)
            
            # Step 4: Iterative Improvement (if enabled)
            if kwargs.get('enable_iterative_improvement', self.enable_iterative_improvement):
                yield await self._yield_progress("improvement", "Starting iterative improvement process...", workflow_state)
                
                try:
                    improvement_result = await self._perform_iterative_improvement(
                        invention_disclosure, 
                        workflow_state, 
                        kwargs
                    )
                    workflow_state["iterations"] = improvement_result
                    workflow_state["current_step"] = "improvement_completed"
                    
                    yield await self._yield_progress(
                        "improvement_completed", 
                        f"Iterative improvement completed with {len(improvement_result)} iterations",
                        workflow_state
                    )
                    
                except Exception as e:
                    error_msg = f"Iterative improvement failed: {str(e)}"
                    logger.error(error_msg)
                    workflow_state["errors"].append(error_msg)
                    yield await self._yield_progress("improvement_error", error_msg, workflow_state)
            
            # Step 5: Final Result Compilation
            yield await self._yield_progress("finalizing", "Compiling final results...", workflow_state)
            
            try:
                final_result = self._compile_final_result(workflow_state, invention_disclosure)
                workflow_state["final_result"] = final_result
                workflow_state["current_step"] = "completed"
                workflow_state["end_time"] = datetime.now().isoformat()
                
                yield await self._yield_progress(
                    "completed", 
                    "Patent drafting workflow completed successfully",
                    workflow_state
                )
                
                # Yield final result
                yield {
                    "type": "final_result",
                    "workflow_state": workflow_state,
                    "final_result": final_result,
                    "timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                error_msg = f"Final result compilation failed: {str(e)}"
                logger.error(error_msg)
                workflow_state["errors"].append(error_msg)
                yield await self._yield_progress("finalization_error", error_msg, workflow_state)
                
        except Exception as e:
            error_msg = f"Patent drafting chain execution failed: {str(e)}"
            logger.error(error_msg)
            yield {
                "type": "error",
                "error": error_msg,
                "timestamp": datetime.now().isoformat(),
                "workflow_state": workflow_state if 'workflow_state' in locals() else {}
            }
    
    async def _yield_progress(self, step: str, message: str, workflow_state: Dict) -> Dict[str, Any]:
        """Yield a progress update with current workflow state"""
        return {
            "type": "progress",
            "step": step,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "workflow_state": workflow_state
        }
    
    async def _perform_iterative_improvement(
        self, 
        invention_disclosure: str, 
        workflow_state: Dict, 
        kwargs: Dict
    ) -> List[Dict[str, Any]]:
        """Perform iterative improvement of claims based on review feedback"""
        iterations = []
        current_claims = workflow_state.get("drafted_claims", {}).get("claims", [])
        
        if not current_claims:
            return iterations
        
        for iteration in range(1, self.max_iterations + 1):
            try:
                logger.info(f"Starting iteration {iteration} of claim improvement")
                
                # Get improvement suggestions from previous review
                if workflow_state.get("claim_review") and workflow_state["claim_review"].get("recommendations"):
                    recommendations = workflow_state["claim_review"]["recommendations"]
                    
                    # Create improvement prompt based on recommendations
                    improvement_prompt = self._create_improvement_prompt(
                        current_claims, recommendations, invention_disclosure
                    )
                    
                    # Attempt to improve claims
                    improved_claims = await self._improve_claims(
                        current_claims, improvement_prompt, kwargs
                    )
                    
                    if improved_claims and improved_claims != current_claims:
                        # Review improved claims
                        review_result = await self.claim_review_tool.run(
                            improved_claims,
                            prior_art_context=kwargs.get('prior_art_context', ""),
                            invention_disclosure=invention_disclosure,
                            review_type="comprehensive"
                        )
                        
                        iteration_result = {
                            "iteration": iteration,
                            "original_claims": current_claims,
                            "improved_claims": improved_claims,
                            "review_result": review_result,
                            "improvement_applied": True
                        }
                        
                        current_claims = improved_claims
                        
                        # Check if quality threshold is met
                        quality_score = review_result.get("summary", {}).get("overall_quality_score", 0.0)
                        if quality_score >= self.quality_threshold:
                            logger.info(f"Quality threshold met ({quality_score:.2f} >= {self.quality_threshold}). Stopping iterations.")
                            break
                    else:
                        iteration_result = {
                            "iteration": iteration,
                            "original_claims": current_claims,
                            "improved_claims": current_claims,
                            "review_result": None,
                            "improvement_applied": False,
                            "reason": "No improvements made"
                        }
                        
                        # If no improvements, stop iterations
                        break
                    
                    iterations.append(iteration_result)
                    
                else:
                    # No recommendations available, stop iterations
                    break
                    
            except Exception as e:
                logger.warning(f"Iteration {iteration} failed: {e}")
                iterations.append({
                    "iteration": iteration,
                    "error": str(e),
                    "improvement_applied": False
                })
                break
        
        return iterations
    
    def _create_improvement_prompt(
        self, 
        claims: List[Dict], 
        recommendations: Dict, 
        invention_disclosure: str
    ) -> str:
        """Create a prompt for improving claims based on recommendations"""
        prompt = f"Based on the following recommendations, improve the patent claims:\n\n"
        
        for category, recs in recommendations.items():
            if recs:
                prompt += f"{category.upper()}:\n"
                for rec in recs:
                    prompt += f"- {rec}\n"
                prompt += "\n"
        
        prompt += f"\nOriginal claims:\n"
        for claim in claims:
            prompt += f"Claim {claim.get('claim_number', '?')}: {claim.get('claim_text', '')}\n"
        
        prompt += f"\nInvention disclosure context:\n{invention_disclosure[:500]}...\n\n"
        prompt += "Please provide improved versions of the claims addressing the recommendations above."
        
        return prompt
    
    async def _improve_claims(
        self, 
        current_claims: List[Dict], 
        improvement_prompt: str, 
        kwargs: Dict
    ) -> List[Dict]:
        """Attempt to improve claims based on the improvement prompt"""
        try:
            # Use the claim drafting tool with the improvement prompt
            # This is a simplified approach - in a real implementation, you might
            # want to use a more sophisticated improvement mechanism
            
            # For now, return the current claims (no improvement)
            # In a real implementation, you would call an LLM to improve the claims
            return current_claims
            
        except Exception as e:
            logger.warning(f"Claim improvement failed: {e}")
            return current_claims
    
    def _compile_final_result(self, workflow_state: Dict, invention_disclosure: str) -> Dict[str, Any]:
        """Compile the final result from the workflow"""
        try:
            final_result = {
                "workflow_summary": {
                    "status": "completed",
                    "start_time": workflow_state.get("start_time"),
                    "end_time": workflow_state.get("end_time"),
                    "total_steps": 5,
                    "completed_steps": len([s for s in workflow_state.values() if s is not None]),
                    "errors": len(workflow_state.get("errors", []))
                },
                "disclosure_assessment": workflow_state.get("disclosure_assessment"),
                "drafted_claims": workflow_state.get("drafted_claims"),
                "claim_review": workflow_state.get("claim_review"),
                "iterative_improvements": {
                    "iterations_performed": len(workflow_state.get("iterations", [])),
                    "final_quality_score": None
                },
                "recommendations": {
                    "next_steps": [],
                    "priority_actions": []
                }
            }
            
            # Extract final quality score
            if workflow_state.get("claim_review"):
                final_result["iterative_improvements"]["final_quality_score"] = \
                    workflow_state["claim_review"].get("summary", {}).get("overall_quality_score")
            
            # Generate final recommendations
            if workflow_state.get("claim_review") and workflow_state["claim_review"].get("recommendations"):
                recommendations = workflow_state["claim_review"]["recommendations"]
                
                # High priority actions
                if recommendations.get("patentability"):
                    final_result["recommendations"]["priority_actions"].extend(recommendations["patentability"])
                
                if recommendations.get("claim_quality"):
                    final_result["recommendations"]["priority_actions"].extend(recommendations["claim_quality"])
                
                # Next steps
                if workflow_state.get("claim_review") and workflow_state["claim_review"].get("next_steps"):
                    final_result["recommendations"]["next_steps"] = workflow_state["claim_review"]["next_steps"]
            
            return final_result
            
        except Exception as e:
            logger.error(f"Final result compilation failed: {e}")
            return {
                "error": f"Final result compilation failed: {str(e)}",
                "workflow_state": workflow_state
            }
    
    async def get_workflow_status(self) -> Dict[str, Any]:
        """Get the current status of the workflow"""
        return {
            "chain_type": "PatentDraftingChain",
            "version": "1.0.0",
            "max_iterations": self.max_iterations,
            "quality_threshold": self.quality_threshold,
            "tools_available": [
                "DisclosureAssessmentTool",
                "ClaimDraftingTool", 
                "ClaimReviewTool"
            ],
            "workflow_steps": [
                "Disclosure Assessment",
                "Claim Drafting",
                "Claim Review",
                "Iterative Improvement",
                "Final Compilation"
            ]
        }
