from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from src.clients.alpha_vantage_client import AlphaVantageClient

class Financials(BaseModel):
    symbol: str
    overview: Dict[str, Any] = Field(default_factory=dict)
    income_statement: Dict[str, Any] = Field(default_factory=dict)
    balance_sheet: Dict[str, Any] = Field(default_factory=dict)
    cash_flow: Dict[str, Any] = Field(default_factory=dict)
    global_quote: Dict[str, Any] = Field(default_factory=dict)

    free_cash_flow: Optional[float] = None
    fcf_margin:   Optional[float] = None
    roic:         Optional[float] = None
    fixed_asset_turnover: Optional[float] = None
    debt_to_equity:       Optional[float] = None
    debt_to_fcf:          Optional[float] = None
    interest_coverage:    Optional[float] = None
    liquidity:            Optional[float] = None
    quick_ratio:          Optional[float] = None
    organic_revenue_growth: Optional[float] = None
    revenue_growth_yoy:     Optional[float] = None
    cash_conversion_cycle:  Optional[float] = None
    sga_pct:                Optional[float] = None
    rd_pct:                 Optional[float] = None
    capex_pct:              Optional[float] = None

    def __init__(self, symbol: str, **data: Any):
        super().__init__(symbol=symbol, **data)
        self.fetch_all()
        self.calculate_derived_metrics()

    def fetch_all(self) -> None:
        """Retrieve and store all financial statements from AlphaVantage."""
        client = AlphaVantageClient()
        self.overview = client.run_query(f"OVERVIEW&symbol={self.symbol}")
        self.income_statement = client.run_query(f"INCOME_STATEMENT&symbol={self.symbol}")
        self.balance_sheet = client.run_query(f"BALANCE_SHEET&symbol={self.symbol}")
        self.cash_flow = client.run_query(f"CASH_FLOW&symbol={self.symbol}")
        self.global_quote = client.run_query(f"GLOBAL_QUOTE&symbol={self.symbol}")['Global Quote']
        
    
    def calculate_derived_metrics(self) -> None:
        bs_reports = self.balance_sheet.get("annualReports", [])
        is_reports = self.income_statement.get("annualReports", [])
        cf_reports = self.cash_flow.get("annualReports", [])
        if not (bs_reports and is_reports and cf_reports):
            return
        bs_cur = bs_reports[0]; bs_prev = bs_reports[1] if len(bs_reports) > 1 else {}
        is_cur = is_reports[0]; is_prev = is_reports[1] if len(is_reports) > 1 else {}
        cf_cur = cf_reports[0]
        # helper to safely parse floats
        get = lambda d,k: float(d.get(k, 0) or 0)
        # key inputs
        revenue = get(is_cur, "totalRevenue"); prev_revenue = get(is_prev, "totalRevenue")
        op_cf = get(cf_cur, "operatingCashflow"); capex = get(cf_cur, "capitalExpenditures")
        net_income = get(is_cur, "netIncome")
        total_assets = get(bs_cur, "totalAssets"); curr_liab = get(bs_cur, "totalCurrentLiabilities")
        equity = get(bs_cur, "totalShareholderEquity"); liabilities = get(bs_cur, "totalLiabilities")
        # compute metrics
        fcf = op_cf + capex
        roic = net_income / (total_assets - curr_liab) if (total_assets - curr_liab) else None
        fixed_asset_turnover = revenue / get(bs_cur, "propertyPlantEquipmentNet") if bs_cur.get("propertyPlantEquipmentNet") else None
        debt_to_equity = liabilities / equity if equity else None
        debt_to_fcf = liabilities / fcf if fcf else None
        ebit = get(is_cur, "ebit") or get(is_cur, "operatingIncome"); interest = abs(get(is_cur, "interestExpense"))
        interest_coverage = ebit / interest if interest else None
        liquidity = get(bs_cur, "totalCurrentAssets") / curr_liab if curr_liab else None
        quick_ratio = (get(bs_cur, "totalCurrentAssets") - get(bs_cur, "inventory")) / curr_liab if curr_liab else None
        rev_growth = (revenue - prev_revenue) / prev_revenue if prev_revenue else None
        cogs = get(is_cur, "costOfGoodsSold")
        dio = get(bs_cur, "inventory") / (cogs / 365) if cogs else None
        dso = get(bs_cur, "netReceivables") / (revenue / 365) if revenue else None
        dpo = get(bs_cur, "accountsPayable") / (cogs / 365) if cogs else None
        ccc = (dio + dso - dpo) if None not in (dio, dso, dpo) else None
        sga_pct = get(is_cur, "sellingGeneralAndAdministrativeExpenses") / revenue if revenue else None
        rd_pct = get(is_cur, "researchAndDevelopmentExpenses") / revenue if revenue else None
        capex_pct = abs(capex) / revenue if revenue else None
        # assign metrics to instance attributes for Intellisense
        self.free_cash_flow = fcf
        self.fcf_margin = fcf / revenue if revenue else None
        self.roic = roic
        self.fixed_asset_turnover = fixed_asset_turnover
        self.debt_to_equity = debt_to_equity
        self.debt_to_fcf = debt_to_fcf
        self.interest_coverage = interest_coverage
        self.liquidity = liquidity
        self.quick_ratio = quick_ratio
        self.organic_revenue_growth = rev_growth
        self.revenue_growth_yoy = rev_growth
        self.cash_conversion_cycle = ccc
        self.sga_pct = sga_pct
        self.rd_pct = rd_pct
        self.capex_pct = capex_pct



