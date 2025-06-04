import asyncio
import json
from agents import Runner

from src.company_research import price_target_intake
from src.company_research.models.diligence import Diligence


class Researcher:

    async def run(self, symbol: str, price_target: int, timeframe: str) -> None:
        company_diligence = Diligence(symbol=symbol, price_target=price_target, timeframe=timeframe)
        print(f"Running research for {company_diligence.symbol} with price target {company_diligence.price_target} in {company_diligence.timeframe}")

        # serialize to dict & wrap in list so Runner.run can extend it
        llm_summary = company_diligence.llm_summary()
        
        # Ensure the input is properly formatted as a string
        if isinstance(llm_summary, dict):
            input_data = json.dumps(llm_summary)
        else:
            input_data = str(llm_summary)
            
        result = await Runner.run(
            price_target_intake.agent,
            input=input_data,  # Pass as string instead of list
        )

        print("Price Target Intake Output:")
        print(f"Summary: {json.dumps(result.final_output.summary, indent=2)}")
        print(f"Reasoning: {json.dumps(result.final_output.reasoning, indent=2)}")

