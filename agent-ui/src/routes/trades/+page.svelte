<script lang="ts">
  import { onMount } from 'svelte';
  import TradeSection from '$lib/components/TradeSection.svelte';
  import { DollarSign } from '@lucide/svelte';
  import TickerSearch from '$lib/components/TickerSearch.svelte';

  let symbol = '';
  let companyName = '';
  
  // Get symbol from URL query parameter if available
  onMount(() => {
    if (typeof window !== 'undefined') {
      const urlParams = new URLSearchParams(window.location.search);
      const urlSymbol = urlParams.get('symbol');
      if (urlSymbol) {
        symbol = urlSymbol.toUpperCase();
      }
    }
  });
</script>

<div class="container mx-auto p-6">
  <div class="mb-8">
    <h1 class="text-3xl font-bold text-primary mb-4">Trade Management</h1>
    <p class="text-base-content/70">Create and manage your trades based on market research insights.</p>
  </div>

  <!-- Symbol Input -->
  <div class="card bg-base-100 shadow-lg border border-base-200 mb-8">
    <div class="card-body p-6">
      <h2 class="card-title text-xl font-bold text-primary mb-4">Select Stock</h2>
      
      <div class="flex flex-wrap gap-4 items-end">
        <div class="form-control w-80">
          <label for="stock-symbol" class="label pb-2">
            <span class="label-text font-medium text-base-content">Stock Symbol or Company Name</span>
          </label>
          <div class="w-full">
            <TickerSearch 
              placeholder="Search for a stock..."
              on:select={(e) => {
                symbol = e.detail.symbol;
                companyName = e.detail.name;
              }}
            />
          </div>
        </div>
        
        <button 
          class="btn btn-primary"
          disabled={!symbol.trim()}
          on:click={() => {
            if (symbol.trim()) {
              // Update URL with the symbol
              const url = new URL(window.location.href);
              url.searchParams.set('symbol', symbol.trim().toUpperCase());
              window.history.pushState({}, '', url);
            }
          }}
        >
          <DollarSign class="w-5 h-5" />
          Use {symbol ? symbol.toUpperCase() : 'Symbol'}
        </button>
        
        {#if companyName}
          <div class="text-sm text-base-content/70">{companyName}</div>
        {/if}
      </div>
    </div>
  </div>

  <!-- Trade Section -->
  <TradeSection {symbol} {companyName} />
</div>
