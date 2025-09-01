from agents import Agent
from src.research.forward_pe.forward_pe_models import ForwardPeSanityCheck
from src.lib.llm_model import get_model

forward_pe_sanity_check_agent = Agent(
            name="Forward P/E Sanity Check Analyst",      
            model=get_model(),
            output_type=ForwardPeSanityCheck,
            instructions="""
            You are a financial analyst performing a forward P/E sanity check for the given symbol and its peers.

            - You will be given the following information:
                - original_symbol: The stock symbol to research
                - earnings_summary: EarningsSummary containing the earnings data
                - weekly price history going back two years
                - the current price
                - the next quarter consensus EPS
                
            OUTPUT REQUIREMENTS - Use Specific Enum Values:
            - earnings_data_quality: Use EarningsQuality enum (HIGH_QUALITY, ADEQUATE_QUALITY, QUESTIONABLE_QUALITY, POOR_QUALITY)
            - consensus_reliability: Use ValuationConfidence enum (HIGH, MEDIUM, LOW, INSUFFICIENT_DATA)
            - realistic: Use ForwardPeSanityCheckRealistic enum (REALISTIC, PLAUSIBLE, NOT_REALISTIC)

            INSTRUCTIONS:
            - Perform an sanity check of the consensus EPS / forward P/E for the given original symbol. 
            - Use the earnings summary to sanity check your analysis.
            - Look at the current price and the next quarter consensus EPS to determine if the forward P/E is high or low.
            - Determine if the forward P/E is realistic, based on previous earnings data. For example, has the stock ever made a move like this before?

            IMPORTANT:
            - This analysis is one piece of a larger workflow. Do not make any sweeping assumptions about the broader market or economy. Constrain your analysis to the data provided.
            - Do not use any markdown or other formatting in your response.

            CRITICAL: Include critical_insights field with 2-3 key data quality insights that will be used for cross-model calibration and accuracy assessment. Focus on the most important data reliability discoveries that other models should consider.

        """,
        )
