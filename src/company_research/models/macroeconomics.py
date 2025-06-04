from typing import Dict, Any
from pydantic import BaseModel
from src.clients.alpha_vantage_client import AlphaVantageClient

class Macroeconomics(BaseModel):
    # Annual data fields
    real_gdp_annual:               Dict[str, Any] = {}
    federal_funds_rate_annual:     Dict[str, Any] = {}
    inflation_rate_annual:         Dict[str, Any] = {}
    nonfarm_payrolls_annual:       Dict[str, Any] = {}
    
    # Quarterly data fields
    real_gdp_quarterly:               Dict[str, Any] = {}
    real_gdp_per_capita_quarterly:    Dict[str, Any] = {}
    federal_funds_rate_quarterly:     Dict[str, Any] = {}
    nonfarm_payrolls_quarterly:       Dict[str, Any] = {}

    # Monthly data fields
    consumer_price_index_monthly:   Dict[str, Any] = {}
    retail_sales_monthly:       Dict[str, Any] = {}
    durable_goods_monthly:       Dict[str, Any] = {}
    unemployment_rate_monthly:      Dict[str, Any] = {}
    nonfarm_payrolls_monthly:     Dict[str, Any] = {}

    # Daily data fields
    treasury_yield_3month_daily:       Dict[str, Any] = {}
    treasury_yield_2year_daily:         Dict[str, Any] = {}
    treasury_yield_5year_daily:       Dict[str, Any] = {}
    treasury_yield_7year_daily:       Dict[str, Any] = {}
    treasury_yield_10year_daily:     Dict[str, Any] = {}
    treasury_yield_30year_daily:     Dict[str, Any] = {}
    federal_funds_rate_daily:     Dict[str, Any] = {}
    
    # Calculated fields
    real_gdp_growth_annual:           Dict[str, float] = {}
    real_gdp_growth_quarterly:        Dict[str, float] = {}
    bry_boschan_peak_trough:          Dict[str, Any] = {}

    def model_post_init(self, __context):
        self.fetch_all()
        self.real_gdp_growth_annual = self._calculate_real_gdp_growth(self.real_gdp_annual)
        self.real_gdp_growth_quarterly = self._calculate_real_gdp_growth(self.real_gdp_quarterly)
        self.bry_boschan_peak_trough = self._calculate_bry_boschan_peak_trough()

    def fetch_all(self) -> None:
        client = AlphaVantageClient()
        
        # Fetch annual data
        self.real_gdp_annual             = client.run_query("REAL_GDP&interval=annual")
        self.inflation_rate_annual       = client.run_query("INFLATION&interval=annual")
        self.nonfarm_payrolls_annual     = client.run_query("NONFARM_PAYROLL&interval=annual")
        
        # Fetch quarterly data
        self.real_gdp_quarterly             = client.run_query("REAL_GDP&interval=quarterly")
        self.real_gdp_per_capita_quarterly  = client.run_query("REAL_GDP_PER_CAPITA&interval=quarterly")

        # Fetch monthly data
        self.consumer_price_index_monthly   = client.run_query("CPI&interval=monthly")
        self.retail_sales_monthly         = client.run_query("RETAIL_SALES&interval=monthly")
        self.durable_goods_monthly       = client.run_query("DURABLES&interval=monthly")
        self.unemployment_rate_monthly      = client.run_query("UNEMPLOYMENT_RATE&interval=monthly")
        self.nonfarm_payrolls_monthly     = client.run_query("NONFARM_PAYROLL&interval=monthly")

        # Fetch treasury yield data
        self.treasury_yield_3month_daily    = client.run_query("TREASURY_YIELD_3MONTH&interval=daily")
        self.treasury_yield_2year_daily     = client.run_query("TREASURY_YIELD_2YEAR&interval=daily")
        self.treasury_yield_5year_daily     = client.run_query("TREASURY_YIELD_5YEAR&interval=daily")
        self.treasury_yield_7year_daily     = client.run_query("TREASURY_YIELD_7YEAR&interval=daily")
        self.treasury_yield_10year_daily    = client.run_query("TREASURY_YIELD_10YEAR&interval=daily")
        self.treasury_yield_30year_daily    = client.run_query("TREASURY_YIELD_30YEAR&interval=daily")

        # Fetch federal funds rate data
        self.federal_funds_rate_daily       = client.run_query("FEDERAL_FUNDS_RATE&interval=daily")


        

    def _calculate_real_gdp_growth(self, gdp_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate year-over-year real GDP growth rate for the most recent period."""
        if not gdp_data or 'data' not in gdp_data:
            return {}
        
        data_points = gdp_data['data']
        
        # Sort data by date to ensure proper chronological order (most recent first)
        sorted_data = sorted(data_points, key=lambda x: x['date'], reverse=True)
        
        if len(sorted_data) < 2:
            return {}
        
        # Get the two most recent data points
        current_value = float(sorted_data[0]['value'])
        previous_value = float(sorted_data[1]['value'])
        
        if previous_value != 0:
            growth_rate = ((current_value - previous_value) / previous_value) * 100
            return {sorted_data[0]['date']: round(growth_rate, 2)}
        
        return {}

    def _calculate_latest_unemployment_rate(self, unemployment_data: Dict[str, Any]) -> Dict[str, float]:
        """Get the most recent unemployment rate."""
        if not unemployment_data or 'data' not in unemployment_data:
            return {}
        
        data_points = unemployment_data['data']
        
        # Sort data by date to get the most recent data point
        sorted_data = sorted(data_points, key=lambda x: x['date'], reverse=True)
        
        if not sorted_data:
            return {}
        
        # Get the most recent unemployment rate
        latest_data = sorted_data[0]
        return {latest_data['date']: float(latest_data['value'])}

    def _calculate_bry_boschan_peak_trough(self) -> Dict[str, Any]:
        """
        Implement Bry-Boschan algorithm to identify business cycle peaks and troughs.
        Returns current economic cycle phase and turning points.
        """
        if not self.real_gdp_quarterly or 'data' not in self.real_gdp_quarterly:
            return {"error": "Insufficient GDP data for cycle analysis"}
        
        data_points = self.real_gdp_quarterly['data']
        
        # Sort data chronologically (oldest first for time series analysis)
        sorted_data = sorted(data_points, key=lambda x: x['date'])
        
        if len(sorted_data) < 6:  # Need minimum data points for cycle analysis
            return {"error": "Insufficient data points for cycle analysis"}
        
        # Extract values and dates
        values = [float(point['value']) for point in sorted_data]
        dates = [point['date'] for point in sorted_data]
        
        # Apply moving average smoothing (3-quarter)
        smoothed_values = self._apply_moving_average(values, window=3)
        
        # Identify preliminary peaks and troughs
        peaks = []
        troughs = []
        
        for i in range(2, len(smoothed_values) - 2):
            # Peak: value higher than 2 quarters before and after
            if (smoothed_values[i] > smoothed_values[i-1] and 
                smoothed_values[i] > smoothed_values[i+1] and
                smoothed_values[i] > smoothed_values[i-2] and 
                smoothed_values[i] > smoothed_values[i+2]):
                peaks.append((dates[i], smoothed_values[i], i))
            
            # Trough: value lower than 2 quarters before and after
            elif (smoothed_values[i] < smoothed_values[i-1] and 
                  smoothed_values[i] < smoothed_values[i+1] and
                  smoothed_values[i] < smoothed_values[i-2] and 
                  smoothed_values[i] < smoothed_values[i+2]):
                troughs.append((dates[i], smoothed_values[i], i))
        
        # Apply Bry-Boschan rules
        filtered_turning_points = self._apply_bry_boschan_rules(peaks, troughs)
        
        # Determine current cycle phase
        current_phase = self._determine_current_phase(filtered_turning_points, dates, smoothed_values)
        
        return {
            "turning_points": filtered_turning_points,
            "current_phase": current_phase,
            "latest_date": dates[-1] if dates else None,
            "analysis_period": f"{dates[0]} to {dates[-1]}" if dates else None
        }
    
    def _apply_moving_average(self, values: list, window: int) -> list:
        """Apply moving average smoothing to the data."""
        if len(values) < window:
            return values
        
        smoothed = []
        for i in range(len(values)):
            if i < window - 1:
                # For early points, use available data
                avg = sum(values[:i+1]) / (i + 1)
            elif i >= len(values) - window + 1:
                # For late points, use available data
                avg = sum(values[i:]) / (len(values) - i)
            else:
                # Standard moving average
                avg = sum(values[i-window+1:i+1]) / window
            smoothed.append(avg)
        
        return smoothed
    
    def _apply_bry_boschan_rules(self, peaks: list, troughs: list) -> list:
        """Apply Bry-Boschan rules to filter turning points."""
        all_points = []
        
        # Mark peaks and troughs
        for peak in peaks:
            all_points.append((peak[0], peak[1], peak[2], 'peak'))
        for trough in troughs:
            all_points.append((trough[0], trough[1], trough[2], 'trough'))
        
        # Sort by date
        all_points.sort(key=lambda x: x[0])
        
        # Rule 1: Alternating peaks and troughs
        filtered_points = []
        last_type = None
        
        for point in all_points:
            date, value, index, point_type = point
            
            if last_type != point_type:
                # Rule 2: Minimum duration between turning points (2 quarters)
                if not filtered_points or index - filtered_points[-1][2] >= 2:
                    filtered_points.append(point)
                    last_type = point_type
                elif point_type == 'peak' and value > filtered_points[-1][1]:
                    # Replace with higher peak
                    filtered_points[-1] = point
                elif point_type == 'trough' and value < filtered_points[-1][1]:
                    # Replace with lower trough
                    filtered_points[-1] = point
        
        return filtered_points
    
    def _determine_current_phase(self, turning_points: list, dates: list, values: list) -> str:
        """Determine the current economic cycle phase."""
        if not turning_points or len(turning_points) < 2:
            return "insufficient_data"
        
        latest_turning_point = turning_points[-1]
        latest_date = dates[-1]
        latest_value = values[-1]
        
        # Get the last turning point type and value
        last_point_type = latest_turning_point[3]
        last_point_value = latest_turning_point[1]
        
        # Determine phase based on last turning point and current trend
        if last_point_type == 'trough':
            # After a trough, check if we're recovering or expanding
            if latest_value > last_point_value * 1.02:  # 2% above trough
                return "expansion"
            else:
                return "recovery"
        
        elif last_point_type == 'peak':
            # After a peak, check if we're declining or have reached bottom
            if latest_value < last_point_value * 0.98:  # 2% below peak
                return "downturn"
            else:
                return "peak"
        
        return "unknown"

