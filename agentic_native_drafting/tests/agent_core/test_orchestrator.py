"""
Unit tests for AgentOrchestrator.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from src.agent_core.orchestrator import AgentOrchestrator


class TestAgentOrchestrator:
    """Test suite for AgentOrchestrator."""
    
    @pytest.fixture
    def orchestrator(self):
        """Create an AgentOrchestrator instance for testing."""
        return AgentOrchestrator()
    
    @pytest.fixture
    def sample_user_input(self):
        """Sample user input for testing."""
        return "I need help drafting patent claims for my wireless communication invention."
    
    @pytest.fixture
    def sample_context(self):
        """Sample context for testing."""
        return "This is a 5G spectrum sharing technology."
    
    @pytest.mark.unit
    def test_orchestrator_initialization(self, orchestrator):
        """Test orchestrator initialization and default values."""
        assert hasattr(orchestrator, 'tools')
        assert hasattr(orchestrator, 'chains')
        assert hasattr(orchestrator, 'conversation_memory')
        assert hasattr(orchestrator, 'intent_cache')
        assert orchestrator.max_memory_size == 100
        assert orchestrator.cache_ttl == 300
    
    @pytest.mark.unit
    def test_tools_available(self, orchestrator):
        """Test that required tools are available."""
        from agent import IntentType
        
        # Check that key tools are available
        assert IntentType.CLAIM_DRAFTING in orchestrator.tools
        assert IntentType.CLAIM_REVIEW in orchestrator.tools
        assert IntentType.PRIOR_ART_SEARCH in orchestrator.tools
        assert IntentType.GENERAL_CONVERSATION in orchestrator.tools
    
    @pytest.mark.unit
    def test_chains_available(self, orchestrator):
        """Test that required chains are available."""
        assert "patent_drafting" in orchestrator.chains
    
    @pytest.mark.unit
    def test_update_conversation_memory(self, orchestrator):
        """Test conversation memory update."""
        session_id = "test_session"
        user_input = "Hello"
        context = "Test context"
        
        orchestrator._update_conversation_memory(session_id, user_input, context)
        
        assert session_id in orchestrator.conversation_memory
        assert len(orchestrator.conversation_memory[session_id]) == 1
        
        memory_entry = orchestrator.conversation_memory[session_id][0]
        assert memory_entry["user_input"] == user_input
        assert memory_entry["context"] == context
        assert "timestamp" in memory_entry
    
    @pytest.mark.unit
    def test_update_conversation_memory_limit(self, orchestrator):
        """Test conversation memory size limit."""
        session_id = "test_session"
        
        # Add more entries than the limit
        for i in range(150):
            orchestrator._update_conversation_memory(session_id, f"Input {i}", f"Context {i}")
        
        # Should be limited to max_memory_size
        assert len(orchestrator.conversation_memory[session_id]) == orchestrator.max_memory_size
        
        # Should keep the most recent entries
        latest_entry = orchestrator.conversation_memory[session_id][-1]
        assert "Input 149" in latest_entry["user_input"]
    
    @pytest.mark.unit
    def test_fallback_intent_classification(self, orchestrator):
        """Test fallback intent classification."""
        # Test claim drafting intent
        input_text = "I need to draft patent claims for my invention"
        result = orchestrator._fallback_intent_classification(input_text)
        
        assert result["intent"] == "claim_drafting"
        assert result["confidence"] == 0.7
        
        # Test prior art search intent
        input_text = "I need to search for prior art in wireless communication"
        result = orchestrator._fallback_intent_classification(input_text)
        
        assert result["intent"] == "prior_art_search"
        assert result["confidence"] == 0.8
        
        # Test general conversation intent
        input_text = "Hello, how are you?"
        result = orchestrator._fallback_intent_classification(input_text)
        
        assert result["intent"] == "general_conversation"
        assert result["confidence"] == 0.5
    
    @pytest.mark.unit
    def test_is_chain_workflow_explicit(self, orchestrator):
        """Test chain workflow detection with explicit parameters."""
        intent = "claim_drafting"
        user_input = "I need help with patent drafting"
        kwargs = {"use_chain": True}
        
        result = orchestrator._is_chain_workflow(intent, user_input, kwargs)
        assert result is True
    
    @pytest.mark.unit
    def test_is_chain_workflow_complex_request(self, orchestrator):
        """Test chain workflow detection with complex request indicators."""
        intent = "claim_drafting"
        user_input = "I need a complete workflow from disclosure to final claims"
        kwargs = {}
        
        result = orchestrator._is_chain_workflow(intent, user_input, kwargs)
        assert result is True
    
    @pytest.mark.unit
    def test_is_chain_workflow_simple_request(self, orchestrator):
        """Test chain workflow detection with simple request."""
        intent = "claim_drafting"
        user_input = "Draft a claim for my invention"
        kwargs = {}
        
        result = orchestrator._is_chain_workflow(intent, user_input, kwargs)
        assert result is False
    
    @pytest.mark.unit
    def test_select_chain_patent_drafting(self, orchestrator):
        """Test chain selection for patent drafting."""
        intent = "claim_drafting"
        user_input = "I need a complete workflow process"
        kwargs = {}
        
        chain_name = orchestrator._select_chain(intent, user_input, kwargs)
        assert chain_name == "patent_drafting"
    
    @pytest.mark.unit
    def test_select_chain_no_match(self, orchestrator):
        """Test chain selection when no chain matches."""
        intent = "general_conversation"
        user_input = "Hello"
        kwargs = {}
        
        chain_name = orchestrator._select_chain(intent, user_input, kwargs)
        assert chain_name is None
    
    @pytest.mark.unit
    def test_summarize_result_claims(self, orchestrator):
        """Test result summarization for claims."""
        result = {"claims_generated": 5, "status": "success"}
        summary = orchestrator._summarize_result(result)
        
        assert "Generated 5 claims" in summary
    
    @pytest.mark.unit
    def test_summarize_result_patents(self, orchestrator):
        """Test result summarization for patents."""
        result = {"total_patents_found": 10, "status": "success"}
        summary = orchestrator._summarize_result(result)
        
        assert "Found 10 patents" in summary
    
    @pytest.mark.unit
    def test_summarize_result_assessment(self, orchestrator):
        """Test result summarization for assessment."""
        result = {"assessment": {"sufficiency_score": 0.8}, "status": "success"}
        summary = orchestrator._summarize_result(result)
        
        assert "score 0.8" in summary
    
    @pytest.mark.unit
    def test_summarize_result_error(self, orchestrator):
        """Test result summarization for error."""
        result = {"status": "error", "error": {"message": "Something went wrong"}}
        summary = orchestrator._summarize_result(result)
        
        assert "Something went wrong" in summary
    
    @pytest.mark.unit
    def test_summarize_result_empty(self, orchestrator):
        """Test result summarization for empty result."""
        result = None
        summary = orchestrator._summarize_result(result)
        
        assert summary == "No result"
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_format_progress_response(self, orchestrator):
        """Test progress response formatting."""
        step = "test_step"
        message = "Test message"
        session_id = "test_session"
        metadata = {"key": "value"}
        
        response = await orchestrator._format_progress_response(step, message, session_id, metadata)
        
        assert response["type"] == "progress"
        assert response["step"] == step
        assert response["message"] == message
        assert response["session_id"] == session_id
        assert response["metadata"] == metadata
        assert "timestamp" in response
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_format_error_response(self, orchestrator):
        """Test error response formatting."""
        error_type = "test_error"
        error_message = "Test error message"
        session_id = "test_session"
        
        response = await orchestrator._format_progress_response(error_type, error_message, session_id)
        
        assert response["type"] == "error"
        assert response["error_type"] == error_type
        assert response["error_message"] == error_message
        assert response["session_id"] == session_id
        assert "timestamp" in response
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_get_orchestrator_status(self, orchestrator):
        """Test orchestrator status retrieval."""
        status = await orchestrator.get_orchestrator_status()
        
        assert status["status"] == "active"
        assert "timestamp" in status
        assert "tools_available" in status
        assert "chains_available" in status
        assert "active_sessions" in status
        assert "intent_cache_size" in status
        assert status["version"] == "2.0.0"
    
    @pytest.mark.unit
    def test_clear_conversation_memory_specific_session(self, orchestrator):
        """Test clearing conversation memory for specific session."""
        session_id = "test_session"
        orchestrator.conversation_memory[session_id] = [{"test": "data"}]
        
        orchestrator.clear_conversation_memory(session_id)
        
        assert session_id not in orchestrator.conversation_memory
    
    @pytest.mark.unit
    def test_clear_conversation_memory_all_sessions(self, orchestrator):
        """Test clearing all conversation memory."""
        orchestrator.conversation_memory["session1"] = [{"test": "data1"}]
        orchestrator.conversation_memory["session2"] = [{"test": "data2"}]
        
        orchestrator.clear_conversation_memory()
        
        assert len(orchestrator.conversation_memory) == 0
    
    @pytest.mark.unit
    def test_clear_intent_cache(self, orchestrator):
        """Test clearing intent classification cache."""
        orchestrator.intent_cache["test_key"] = {"result": "test"}
        
        orchestrator.clear_intent_cache()
        
        assert len(orchestrator.intent_cache) == 0
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    @patch('src.agent_core.orchestrator.agent')
    async def test_classify_intent_success(self, mock_agent, orchestrator):
        """Test successful intent classification."""
        # Mock the agent response
        mock_agent.classify_user_intent_streaming.return_value = [
            {"type": "intent_classified", "intent": "claim_drafting"}
        ]
        
        result = await orchestrator._classify_intent("test input", "test context", "test_session")
        
        assert result is not None
        assert result["intent"] == "claim_drafting"
        assert result["confidence"] == 0.8  # Default confidence
        assert "timestamp" in result
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    @patch('src.agent_core.orchestrator.agent')
    async def test_classify_intent_failure(self, mock_agent, orchestrator):
        """Test intent classification failure."""
        # Mock the agent failure
        mock_agent.classify_user_intent_streaming.side_effect = Exception("Agent failed")
        
        result = await orchestrator._classify_intent("test input", "test context", "test_session")
        
        # Should fall back to keyword-based classification
        assert result is not None
        assert "intent" in result
        assert "confidence" in result
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    @patch('src.agent_core.orchestrator.agent')
    async def test_classify_intent_cache(self, orchestrator):
        """Test intent classification caching."""
        # Mock the agent response
        from agent import IntentType
        
        # First call should use agent
        with patch.object(orchestrator, '_fallback_intent_classification') as mock_fallback:
            mock_fallback.return_value = {"intent": IntentType.CLAIM_DRAFTING, "confidence": 0.8}
            
            result1 = await orchestrator._classify_intent("test input", "test context", "test_session")
            result2 = await orchestrator._classify_intent("test input", "test context", "test_session")
            
            # Second call should use cache
            assert result1 == result2
            # Fallback should only be called once
            assert mock_fallback.call_count == 1
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_handle_success(self, orchestrator, sample_user_input, sample_context):
        """Test successful request handling."""
        # Mock intent classification
        with patch.object(orchestrator, '_classify_intent') as mock_classify:
            mock_classify.return_value = {
                "intent": "claim_drafting",
                "confidence": 0.8
            }
            
            # Mock tool execution
            with patch.object(orchestrator, '_execute_single_tool') as mock_execute:
                mock_execute.return_value = [
                    {"type": "tool_result", "result": {"status": "success"}}
                ]
                
                events = []
                async for event in orchestrator.handle(sample_user_input, sample_context):
                    events.append(event)
                
                # Should have progress events and tool result
                assert len(events) > 0
                assert any("intent_classified" in event.get("step", "") for event in events)
                assert any("tool_result" in event.get("type", "") for event in events)
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_handle_chain_workflow(self, orchestrator, sample_user_input, sample_context):
        """Test handling of chain workflow requests."""
        # Mock intent classification
        with patch.object(orchestrator, '_classify_intent') as mock_classify:
            mock_classify.return_value = {
                "intent": "claim_drafting",
                "confidence": 0.8
            }
            
            # Mock chain workflow detection
            with patch.object(orchestrator, '_is_chain_workflow') as mock_detect:
                mock_detect.return_value = True
                
                # Mock chain execution
                with patch.object(orchestrator, '_execute_chain_workflow') as mock_execute:
                    mock_execute.return_value = [
                        {"type": "chain_result", "result": {"status": "success"}}
                    ]
                    
                    events = []
                    async for event in orchestrator.handle(
                        sample_user_input, 
                        sample_context, 
                        use_chain=True
                    ):
                        events.append(event)
                    
                    # Should have chain workflow events
                    assert len(events) > 0
                    assert any("chain_workflow" in event.get("step", "") for event in events)
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_handle_intent_classification_failure(self, orchestrator, sample_user_input, sample_context):
        """Test handling when intent classification fails."""
        # Mock intent classification failure
        with patch.object(orchestrator, '_classify_intent') as mock_classify:
            mock_classify.return_value = None
            
            events = []
            async for event in orchestrator.handle(sample_user_input, sample_context):
                events.append(event)
            
            # Should have error event
            assert len(events) > 0
            assert any("error" in event.get("type", "") for event in events)
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_execute_single_tool_success(self, orchestrator):
        """Test successful single tool execution."""
        intent = "claim_drafting"
        user_input = "Draft claims"
        context = "Test context"
        session_id = "test_session"
        
        # Mock tool execution
        with patch.object(orchestrator, '_execute_single_tool') as mock_execute:
            mock_execute.return_value = [
                {"type": "tool_result", "result": {"status": "success"}}
            ]
            
            events = []
            async for event in orchestrator._execute_single_tool(
                intent, user_input, context, session_id
            ):
                events.append(event)
            
            # Should have tool execution events
            assert len(events) > 0
            assert any("tool_executing" in event.get("step", "") for event in events)
            assert any("tool_completed" in event.get("step", "") for event in events)
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_execute_single_tool_not_implemented(self, orchestrator):
        """Test single tool execution when tool is not implemented."""
        intent = "invention_analysis"  # Not implemented
        user_input = "Analyze invention"
        context = "Test context"
        session_id = "test_session"
        
        events = []
        async for event in orchestrator._execute_single_tool(
            intent, user_input, context, session_id
        ):
            events.append(event)
        
        # Should have error event
        assert len(events) > 0
        assert any("tool_not_implemented" in event.get("error_type", "") for event in events)
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_execute_chain_workflow_success(self, orchestrator):
        """Test successful chain workflow execution."""
        intent = "claim_drafting"
        user_input = "Complete workflow"
        context = "Test context"
        session_id = "test_session"
        
        # Mock chain execution
        with patch.object(orchestrator, '_execute_chain_workflow') as mock_execute:
            mock_execute.return_value = [
                {"type": "chain_result", "result": {"status": "success"}}
            ]
            
            events = []
            async for event in orchestrator._execute_chain_workflow(
                intent, user_input, context, session_id
            ):
                events.append(event)
            
            # Should have chain workflow events
            assert len(events) > 0
            assert any("chain_started" in event.get("step", "") for event in events)
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_execute_chain_workflow_no_chain(self, orchestrator):
        """Test chain workflow execution when no suitable chain is found."""
        intent = "general_conversation"
        user_input = "Hello"
        context = "Test context"
        session_id = "test_session"
        
        events = []
        async for event in orchestrator._execute_chain_workflow(
            intent, user_input, context, session_id
        ):
            events.append(event)
        
        # Should have error event
        assert len(events) > 0
        assert any("chain_selection_error" in event.get("error_type", "") for event in events)
