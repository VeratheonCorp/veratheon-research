"""Tests for management guidance agent."""

import pytest
from unittest.mock import patch, AsyncMock
from src.research.management_guidance.management_guidance_agent import (
    management_guidance_agent,
    _extract_transcript_content,
    _create_no_transcript_analysis,
    _create_error_analysis
)
from src.research.management_guidance.management_guidance_models import (
    ManagementGuidanceData,
    ManagementGuidanceAnalysis
)


class TestManagementGuidanceAgent:
    
    def test_extract_transcript_content_direct_key(self):
        """Test transcript content extraction with direct key."""
        transcript_data = {
            "transcript": "This is the earnings call transcript content..."
        }
        
        result = _extract_transcript_content(transcript_data)
        assert result == "This is the earnings call transcript content..."
    
    def test_extract_transcript_content_alternative_keys(self):
        """Test transcript content extraction with alternative keys."""
        transcript_data = {
            "content": "This is the content..."
        }
        
        result = _extract_transcript_content(transcript_data)
        assert result == "This is the content..."
    
    def test_extract_transcript_content_nested_structure(self):
        """Test transcript content extraction from nested structure."""
        transcript_data = {
            "metadata": {"source": "earnings_call"},
            "data": {
                "text": "This is nested transcript content that is long enough to be considered valid content..."
            }
        }
        
        result = _extract_transcript_content(transcript_data)
        assert "This is nested transcript content" in result
    
    def test_extract_transcript_content_empty(self):
        """Test transcript content extraction with empty data."""
        transcript_data = {}
        result = _extract_transcript_content(transcript_data)
        assert result == ""
    
    def test_create_no_transcript_analysis(self):
        """Test creation of analysis when no transcript is available."""
        result = _create_no_transcript_analysis("AAPL")
        
        assert isinstance(result, ManagementGuidanceAnalysis)
        assert result.symbol == "AAPL"
        assert result.transcript_available == False
        assert result.quarter_analyzed is None
        assert result.guidance_confidence == "low"
        assert result.consensus_validation_signal == "neutral"
        assert "No earnings call transcript available" in result.key_guidance_summary
    
    def test_create_error_analysis(self):
        """Test creation of analysis when an error occurs."""
        error_msg = "API connection failed"
        result = _create_error_analysis("AAPL", error_msg)
        
        assert isinstance(result, ManagementGuidanceAnalysis)
        assert result.symbol == "AAPL"
        assert result.transcript_available == False
        assert result.guidance_confidence == "low"
        assert result.consensus_validation_signal == "neutral"
        assert error_msg in result.key_guidance_summary
        assert error_msg in result.analysis_notes
    
    @pytest.mark.asyncio
    async def test_management_guidance_agent_no_transcript(self):
        """Test agent when no transcript is available."""
        guidance_data = ManagementGuidanceData(
            symbol="AAPL",
            earnings_estimates={"quarterlyEstimates": []},
            earnings_transcript=None,
            quarter=None
        )
        
        result = await management_guidance_agent("AAPL", guidance_data)
        
        assert isinstance(result, ManagementGuidanceAnalysis)
        assert result.symbol == "AAPL"
        assert result.transcript_available == False
        assert result.consensus_validation_signal == "neutral"
    
    @pytest.mark.asyncio
    @patch('src.research.management_guidance.management_guidance_agent.call_llm_model')
    async def test_management_guidance_agent_with_transcript(self, mock_llm):
        """Test agent with valid transcript data."""
        # Mock AI response
        mock_llm.return_value = '''
        {
            "symbol": "AAPL",
            "quarter_analyzed": "2024Q1",
            "transcript_available": true,
            "guidance_indicators": [
                {
                    "type": "revenue",
                    "direction": "positive",
                    "confidence": "high",
                    "context": "Management expects strong iPhone sales next quarter",
                    "impact_assessment": "Positive impact on Q2 revenue growth"
                }
            ],
            "overall_guidance_tone": "optimistic",
            "risk_factors_mentioned": ["Supply chain constraints"],
            "opportunities_mentioned": ["New product launches", "Market expansion"],
            "revenue_guidance_direction": "positive",
            "margin_guidance_direction": "neutral",
            "eps_guidance_direction": "positive",
            "guidance_confidence": "high",
            "consensus_validation_signal": "bullish",
            "key_guidance_summary": "Management provided bullish guidance for next quarter with strong revenue outlook",
            "analysis_notes": "Overall positive tone with specific revenue growth drivers mentioned"
        }
        '''
        
        guidance_data = ManagementGuidanceData(
            symbol="AAPL",
            earnings_estimates={
                "quarterlyEstimates": [
                    {"fiscalDateEnding": "2024-06-30", "estimatedEPS": 2.50}
                ]
            },
            earnings_transcript={"transcript": "This is a sample earnings call transcript with management guidance..."},
            quarter="2024Q1"
        )
        
        result = await management_guidance_agent("AAPL", guidance_data)
        
        assert isinstance(result, ManagementGuidanceAnalysis)
        assert result.symbol == "AAPL"
        assert result.transcript_available == True
        assert result.quarter_analyzed == "2024Q1"
        assert result.overall_guidance_tone == "optimistic"
        assert result.consensus_validation_signal == "bullish"
        assert result.guidance_confidence == "high"
        assert len(result.guidance_indicators) == 1
        assert result.guidance_indicators[0].type == "revenue"
        assert result.guidance_indicators[0].direction == "positive"
        assert "Supply chain constraints" in result.risk_factors_mentioned
        assert "New product launches" in result.opportunities_mentioned
    
    @pytest.mark.asyncio
    @patch('src.research.management_guidance.management_guidance_agent.call_llm_model')
    async def test_management_guidance_agent_json_parse_error(self, mock_llm):
        """Test agent when AI returns invalid JSON."""
        mock_llm.return_value = "This is not valid JSON response from the AI model"
        
        guidance_data = ManagementGuidanceData(
            symbol="AAPL",
            earnings_estimates={"quarterlyEstimates": []},
            earnings_transcript={"transcript": "Sample transcript"},
            quarter="2024Q1"
        )
        
        result = await management_guidance_agent("AAPL", guidance_data)
        
        assert isinstance(result, ManagementGuidanceAnalysis)
        assert result.symbol == "AAPL"
        assert result.transcript_available == True
        assert result.guidance_confidence == "low"
        assert "Analysis completed but could not parse" in result.key_guidance_summary
    
    @pytest.mark.asyncio
    @patch('src.research.management_guidance.management_guidance_agent.call_llm_model')
    async def test_management_guidance_agent_llm_error(self, mock_llm):
        """Test agent when LLM call fails."""
        mock_llm.side_effect = Exception("LLM API error")
        
        guidance_data = ManagementGuidanceData(
            symbol="AAPL",
            earnings_estimates={"quarterlyEstimates": []},
            earnings_transcript={"transcript": "Sample transcript"},
            quarter="2024Q1"
        )
        
        result = await management_guidance_agent("AAPL", guidance_data)
        
        assert isinstance(result, ManagementGuidanceAnalysis)
        assert result.symbol == "AAPL"
        assert result.transcript_available == False
        assert "LLM API error" in result.key_guidance_summary