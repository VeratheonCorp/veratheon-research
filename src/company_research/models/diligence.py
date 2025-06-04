from pydantic import BaseModel
from src.company_research.models.financials import Financials
from src.company_research.models.macroeconomics import Macroeconomics


class Diligence(BaseModel):
    symbol: str
    price_target: int
    timeframe: str
    is_thesis_upside: bool = False
    company_financials: Financials = None
    macroeconomics: Macroeconomics = None

    def model_post_init(self, __context):
        """Initialize financials and macroeconomics after Pydantic initialization."""
        self.company_financials = Financials(symbol=self.symbol)
        self.macroeconomics = Macroeconomics()
        self.check_if_thesis_is_upside()

    def check_if_thesis_is_upside(self) -> bool:
        """Check if the current price is below the price target."""
        current_price = float(self.company_financials.global_quote["05. price"])
        self.is_thesis_upside = current_price < self.price_target

    def llm_summary(self) -> str:
        """Generate a comprehensive summary of financial and macroeconomic data for LLM analysis."""
        
        # Basic company information
        summary = f"INVESTMENT THESIS ANALYSIS FOR {self.symbol}\n"
        summary += "=" * 50 + "\n\n"
        
        # Investment thesis overview
        current_price = float(self.company_financials.global_quote.get("05. price", 0))
        summary += f"Price Target: ${self.price_target}\n"
        summary += f"Current Price: ${current_price:.2f}\n"
        summary += f"Timeframe: {self.timeframe}\n"
        summary += f"Upside Potential: {'YES' if self.is_thesis_upside else 'NO'} "
        summary += f"({((self.price_target - current_price) / current_price * 100):.1f}%)\n\n"
        
        # Company overview
        overview = self.company_financials.overview
        if overview:
            summary += "COMPANY OVERVIEW\n"
            summary += "-" * 20 + "\n"
            summary += f"Sector: {overview.get('Sector', 'N/A')}\n"
            summary += f"Industry: {overview.get('Industry', 'N/A')}\n"
            summary += f"Market Cap: ${overview.get('MarketCapitalization', 'N/A')}\n"
            summary += f"P/E Ratio: {overview.get('PERatio', 'N/A')}\n"
            summary += f"Forward P/E: {overview.get('ForwardPE', 'N/A')}\n"
            summary += f"PEG Ratio: {overview.get('PEGRatio', 'N/A')}\n"
            summary += f"Price/Book: {overview.get('PriceToBookRatio', 'N/A')}\n"
            summary += f"Price/Sales: {overview.get('PriceToSalesRatioTTM', 'N/A')}\n"
            summary += f"ROE: {overview.get('ReturnOnEquityTTM', 'N/A')}\n"
            summary += f"ROA: {overview.get('ReturnOnAssetsTTM', 'N/A')}\n"
            summary += f"Profit Margin: {overview.get('ProfitMargin', 'N/A')}\n\n"
        
        # Custom financial metrics
        fin = self.company_financials
        summary += "KEY FINANCIAL METRICS\n"
        summary += "-" * 20 + "\n"
        
        # Free Cash Flow analysis
        if fin.free_cash_flow:
            summary += f"Free Cash Flow (10-year): {[f'${fcf/1e6:.1f}M' for fcf in fin.free_cash_flow[:5]]}\n"
            summary += f"Recent FCF: ${fin.free_cash_flow[0]/1e6:.1f}M\n"
        
        # Custom calculated metrics
        metrics = [
            ("FCF Margin", fin.fcf_margin, "%"),
            ("ROIC", fin.roic, "%"),
            ("Fixed Asset Turnover", fin.fixed_asset_turnover, "x"),
            ("Debt/Equity", fin.debt_to_equity, "x"),
            ("Debt/FCF", fin.debt_to_fcf, "x"),
            ("Interest Coverage", fin.interest_coverage, "x"),
            ("Current Ratio", fin.liquidity, "x"),
            ("Quick Ratio", fin.quick_ratio, "x"),
            ("Revenue Growth YoY", fin.revenue_growth_yoy, "%"),
            ("Cash Conversion Cycle", fin.cash_conversion_cycle, "days"),
            ("SG&A %", fin.sga_pct, "%"),
            ("R&D %", fin.rd_pct, "%"),
            ("CapEx %", fin.capex_pct, "%")
        ]
        
        for name, value, unit in metrics:
            if value is not None:
                if unit == "%":
                    summary += f"{name}: {value*100:.1f}%\n"
                elif unit == "days":
                    summary += f"{name}: {value:.0f} days\n"
                else:
                    summary += f"{name}: {value:.2f}{unit}\n"
            else:
                summary += f"{name}: N/A\n"
        
        # Technical indicators
        summary += "\nTECHNICAL INDICATORS\n"
        summary += "-" * 20 + "\n"
        
        # Get latest technical data
        if hasattr(fin, 'rsi_daily') and fin.rsi_daily:
            latest_rsi_date = max(fin.rsi_daily.keys())
            latest_rsi = fin.rsi_daily[latest_rsi_date].get('RSI', 'N/A')
            summary += f"RSI (50-day): {latest_rsi}\n"
        
        if hasattr(fin, 'macd_daily') and fin.macd_daily:
            latest_macd_date = max(fin.macd_daily.keys())
            macd_data = fin.macd_daily[latest_macd_date]
            summary += f"MACD: {macd_data.get('MACD', 'N/A')}\n"
            summary += f"MACD Signal: {macd_data.get('MACD_Signal', 'N/A')}\n"
        
        # Price performance
        daily_prices = list(fin.time_series_daily.values())[:5] if fin.time_series_daily else []
        if len(daily_prices) >= 2:
            latest_price = float(daily_prices[0]['4. close'])
            week_ago_price = float(daily_prices[4]['4. close']) if len(daily_prices) >= 5 else float(daily_prices[-1]['4. close'])
            week_performance = (latest_price - week_ago_price) / week_ago_price * 100
            summary += f"5-Day Performance: {week_performance:.1f}%\n"
        
        # Macroeconomic environment
        macro = self.macroeconomics
        summary += "\nMACROECONOMIC ENVIRONMENT\n"
        summary += "-" * 30 + "\n"
        
        # GDP Growth
        if macro.real_gdp_growth_quarterly:
            latest_gdp_date = max(macro.real_gdp_growth_quarterly.keys())
            gdp_growth = macro.real_gdp_growth_quarterly[latest_gdp_date]
            summary += f"Real GDP Growth (Quarterly): {gdp_growth}%\n"
        
        # Unemployment
        if macro.unemployment_rate_monthly and 'data' in macro.unemployment_rate_monthly:
            latest_unemployment = macro.unemployment_rate_monthly['data'][0]['value']
            summary += f"Unemployment Rate: {latest_unemployment}%\n"
        
        # Interest Rates
        if macro.federal_funds_rate_daily and 'data' in macro.federal_funds_rate_daily:
            latest_fed_rate = macro.federal_funds_rate_daily['data'][0]['value']
            summary += f"Federal Funds Rate: {latest_fed_rate}%\n"
        
        # Treasury Yields
        treasury_yields = [
            ("3-Month", macro.treasury_yield_3month_daily),
            ("2-Year", macro.treasury_yield_2year_daily),
            ("10-Year", macro.treasury_yield_10year_daily),
            ("30-Year", macro.treasury_yield_30year_daily)
        ]
        
        for name, yield_data in treasury_yields:
            if yield_data and 'data' in yield_data and yield_data['data']:
                latest_yield = yield_data['data'][0]['value']
                summary += f"{name} Treasury: {latest_yield}%\n"
        
        # Yield curve analysis
        if (macro.treasury_yield_2year_daily and 'data' in macro.treasury_yield_2year_daily and
            macro.treasury_yield_10year_daily and 'data' in macro.treasury_yield_10year_daily):
            two_year = float(macro.treasury_yield_2year_daily['data'][0]['value'])
            ten_year = float(macro.treasury_yield_10year_daily['data'][0]['value'])
            yield_spread = ten_year - two_year
            summary += f"2-10 Year Spread: {yield_spread:.2f}% "
            summary += f"({'Inverted' if yield_spread < 0 else 'Normal'})\n"
        
        # Inflation
        if macro.consumer_price_index_monthly and 'data' in macro.consumer_price_index_monthly:
            latest_cpi = macro.consumer_price_index_monthly['data'][0]['value']
            summary += f"Consumer Price Index: {latest_cpi}\n"
        
        # Business cycle analysis
        if macro.bry_boschan_peak_trough and 'current_phase' in macro.bry_boschan_peak_trough:
            current_phase = macro.bry_boschan_peak_trough['current_phase']
            summary += f"Economic Cycle Phase: {current_phase.title()}\n"
        
        # Recent economic indicators
        summary += "\nRECENT ECONOMIC INDICATORS\n"
        summary += "-" * 30 + "\n"
        
        economic_indicators = [
            ("Retail Sales", macro.retail_sales_monthly),
            ("Durable Goods Orders", macro.durable_goods_monthly),
            ("Nonfarm Payrolls", macro.nonfarm_payrolls_monthly)
        ]
        
        for name, indicator_data in economic_indicators:
            if indicator_data and 'data' in indicator_data and indicator_data['data']:
                latest_value = indicator_data['data'][0]['value']
                latest_date = indicator_data['data'][0]['date']
                summary += f"{name}: {latest_value} ({latest_date})\n"
        
        summary += "\n" + "=" * 50 + "\n"
        summary += "END OF ANALYSIS\n"
        
        return summary
