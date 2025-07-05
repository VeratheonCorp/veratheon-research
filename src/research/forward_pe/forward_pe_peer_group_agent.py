from agents import Agent
from src.research.forward_pe.forward_pe_models import PeerGroup

peer_group_agent = Agent(
            name="Peer Group Analyst",      
            model="o4-mini",
            output_type=PeerGroup,
            # TODO: Allow Web Search Tool
            instructions="""
            You are a financial analyst performing a comparable-company (“comps”) analysis for forward P/E comparison.

            • Given an original symbol, identify 3-10 public companies whose business models, scale and growth profiles most closely resemble it.  
            • Focus on similarities in core products/services, market-cap range, revenue/growth trajectory and investor expectations.  
            • Exclude companies that, despite superficial overlaps, differ dramatically in size, profitability or market positioning (e.g. Fitbit vs. Apple).

            Return a JSON object:
            {
                "original_symbol": "Ticker0",
                "peer_group": [ "Ticker1", "Ticker2", … ],
                "errors": [ "" ]
            }
            """
        )