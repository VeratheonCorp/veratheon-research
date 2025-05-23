import asyncio
import json
from agents import Runner

from src.company_research.models.diligence import Diligence
from src.company_research.models.financials import Financials
from src.company_research.models.macroeconomics import Macroeconomics

class Researcher:

    async def run(self, symbol: str, price_target: int, timeframe: str) -> None:
        company_diligence = Diligence(symbol, price_target, timeframe)
        print(f"Running research for {company_diligence.symbol} with price target {company_diligence.price_target} in {company_diligence.timeframe}")
        print(f"Free Cash Flow: {company_diligence.company_financials.free_cash_flow}")
        print(f"Closing Price: {company_diligence.company_financials.global_quote['05. price']}")
        print(f"Is Thesis Upside: {company_diligence.is_thesis_upside}")
        