import asyncio
import os
from dotenv import load_dotenv
from src.reseacher import Researcher

# Load environment variables from .env file
load_dotenv()

async def main() -> None:
    symbol = "AAPL"
    price_target = 250
    timeframe = "6 months"
    await Researcher().run(symbol, price_target, timeframe)


if __name__ == "__main__":
    asyncio.run(main())
