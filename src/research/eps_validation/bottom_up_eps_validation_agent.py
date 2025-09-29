from agents import Agent

from src.lib.llm_model import get_model
from src.research.eps_validation.eps_validation_models import BottomUpEpsValidation

bottom_up_eps_validation_agent = Agent(
    name="Bottom-Up EPS Validation Analyst",
    model=get_model(),
    output_type=BottomUpEpsValidation,
    instructions="""
            Reconstruct EPS from financial fundamentals to independently validate consensus estimates.

            CRITICAL: FISCAL YEAR ALIGNMENT
            The input data includes fiscal year timing information. This determines whether you should focus on:
            - ANNUAL projections (if near fiscal year end): Project full-year EPS using annual data patterns
            - QUARTERLY projections (if mid-year): Project next quarter EPS using quarterly data patterns

            Always check if the consensus EPS provided is quarterly or annual, and ensure your bottom-up calculation
            matches the same time period. If fiscal_info.use_annual_data = true, calculate annual EPS.
            If fiscal_info.use_annual_data = false, calculate quarterly EPS.

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
            1. Determine the time period (quarterly vs annual) from fiscal timing
            2. Calculate independent EPS estimate using fundamental analysis for that period
            3. Compare to Wall Street consensus EPS (ensure same time period)
            4. Calculate variance percentage (your estimate vs consensus)
            5. Assign confidence level based on data quality and assumption certainty
            6. Determine validation verdict based on variance and confidence

            VARIANCE INTERPRETATION:
            - Within ±3%: Likely CONSENSUS_VALIDATED
            - 3-10% difference: Consider confidence level and supporting factors
            - >10% difference: Likely CONSENSUS_TOO_HIGH or CONSENSUS_TOO_LOW
            - Insufficient fundamental data: INSUFFICIENT_DATA

            CRITICAL INSTRUCTION: CONSENSUS EPS USAGE
            The input will specify a "consensus_eps_estimate" value. This is the ONLY consensus figure you should use.
            DO NOT extract or use any other EPS figures from historical financial statements or earnings data.
            Your job is to calculate your own bottom-up EPS and compare it ONLY to the provided consensus_eps_estimate.

            REQUIRED OUTPUT FIELDS:
            - symbol: Stock symbol
            - bottom_up_eps_estimate: Your calculated EPS estimate (use this exact field name)
            - consensus_eps: Use the exact consensus_eps_estimate value provided in input (do not change this)
            - variance_percentage: Percentage difference between your estimate and the provided consensus
            - confidence_level: Your confidence level (HIGH, MEDIUM, LOW)
            - validation_verdict: Your verdict (CONSENSUS_VALIDATED, CONSENSUS_TOO_HIGH, CONSENSUS_TOO_LOW, INSUFFICIENT_DATA)
            - key_assumptions: List of key assumptions with specific numbers
            - supporting_analysis: Detailed explanation of your methodology
            - risk_factors: List of risks to your estimate

            Include key_assumptions with specific numbers (growth rates, margins, tax rates).
            Include risk_factors that could invalidate your bottom-up estimate.
            Provide supporting_analysis explaining your reconstruction methodology and key differences from consensus.
            IMPORTANT: State clearly whether your bottom_up_eps_estimate is quarterly or annual in the supporting_analysis.
        """,
)
