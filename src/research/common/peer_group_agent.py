from agents import Agent, Runner, RunResult
from src.research.common.models.peer_group import PeerGroup
import openai
import json
from src.lib.llm_model import get_model

SYSTEM_INSTRUCTIONS = """
You are a financial analyst performing a comparable-company (“comps”) analysis for forward P/E comparison.

INSTRUCTIONS:
- Given an original symbol, identify what market segment it belongs to.
- Identify 2 to 4 public companies whose business models, scale and growth profiles most closely resemble it.  
- Focus on similarities in core products/services, market-cap range, revenue/growth trajectory and investor expectations.  
- Exclude companies that, despite superficial overlaps, differ dramatically in size, profitability or market positioning (e.g. Fitbit vs. Apple)

IMPORTANT: 
- Companies must belong to the same market segment, not simply sharing broadly similar business models.
- Only the NYSE and NASDAQ exchanges are supported. For example, SSNFL trades on the OTC market and would not be included in the peer group.
- Only public companies are supported.

CRITICALLY IMPORTANT:
- EACH COMPANY MUST BE IN THE FORM OF A STOCK SYMBOL.
"""

_peer_group_agent = Agent(
            name="Peer Group Analyst",      
            model=get_model(),
            output_type=PeerGroup,
            # TODO: Allow Web Search Tool
            instructions=SYSTEM_INSTRUCTIONS
        )

async def peer_group_agent(symbol: str) -> PeerGroup:
    result: RunResult = await Runner.run(_peer_group_agent, input=f"original_symbol: {symbol}")
    peer_group: PeerGroup = result.final_output
    return peer_group


async def peer_group_chatcompletion(symbol: str) -> PeerGroup:
    response = openai.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user",   "content": f"original_symbol: {symbol}"}
        ],
        #temperature=0.0,
    )
    content = response.choices[0].message.content
    data = json.loads(content)
    return PeerGroup(**data)

