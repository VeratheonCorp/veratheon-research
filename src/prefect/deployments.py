#!/usr/bin/env python3
"""
Prefect deployment registration script.
This script registers all flows as Prefect deployments for independent execution.
"""

import asyncio
from prefect import serve
from prefect.client.schemas.schedules import IntervalSchedule
from prefect.client.schemas.objects import WorkPool
from prefect.client.orchestration import get_client
from datetime import timedelta

# Import all flows
from src.prefect.flows.research_flow import main_research_flow
from src.prefect.flows.subflows.forward_pe_flow import forward_pe_flow, forward_pe_sanity_check_flow
from src.prefect.flows.subflows.trade_ideas_flow import trade_ideas_flow
from src.prefect.flows.subflows.news_sentiment_flow import news_sentiment_flow
from src.prefect.flows.subflows.historical_earnings_flow import historical_earnings_flow
from src.prefect.flows.subflows.financial_statements_flow import financial_statements_flow
from src.prefect.flows.subflows.earnings_projections_flow import earnings_projections_flow
from src.prefect.flows.subflows.management_guidance_flow import management_guidance_flow


async def create_deployments():
    """Create Prefect deployments for all flows."""
    
    deployments = []
    
    # Main research flow deployment
    main_deployment = await main_research_flow.to_deployment(
        name="main-research-deployment",
        description="Complete market research analysis for a given stock symbol",
        tags=["research", "main", "complete"],
        parameters={"symbol": "AAPL"},  # Default parameter
        work_pool_name="default-agent-pool",
    )
    deployments.append(main_deployment)
    
    # Historical earnings flow deployment
    historical_earnings_deployment = await historical_earnings_flow.to_deployment(
        name="historical-earnings-deployment",
        description="Analyze historical earnings patterns and trends",
        tags=["research", "historical", "earnings"],
        parameters={"symbol": "AAPL"},
        work_pool_name="default-agent-pool",
    )
    deployments.append(historical_earnings_deployment)
    
    # Financial statements flow deployment
    financial_statements_deployment = await financial_statements_flow.to_deployment(
        name="financial-statements-deployment",
        description="Analyze financial statements and trends",
        tags=["research", "financial", "statements"],
        parameters={"symbol": "AAPL"},
        work_pool_name="default-agent-pool",
    )
    deployments.append(financial_statements_deployment)
    
    # Earnings projections flow deployment
    earnings_projections_deployment = await earnings_projections_flow.to_deployment(
        name="earnings-projections-deployment",
        description="Generate independent earnings projections",
        tags=["research", "projections", "earnings"],
        parameters={
            "symbol": "AAPL",
            "historical_analysis_context": {},
            "financial_statements_context": {}
        },
        work_pool_name="default-agent-pool",
    )
    deployments.append(earnings_projections_deployment)
    
    # Management guidance flow deployment
    management_guidance_deployment = await management_guidance_flow.to_deployment(
        name="management-guidance-deployment",
        description="Analyze management guidance from earnings calls",
        tags=["research", "management", "guidance"],
        parameters={
            "symbol": "AAPL",
            "historical_earnings_analysis": {},
            "financial_statements_analysis": {}
        },
        work_pool_name="default-agent-pool",
    )
    deployments.append(management_guidance_deployment)
    
    # Forward PE sanity check flow deployment
    forward_pe_sanity_deployment = await forward_pe_sanity_check_flow.to_deployment(
        name="forward-pe-sanity-check-deployment",
        description="Perform forward PE sanity check on earnings data quality",
        tags=["research", "forward-pe", "sanity-check"],
        parameters={"symbol": "AAPL"},
        work_pool_name="default-agent-pool",
    )
    deployments.append(forward_pe_sanity_deployment)
    
    # Forward PE analysis flow deployment
    forward_pe_deployment = await forward_pe_flow.to_deployment(
        name="forward-pe-analysis-deployment",
        description="Analyze forward PE valuation metrics",
        tags=["research", "forward-pe", "valuation"],
        parameters={
            "symbol": "AAPL",
            "peer_group": {},
            "earnings_projections_analysis": {},
            "management_guidance_analysis": {},
            "forward_pe_sanity_check": {}
        },
        work_pool_name="default-agent-pool",
    )
    deployments.append(forward_pe_deployment)
    
    # News sentiment flow deployment
    news_sentiment_deployment = await news_sentiment_flow.to_deployment(
        name="news-sentiment-deployment",
        description="Analyze news sentiment for the stock and peers",
        tags=["research", "news", "sentiment"],
        parameters={
            "symbol": "AAPL",
            "peer_group": {},
            "earnings_projections_analysis": {},
            "management_guidance_analysis": {}
        },
        work_pool_name="default-agent-pool",
    )
    deployments.append(news_sentiment_deployment)
    
    # Trade ideas flow deployment
    trade_ideas_deployment = await trade_ideas_flow.to_deployment(
        name="trade-ideas-deployment",
        description="Generate trade ideas based on comprehensive analysis",
        tags=["research", "trade-ideas", "synthesis"],
        parameters={
            "symbol": "AAPL",
            "forward_pe_analysis": {},
            "news_sentiment_analysis": {},
            "historical_earnings_analysis": {},
            "financial_statements_analysis": {},
            "earnings_projections_analysis": {},
            "management_guidance_analysis": {}
        },
        work_pool_name="default-agent-pool",
    )
    deployments.append(trade_ideas_deployment)
    
    return deployments


async def ensure_work_pool_exists():
    """Ensure the default work pool exists."""
    async with get_client() as client:
        try:
            # Try to get the work pool
            await client.read_work_pool("default-agent-pool")
            print("✅ Work pool 'default-agent-pool' already exists")
        except Exception:
            # Work pool doesn't exist, create it
            print("Creating work pool 'default-agent-pool'...")
            work_pool = WorkPool(
                name="default-agent-pool",
                type="process",
                description="Default work pool for market research deployments"
            )
            await client.create_work_pool(work_pool)
            print("✅ Work pool 'default-agent-pool' created")


async def register_deployments():
    """Register all deployments with Prefect."""
    try:
        # First ensure work pool exists
        await ensure_work_pool_exists()
        
        print("Creating deployments...")
        deployments = await create_deployments()
        
        print(f"Registering {len(deployments)} deployments with Prefect...")
        
        # Register each deployment individually
        for deployment in deployments:
            print(f"  Registering: {deployment.name}")
            deployment_id = await deployment.apply()
            print(f"    ✅ Registered with ID: {deployment_id}")
        
        print("✅ All deployments registered successfully!")
        
        # Print deployment info
        print("\n📋 Registered Deployments:")
        for deployment in deployments:
            print(f"  • {deployment.name} - {deployment.description}")
            
        print(f"\n🎯 Access Prefect UI at: http://localhost:4200")
        print("   Navigate to Deployments to see all registered flows")
        
    except Exception as e:
        print(f"❌ Error registering deployments: {e}")
        raise


if __name__ == "__main__":
    print("🚀 Starting Prefect deployment registration...")
    asyncio.run(register_deployments())