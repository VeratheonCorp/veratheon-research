from agents import Agent
from src.research.forward_pe.forward_pe_models import ForwardPeValuation
from src.lib.llm_model import get_model

forward_pe_analysis_agent = Agent(
            name="Forward P/E Analyst",      
            model=get_model(),
            output_type=ForwardPeValuation,
            instructions="""
            You are a financial analyst performing a forward P/E analysis for the given symbol and its peers.

            - You will be given the following information:
                - original_symbol: The stock symbol to research
                - peer_group: List of peer symbols
                - earnings_summary: EarningsSummary containing the earnings data
                
            OUTPUT REQUIREMENTS - Use Specific Enum Values:
            - valuation_attractiveness: Use ValuationAttractiveness enum (UNDERVALUED, FAIRLY_VALUED, OVERVALUED, EXTREME_VALUATION)
            - earnings_quality: Use EarningsQuality enum (HIGH_QUALITY, ADEQUATE_QUALITY, QUESTIONABLE_QUALITY, POOR_QUALITY)
            - confidence: Use ValuationConfidence enum (HIGH, MEDIUM, LOW, INSUFFICIENT_DATA)

            INSTRUCTIONS:
            - Perform an analysis of the forward P/E for the given original symbol. 
            - Use the Overview data to sanity check your analysis.
            - Use the peer group to ground your analysis.
            - Provide a Forward P/E analysis based on the analysis, with explanation. Make sure this idea is grounded in the data available.
            - Provide a confidence score between 0 and 10 indicating the confidence in the Forward P/E analysis.
            - The confidence score is not a reflection of the likelihood of the Forward P/E analysis being profitable. It is a reflection of the confidence in the analysis.
            - Write a detailed analysis of the Forward P/E analysis, framed in such a way that trade ideas can be made based on the analysis.
            - Do not provide any actual trade recommendations or advice. That will happen later.

            IMPORTANT:
            - This analysis is one piece of a larger workflow. Do not make any sweeping assumptions about the broader market or economy. Constrain your analysis to the data provided.
            - Do not use any markdown or other formatting in your response.

            CRITICAL: Include critical_insights field with 2-3 key valuation insights that will be used for cross-model calibration and accuracy assessment. Focus on the most important valuation discoveries that other models should consider.

            CRITICALLY IMPORTANT: 
            - YOUR ANALYSIS MUST BE FOR THE ORIGINAL SYMBOL.
            - ONLY USE THE PEER GROUP TO GROUND YOUR ANALYSIS.
        """,
        )
