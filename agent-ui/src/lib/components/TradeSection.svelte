<script lang="ts">
  import { onMount } from 'svelte';
  import TradeButton from './TradeButton.svelte';
  import TradeModal from './TradeModal.svelte';
  import TradeHistory from './TradeHistory.svelte';
  import type { Trade, TradeDetails } from '$lib/research-types';
  import { DollarSign } from '@lucide/svelte';
  
  export let symbol: string = '';
  export let companyName: string = '';
  
  let isTradeModalOpen = false;
  let trades: Trade[] = [];
  
  let isLoading = false;
  let error: string | null = null;
  
  // Handle trade submission
  async function handleTradeSubmit(event: CustomEvent<TradeDetails>) {
    const tradeDetails = event.detail;
    isLoading = true;
    error = null;
    
    try {
      // Create a unique ID for the trade
      const tradeId = `trade_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
      
      // In a real implementation, this would be sent to the backend for validation
      // For now, we'll create a mock trade with pending status
      const newTrade: Trade = {
        ...tradeDetails,
        id: tradeId,
        timestamp: new Date().toISOString(),
        status: 'pending'
      };
      
      // Add the new trade to the list
      trades = [newTrade, ...trades];
      
      // In the future, this would trigger validation against the research data
      console.log('Trade submitted for validation:', newTrade);
    } catch (err) {
      error = 'An error occurred while submitting the trade';
      console.error('Trade submission error:', err);
    } finally {
      isLoading = false;
    }
  }
  
  // Initialize with mock data on mount
  onMount(() => {
    if (symbol) {
      // In a real implementation, this would fetch trades from the backend
      // For now, we'll use mock data
      const mockTrades: Trade[] = [];
      trades = mockTrades;
    }
  });
</script>

<div class="space-y-8">
  <!-- Trade Action Section -->
  <div class="card bg-base-100 shadow-lg border border-base-200">
    <div class="card-body p-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="card-title text-xl font-bold text-primary">Trade Actions</h2>
          {#if companyName}
            <p class="text-sm text-base-content/70">{companyName}</p>
          {/if}
        </div>
        {#if symbol}
          <div class="badge badge-lg">{symbol}</div>
        {/if}
      </div>
      
      {#if symbol}
        <div class="flex flex-col sm:flex-row gap-4 items-center">
          <div class="flex-1">
            <p class="text-base-content">
              Ready to execute a trade based on the research analysis?
            </p>
          </div>
          <div>
            <TradeButton 
              {symbol} 
              {companyName} 
              variant="primary" 
              size="lg" 
              on:click={() => isTradeModalOpen = true}
            >
              Create Trade
            </TradeButton>
          </div>
        </div>
      {:else}
        <div class="flex flex-col items-center justify-center py-8 text-base-content/60">
          <div class="text-4xl mb-4">
            <DollarSign class="w-12 h-12 opacity-40" />
          </div>
          <p class="text-lg font-medium mb-1">No stock selected</p>
          <p class="text-sm">Run research on a stock to enable trading</p>
        </div>
      {/if}
    </div>
  </div>
  
  <!-- Trade History Section -->
  {#if symbol}
    {#if isLoading}
      <div class="card bg-base-100 shadow-lg border border-base-200">
        <div class="card-body p-6 flex items-center justify-center">
          <div class="flex flex-col items-center py-8">
            <div class="loading loading-spinner loading-lg text-primary mb-4"></div>
            <p class="text-base-content/70">Loading trades...</p>
          </div>
        </div>
      </div>
    {:else if error}
      <div class="card bg-base-100 shadow-lg border border-error/30">
        <div class="card-body p-6">
          <div class="flex items-center gap-3 text-error mb-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="font-medium">Error loading trades</h3>
          </div>
          <p class="text-base-content/70">{error}</p>
          <div class="card-actions justify-end mt-4">
            <button class="btn btn-sm btn-outline" on:click={() => window.location.reload()}>Retry</button>
          </div>
        </div>
      </div>
    {:else}
      <TradeHistory trades={trades} />
    {/if}
  {/if}
  
  <!-- Trade Modal -->
  <TradeModal 
    isOpen={isTradeModalOpen} 
    {symbol} 
    {companyName} 
    on:close={() => isTradeModalOpen = false}
    on:submit={handleTradeSubmit}
  />
</div>
