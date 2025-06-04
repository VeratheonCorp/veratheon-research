from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List
from src.clients.alpha_vantage_client import AlphaVantageClient

class Financials(BaseModel):
    symbol: str
    overview: Dict[str, Any] = Field(default_factory=dict)
    income_statement: Dict[str, Any] = Field(default_factory=dict)
    balance_sheet: Dict[str, Any] = Field(default_factory=dict)
    cash_flow: Dict[str, Any] = Field(default_factory=dict)
    global_quote: Dict[str, Any] = Field(default_factory=dict)

    time_series_daily: Dict[str, Any] = Field(default_factory=dict)
    rsi_daily: Optional[float] = None
    macd_daily: Optional[float] = None
    bollinger_bands_daily: Optional[Dict[str, Any]] = None

    free_cash_flow: Optional[List[float]] = None
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

    def model_post_init(self, __context):
        """Initialize financial data after Pydantic initialization."""
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
        self.time_series_daily = client.run_query(f"TIME_SERIES_DAILY&symbol={self.symbol}&outputsize=full")['Time Series (Daily)']
        self.rsi_daily = client.run_query(f"RSI&symbol={self.symbol}&interval=daily&time_period=50&series_type=close")['Technical Analysis: RSI']
        self.macd_daily = client.run_query(f"MACD&symbol={self.symbol}&interval=daily&time_period=50&series_type=close")['Technical Analysis: MACD']
        self.bollinger_bands_daily = client.run_query(f"BBANDS&symbol={self.symbol}&interval=daily&time_period=50&series_type=close")['Technical Analysis: BBANDS']

    def calculate_derived_metrics(self) -> None:
        balance_sheets = self.balance_sheet.get("annualReports", [])
        income_statements = self.income_statement.get("annualReports", [])
        cash_flows = self.cash_flow.get("annualReports", [])
        if not (balance_sheets and income_statements and cash_flows):
            return
        
        self.free_cash_flow = self._calculate_free_cash_flow()
        self.fcf_margin = self._calculate_fcf_margin()
        self.roic = self._calculate_roic()
        self.fixed_asset_turnover = self._calculate_fixed_asset_turnover()
        self.debt_to_equity = self._calculate_debt_to_equity()
        self.debt_to_fcf = self._calculate_debt_to_fcf()
        self.interest_coverage = self._calculate_interest_coverage()
        self.liquidity = self._calculate_liquidity()
        self.quick_ratio = self._calculate_quick_ratio()
        self.organic_revenue_growth = self._calculate_organic_revenue_growth()
        self.revenue_growth_yoy = self._calculate_revenue_growth_yoy()
        self.cash_conversion_cycle = self._calculate_cash_conversion_cycle()
        self.sga_pct = self._calculate_sga_pct()
        self.rd_pct = self._calculate_rd_pct()
        self.capex_pct = self._calculate_capex_pct()

    def _calculate_free_cash_flow(self) -> Optional[List[float]]:
        cash_flows = self.cash_flow.get("annualReports", [])
        if not cash_flows:
            return None
        
        get = lambda d,k: float(d.get(k, 0) or 0)
        fcf_list = []
        
        # Calculate FCF for up to 10 years (or however many reports are available)
        for cf_report in cash_flows[:10]:
            op_cf = get(cf_report, "operatingCashflow")
            capex = get(cf_report, "capitalExpenditures")
            fcf = op_cf + capex
            fcf_list.append(fcf)
        
        return fcf_list if fcf_list else None

    def _calculate_fcf_margin(self) -> Optional[float]:
        income_statements = self.income_statement.get("annualReports", [])
        if not income_statements or not self.free_cash_flow:
            return None
        is_cur = income_statements[0]
        get = lambda d,k: float(d.get(k, 0) or 0)
        revenue = get(is_cur, "totalRevenue")
        # Use the most recent FCF value (first in the list)
        recent_fcf = self.free_cash_flow[0]
        return recent_fcf / revenue if revenue and recent_fcf else None

    def _calculate_roic(self) -> Optional[float]:
        balance_sheets = self.balance_sheet.get("annualReports", [])
        income_statements = self.income_statement.get("annualReports", [])
        if not (balance_sheets and income_statements):
            return None
        bs_cur = balance_sheets[0]
        is_cur = income_statements[0]
        get = lambda d,k: float(d.get(k, 0) or 0)
        net_income = get(is_cur, "netIncome")
        total_assets = get(bs_cur, "totalAssets")
        curr_liab = get(bs_cur, "totalCurrentLiabilities")
        return net_income / (total_assets - curr_liab) if (total_assets - curr_liab) else None

    def _calculate_fixed_asset_turnover(self) -> Optional[float]:
        balance_sheets = self.balance_sheet.get("annualReports", [])
        income_statements = self.income_statement.get("annualReports", [])
        if not (balance_sheets and income_statements):
            return None
        bs_cur = balance_sheets[0]
        is_cur = income_statements[0]
        get = lambda d,k: float(d.get(k, 0) or 0)
        revenue = get(is_cur, "totalRevenue")
        ppe = get(bs_cur, "propertyPlantEquipmentNet")
        return revenue / ppe if ppe else None

    def _calculate_debt_to_equity(self) -> Optional[float]:
        balance_sheets = self.balance_sheet.get("annualReports", [])
        if not balance_sheets:
            return None
        bs_cur = balance_sheets[0]
        get = lambda d,k: float(d.get(k, 0) or 0)
        liabilities = get(bs_cur, "totalLiabilities")
        equity = get(bs_cur, "totalShareholderEquity")
        return liabilities / equity if equity else None

    def _calculate_debt_to_fcf(self) -> Optional[float]:
        balance_sheets = self.balance_sheet.get("annualReports", [])
        if not balance_sheets or not self.free_cash_flow:
            return None
        bs_cur = balance_sheets[0]
        get = lambda d,k: float(d.get(k, 0) or 0)
        liabilities = get(bs_cur, "totalLiabilities")
        # Use the most recent FCF value (first in the list)
        recent_fcf = self.free_cash_flow[0]
        return liabilities / recent_fcf if recent_fcf else None

    def _calculate_interest_coverage(self) -> Optional[float]:
        income_statements = self.income_statement.get("annualReports", [])
        if not income_statements:
            return None
        is_cur = income_statements[0]
        get = lambda d,k: float(d.get(k, 0) or 0)
        ebit = get(is_cur, "ebit") or get(is_cur, "operatingIncome")
        interest = abs(get(is_cur, "interestExpense"))
        return ebit / interest if interest else None

    def _calculate_liquidity(self) -> Optional[float]:
        balance_sheets = self.balance_sheet.get("annualReports", [])
        if not balance_sheets:
            return None
        bs_cur = balance_sheets[0]
        get = lambda d,k: float(d.get(k, 0) or 0)
        curr_assets = get(bs_cur, "totalCurrentAssets")
        curr_liab = get(bs_cur, "totalCurrentLiabilities")
        return curr_assets / curr_liab if curr_liab else None

    def _calculate_quick_ratio(self) -> Optional[float]:
        balance_sheets = self.balance_sheet.get("annualReports", [])
        if not balance_sheets:
            return None
        bs_cur = balance_sheets[0]
        get = lambda d,k: float(d.get(k, 0) or 0)
        curr_assets = get(bs_cur, "totalCurrentAssets")
        inventory = get(bs_cur, "inventory")
        curr_liab = get(bs_cur, "totalCurrentLiabilities")
        return (curr_assets - inventory) / curr_liab if curr_liab else None

    def _calculate_organic_revenue_growth(self) -> Optional[float]:
        return self._calculate_revenue_growth_yoy()

    def _calculate_revenue_growth_yoy(self) -> Optional[float]:
        income_statements = self.income_statement.get("annualReports", [])
        if len(income_statements) < 2:
            return None
        is_cur = income_statements[0]
        is_prev = income_statements[1]
        get = lambda d,k: float(d.get(k, 0) or 0)
        revenue = get(is_cur, "totalRevenue")
        prev_revenue = get(is_prev, "totalRevenue")
        return (revenue - prev_revenue) / prev_revenue if prev_revenue else None

    def _calculate_cash_conversion_cycle(self) -> Optional[float]:
        balance_sheets = self.balance_sheet.get("annualReports", [])
        income_statements = self.income_statement.get("annualReports", [])
        if not (balance_sheets and income_statements):
            return None
        bs_cur = balance_sheets[0]
        is_cur = income_statements[0]
        get = lambda d,k: float(d.get(k, 0) or 0)
        revenue = get(is_cur, "totalRevenue")
        cogs = get(is_cur, "costOfGoodsSold")
        inventory = get(bs_cur, "inventory")
        receivables = get(bs_cur, "netReceivables")
        payables = get(bs_cur, "accountsPayable")
        
        if not cogs or not revenue:
            return None
        
        dio = inventory / (cogs / 365)
        dso = receivables / (revenue / 365)
        dpo = payables / (cogs / 365)
        return dio + dso - dpo

    def _calculate_sga_pct(self) -> Optional[float]:
        income_statements = self.income_statement.get("annualReports", [])
        if not income_statements:
            return None
        is_cur = income_statements[0]
        get = lambda d,k: float(d.get(k, 0) or 0)
        sga = get(is_cur, "sellingGeneralAndAdministrativeExpenses")
        revenue = get(is_cur, "totalRevenue")
        return sga / revenue if revenue else None

    def _calculate_rd_pct(self) -> Optional[float]:
        income_statements = self.income_statement.get("annualReports", [])
        if not income_statements:
            return None
        is_cur = income_statements[0]
        get = lambda d,k: float(d.get(k, 0) or 0)
        rd = get(is_cur, "researchAndDevelopmentExpenses")
        revenue = get(is_cur, "totalRevenue")
        return rd / revenue if revenue else None

    def _calculate_capex_pct(self) -> Optional[float]:
        cash_flows = self.cash_flow.get("annualReports", [])
        income_statements = self.income_statement.get("annualReports", [])
        if not (cash_flows and income_statements):
            return None
        cf_cur = cash_flows[0]
        is_cur = income_statements[0]
        get = lambda d,k: float(d.get(k, 0) or 0)
        capex = get(cf_cur, "capitalExpenditures")
        revenue = get(is_cur, "totalRevenue")
        return abs(capex) / revenue if revenue else None



