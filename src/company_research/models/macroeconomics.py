from typing import Dict, Any
from pydantic import BaseModel
from src.clients.alpha_vantage_client import AlphaVantageClient

class Macroeconomics(BaseModel):
    real_gdp:               Dict[str, Any] = {}
    real_gdp_per_capita:    Dict[str, Any] = {}
    treasury_yield:         Dict[str, Any] = {}
    federal_funds_rate:     Dict[str, Any] = {}
    consumer_price_index:   Dict[str, Any] = {}
    inflation_rate:         Dict[str, Any] = {}
    retail_sales:           Dict[str, Any] = {}
    durable_goods_orders:   Dict[str, Any] = {}
    unemployment_rate:      Dict[str, Any] = {}
    nonfarm_payrolls:       Dict[str, Any] = {}

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.fetch_all()

    def fetch_all(self) -> None:
        client = AlphaVantageClient()
        self.real_gdp             = client.run_query("REAL_GDP")
        self.real_gdp_per_capita  = client.run_query("REAL_GDP_PER_CAPITA")
        self.treasury_yield       = client.run_query("TREASURY_YIELD")
        self.federal_funds_rate   = client.run_query("FEDERAL_FUNDS_RATE")
        self.consumer_price_index = client.run_query("CPI")
        self.inflation_rate       = client.run_query("INFLATION")
        self.retail_sales         = client.run_query("RETAIL_SALES")
        self.durable_goods_orders = client.run_query("DURABLES")
        self.unemployment_rate    = client.run_query("UNEMPLOYMENT")
        self.nonfarm_payrolls     = client.run_query("NONFARM_PAYROLL")
