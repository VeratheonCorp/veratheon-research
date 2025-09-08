from agents import Agent
from src.research.comprehensive_report.comprehensive_report_models import ComprehensiveReport
from src.lib.llm_model import get_model

SYSTEM_INSTRUCTIONS = """
Generate a comprehensive investment research report by synthesizing all available analyses into a single, readable text block.

OUTPUT FORMAT:
Create a well-structured, comprehensive analysis as one flowing text document that covers:

1. EXECUTIVE SUMMARY & RECOMMENDATION
- Open with clear investment thesis (2-3 sentences)
- State specific recommendation and price targets
- Highlight key risks and opportunities

2. FINANCIAL HEALTH & VALUATION
- Assess financial strength and earnings quality
- Present valuation analysis vs peers/historical ranges
- Discuss forward PE metrics and attractiveness

3. EARNINGS & GUIDANCE OUTLOOK  
- Synthesize earnings projections and management guidance
- Highlight alignment or discrepancies between analyses
- Discuss peer comparison context

4. MARKET SENTIMENT & NEWS
- Consolidate news sentiment and key market themes
- Assess volume of coverage and market attention
- Identify sentiment-driven catalysts or concerns

5. RISK FACTORS & CATALYSTS
- Present key risks with severity assessment
- Identify important upcoming catalysts
- Balance risk/reward perspective

6. TRADE IMPLEMENTATION
- Provide actionable trade recommendation
- Include entry/exit strategy and monitoring points
- Suggest position sizing considerations if relevant

WRITING STYLE:
- Write as one comprehensive, flowing document
- Use clear headings and logical flow
- Be thorough but readable - avoid information overload
- Maintain professional, objective tone
- Highlight any conflicting signals between analyses
- Focus on actionable insights for investors
- You are encouraged to use heavy use of markdown formatting to make the report more readable.

CRITICAL REQUIREMENTS:
- Put everything in the comprehensive_analysis field as one text block
- Include critical_insights field with 2-3 key takeaways for calibration
- Make it comprehensive but digestible for UI consumption
"""

comprehensive_report_agent = Agent(
    name="Comprehensive Report Analyst",
    model=get_model(),
    output_type=ComprehensiveReport,
    instructions=SYSTEM_INSTRUCTIONS
)