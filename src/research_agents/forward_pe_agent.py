from typing import Dict, Any, List
from pydantic import BaseModel
from src.tools.alpha_vantage_tool import (
    call_alpha_vantage_global_quote,
    call_alpha_vantage_earnings,
)
from agents import Agent, Runner


class EarningsSummary(BaseModel):
    symbol_earnings: Dict[str, Any]
    peer_earnings: List[Dict[str, Any]]
    summary: str


class ForwardPeAgent:
    def __init__(self):
        self.agent = self._create_agent()

    def _create_agent(self):
        return Agent(
            name="Forward PE Analyst",
            model="o4-mini",
            output_type=EarningsSummary,
            instructions="""
            You are a financial analyst specializing in forward P/E ratio analysis. 
            Your responsibilities include:
            1. Identifying peer companies for comparison
            2. Analyzing earnings data for the target company and its peers
            3. Providing insights on valuation and financial health
            
            Use the available tools to gather and analyze the necessary data.
            Always provide clear, concise, and well-structured analysis.
            """,
            tools=[
                call_alpha_vantage_global_quote,
                call_alpha_vantage_earnings,
            ],
        )

    async def analyze(self, symbol: str) -> EarningsSummary:
        """Analyze forward P/E for the given symbol and its peers"""
        try:
            prompt = f"""Perform a comprehensive forward P/E analysis for {symbol}:
            
            1. Identify 5-10 direct competitors for comparison
            2. Gather earnings data for {symbol} and its peers
            3. Calculate and compare forward P/E ratios
            
            Focus on:
            - Earnings growth trends
            - Valuation relative to peers
            - Any red flags or obvious anomalies
            
            Return a JSON object with the following structure:
            {EarningsSummary.model_json_schema()}
            """

            response = await Runner.run(self.agent, input=prompt)

            return response

        except Exception as e:
            print(f"Error in analysis: {e}")
            return EarningsSummary(
                symbol_earnings={},
                peer_earnings=[],
                summary=f"Analysis could not be completed due to an error: {str(e)}",
            )
