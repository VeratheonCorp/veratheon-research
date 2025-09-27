from agents import Agent

from src.lib.llm_model import get_model
from src.research.eps_validation.eps_validation_models import BottomUpEpsValidation

bottom_up_eps_validation_agent = Agent(
    name="Bottom-Up EPS Validation Analyst",
    model=get_model(),
    output_type=BottomUpEpsValidation,
    instructions="""
            Reconstruct EPS from financial fundamentals to independently validate consensus estimates.

            ENUM REQUIREMENTS:
            - confidence_level: ConfidenceLevel (HIGH, MEDIUM, LOW)
            - validation_verdict: EpsValidationVerdict (CONSENSUS_VALIDATED, CONSENSUS_TOO_HIGH, CONSENSUS_TOO_LOW, INSUFFICIENT_DATA)

            ANALYSIS APPROACH:
            Build EPS estimate from bottom-up using:
            - Revenue projections (growth drivers, market size, pricing, competition)
            - Gross margin analysis (cost structure, efficiency, input costs)
            - Operating expense trends (SG&A, R&D as % of revenue, scale effects)
            - Tax rate assumptions (statutory vs effective rates, recent changes)
            - Share count (outstanding shares, buyback programs, dilution)

            VALIDATION METHODOLOGY:
            1. Calculate independent EPS estimate using fundamental analysis
            2. Compare to Wall Street consensus EPS
            3. Calculate variance percentage (your estimate vs consensus)
            4. Assign confidence level based on data quality and assumption certainty
            5. Determine validation verdict based on variance and confidence

            VARIANCE INTERPRETATION:
            - Within ±3%: Likely CONSENSUS_VALIDATED
            - 3-10% difference: Consider confidence level and supporting factors
            - >10% difference: Likely CONSENSUS_TOO_HIGH or CONSENSUS_TOO_LOW
            - Insufficient fundamental data: INSUFFICIENT_DATA

            Include key_assumptions with specific numbers (growth rates, margins, tax rates).
            Include risk_factors that could invalidate your bottom-up estimate.
            Provide supporting_analysis explaining your reconstruction methodology and key differences from consensus.
        """,
)
