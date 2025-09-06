<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { flip } from 'svelte/animate';
  import { fade } from 'svelte/transition';
  import { createRedisSubscriber, type StatusUpdate } from '$lib/redis-subscriber';
  import HistoricalEarningsDisplay from '$lib/components/HistoricalEarningsDisplay.svelte';
  import FinancialStatementsDisplay from '$lib/components/FinancialStatementsDisplay.svelte';
  import EarningsProjectionsDisplay from '$lib/components/EarningsProjectionsDisplay.svelte';
  import ManagementGuidanceDisplay from '$lib/components/ManagementGuidanceDisplay.svelte';
  import PeerGroupDisplay from '$lib/components/PeerGroupDisplay.svelte';
  import ForwardPEValuationDisplay from '$lib/components/ForwardPEValuationDisplay.svelte';
  import NewsSentimentDisplay from '$lib/components/NewsSentimentDisplay.svelte';
  import TradeIdeasDisplay from '$lib/components/TradeIdeasDisplay.svelte';
  import type { ResearchResult } from '$lib/research-types';

  let statusUpdates: StatusUpdate[] = [];
  let subscriber = createRedisSubscriber();
  let stockSymbol = '';
  let isRunningResearch = false;
  let redisConnectionError = false;
  let researchResult: ResearchResult | null = null;
  let isUpdatesCollapsed = true;
  let slideOffset = 0;
  let isAnimating = false;
  let showModal = false;

  function slideUpdates() {
    if (isAnimating) return;
    isAnimating = true;
    slideOffset = 100;
    setTimeout(() => {
      slideOffset = 0;
      isAnimating = false;
    }, 800);
  }

  $: if (showModal) {
    // Scroll to bottom of modal when opened
    setTimeout(() => {
      const modalContent = document.querySelector('.modal-box .space-y-2');
      if (modalContent) {
        modalContent.scrollTop = modalContent.scrollHeight;
      }
    }, 10);
  }

  onMount(() => {
    console.log('Auto-subscribing to Redis status updates...');
    subscriber.subscribe(
      (data: StatusUpdate) => {
        console.log('Received status update:', data);
        statusUpdates = [...statusUpdates, data].slice(-20); // Keep only last 20 updates
        redisConnectionError = false; // Connection is working
      },
      (error) => {
        console.error('Status update error:', error);
        redisConnectionError = true;
      }
    );
  });

  async function runResearch() {
    if (!stockSymbol.trim()) {
      alert('Please enter a stock symbol');
      return;
    }
    
    // Clear old status updates for new research run
    statusUpdates = [];
    
    isRunningResearch = true;
    
    try {
      const response = await fetch('/api/research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ symbol: stockSymbol.trim().toUpperCase() })
      });
      
      if (!response.ok) {
        throw new Error(`Research failed: ${response.statusText}`);
      }
      
      const result = await response.json();
      console.log('Research completed:', result);
      researchResult = result as ResearchResult;
    } catch (error) {
      console.error('Research error:', error);
      alert(`Research failed: ${error.message}`);
    } finally {
      isRunningResearch = false;
    }
  }

  onDestroy(() => {
    subscriber.unsubscribe();
  });
</script>

<div class="container mx-auto p-6">
  <div class="mb-6">
    <div class="card bg-base-100 shadow">
      <div class="card-body">
        <h2 class="card-title">Research Controls</h2>
        <div class="flex flex-wrap gap-4 items-end">
          <div class="form-control">
            <label class="label" for="stock-symbol">
              <span class="label-text">Stock Symbol</span>
            </label>
            <input
              id="stock-symbol"
              type="text"
              placeholder="e.g., AAPL, MSFT, PG"
              class="input input-bordered w-40"
              bind:value={stockSymbol}
              disabled={isRunningResearch}
              on:keydown={(e) => {
                if (e.key === 'Enter' && !isRunningResearch && stockSymbol.trim()) {
                  runResearch();
                }
              }}
            />
          </div>

          <button
            class="btn btn-primary"
            on:click={runResearch}
            disabled={isRunningResearch || !stockSymbol.trim()}
          >
            {#if isRunningResearch}
              <span class="loading loading-spinner loading-sm"></span>
              Running Research...
            {:else}
              Run Research
            {/if}
          </button>

          {#if (statusUpdates.length > 0 && statusUpdates[statusUpdates.length - 1].status !== 'completed') || redisConnectionError}
            <!-- Divider -->
            <div class="divider divider-horizontal"></div>

            <!-- Status Display -->
            <div class="card bg-base-100 shadow-sm border border-base-300">
              <div class="card-body p-3">
                <div class="flex items-center justify-between">
                  <div>
                    {#if redisConnectionError}
                      <span class="text-xs text-error mr-4">Redis connection failed</span>
                    {:else if statusUpdates.length > 0}
                      <span class="text-xs text-base-content/70 mr-4">
                        {statusUpdates[statusUpdates.length - 1].details.flow || 'Processing'}...
                      </span>
                    {:else}
                      <span class="text-xs text-base-content/60 mr-4">Ready for research</span>
                    {/if}
                  </div>
                  {#if statusUpdates.length > 0}
                    <button class="btn btn-xs btn-outline" on:click={() => showModal = true}>
                      View All ({statusUpdates.length})
                    </button>
                  {/if}
                </div>
              </div>
            </div>
          {/if}
        </div>
      </div>
    </div>
  </div>

<!-- Status Updates Modal -->
<div class="modal" class:modal-open={showModal}>
  <div class="modal-box max-w-4xl">
    <h3 class="font-bold text-lg">Status Updates ({statusUpdates.length})</h3>
    <div class="py-4">
      {#if statusUpdates.length === 0}
        <div class="text-center py-8 text-base-content/60">
          No status updates yet
        </div>
      {:else}
        <div class="space-y-2 max-h-96 overflow-y-auto">
          {#each statusUpdates as update, index (update)}
            <div class="card bg-base-100 shadow-sm">
              <div class="card-body p-3">
                <div class="flex justify-between items-start">
                  <div class="flex-1">
                    <div class="text-sm font-medium">
                      {update.details.flow ? `${update.details.flow} for ${update.details.symbol || 'N/A'}${update.details.duration_seconds ? ` (${update.details.duration_seconds}s)` : ''}` : JSON.stringify(update.details)}
                    </div>
                    <div class="text-xs text-base-content/60 mt-1">
                      {new Date(update.timestamp || Date.now()).toLocaleString()}
                    </div>
                  </div>
                  <div class="badge {update.status === 'completed' ? 'badge-primary' : 'badge-secondary'} badge-sm ml-2">{update.status}</div>
                </div>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
    <div class="modal-action">
      <button class="btn" on:click={() => showModal = false}>Close</button>
    </div>
  </div>
</div>

<!-- Research Results Section -->
{#if researchResult}
  <div class="mt-8">
    <h2 class="text-2xl font-bold mb-6">Research Results for {stockSymbol.toUpperCase()}</h2>
    
    <!-- Historical Earnings Analysis -->
    {#if researchResult.historical_earnings_analysis}
      <div class="card bg-base-100 shadow mb-6">
        <div class="card-body">
          <h3 class="card-title text-lg">Historical Earnings Analysis</h3>
          <HistoricalEarningsDisplay analysis={researchResult.historical_earnings_analysis} />
        </div>
      </div>
    {/if}
    
    <!-- Financial Statements Analysis -->
    {#if researchResult.financial_statements_analysis}
      <FinancialStatementsDisplay analysis={researchResult.financial_statements_analysis} />
    {/if}

    <!-- Earnings Projections Analysis -->
    {#if researchResult.earnings_projections_analysis}
      <EarningsProjectionsDisplay analysis={researchResult.earnings_projections_analysis} />
    {/if}

    <!-- Management Guidance Analysis -->
    {#if researchResult.management_guidance_analysis}
      <ManagementGuidanceDisplay analysis={researchResult.management_guidance_analysis} />
    {/if}

    <!-- Forward PE Analysis -->
    {#if researchResult.forward_pe_valuation}
      <ForwardPEValuationDisplay analysis={researchResult.forward_pe_valuation} />
    {/if}

    <!-- News Sentiment Analysis -->
    {#if researchResult.news_sentiment_summary}
      <NewsSentimentDisplay analysis={researchResult.news_sentiment_summary} />
    {/if}

    <!-- Trade Ideas -->
    {#if researchResult.trade_idea}
      <TradeIdeasDisplay analysis={researchResult.trade_idea} />
    {/if}
  </div>
{/if}

</div>
