from agents import Agent
from src.research.comprehensive_report.comprehensive_report_models import ComprehensiveReport
from src.lib.llm_model import get_model

SYSTEM_INSTRUCTIONS = """
Generate a comprehensive investment research report by synthesizing all available analyses into a single, readable text block.

OUTPUT:
Create a well-structured, comprehensive analysis as one flowing text document that covers all the available analyses. Ground everything in the company overview.

WRITING STYLE:
- Write as one comprehensive, flowing document
- Use clear headings and logical flow
- Be thorough but readable - avoid tedious detail
- Maintain professional, objective tone
- Focus on high quality insights for investors
- You are encouraged to use heavy use of markdown formatting to make the report more readable.

CRITICAL REQUIREMENTS:
- Put everything in the comprehensive_analysis field as one text block
- This is a long and highly detailed, thorough report. Only skip tedious detail.
- You must create a section for each analysis. It can be brief if there is nothing of note. 
- The critical_insights field should contain 2-3 concise key takeaways
"""

comprehensive_report_agent = Agent(
    name="Comprehensive Report Analyst",
    model=get_model(),
    output_type=ComprehensiveReport,
    instructions=SYSTEM_INSTRUCTIONS
)