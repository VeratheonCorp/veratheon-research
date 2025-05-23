from src.company_research.models.financials import Financials
from src.company_research.models.macroeconomics import Macroeconomics


class Diligence:
  def __init__(self, symbol: str, price_target: int, timeframe: str):
    self.symbol = symbol
    self.price_target = price_target
    self.timeframe = timeframe
    self.is_thesis_upside = False
    self.company_financials = Financials(symbol)
    self.macroeconomics = Macroeconomics()
    self.check_if_thesis_is_upside()

  def check_if_thesis_is_upside(self) -> bool:
    """Check if the current price is below the price target."""
    current_price = float(self.company_financials.global_quote["05. price"])
    self.is_thesis_upside = current_price < self.price_target