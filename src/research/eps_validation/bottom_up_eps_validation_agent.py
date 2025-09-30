from agents import Agent

from src.lib.llm_model import get_model
from src.research.eps_validation.eps_validation_models import BottomUpEpsValidation

bottom_up_eps_validation_agent = Agent(
    name="Bottom-Up EPS Validation Analyst",
    model=get_model(),
    output_type=BottomUpEpsValidation,
    instructions="""
            Reconstruct EPS from fundamentals to validate consensus estimates.

            FISCAL YEAR ALIGNMENT:
            - Use fiscal_info.use_annual_data to determine if calculating annual or quarterly EPS
            - Match your calculation period to the consensus_eps_estimate provided

            ENUMS:
            - confidence_level: HIGH/MEDIUM/LOW
            - validation_verdict: CONSENSUS_VALIDATED/CONSENSUS_TOO_HIGH/CONSENSUS_TOO_LOW/INSUFFICIENT_DATA

            METHODOLOGY:
            1. Build bottom-up EPS from: revenue projections, gross margins, operating expenses, tax rate, share count
            2. Compare to provided consensus_eps_estimate (DO NOT use other EPS figures from historical data)
            3. Calculate variance percentage

            VARIANCE THRESHOLDS:
            - Within ±3%: CONSENSUS_VALIDATED
            - 3-10%: Consider data quality
            - >10%: CONSENSUS_TOO_HIGH or CONSENSUS_TOO_LOW
            - Poor data: INSUFFICIENT_DATA

            Include key_assumptions (specific numbers), risk_factors, and supporting_analysis.
            State clearly if your estimate is quarterly or annual.
        """,
)
