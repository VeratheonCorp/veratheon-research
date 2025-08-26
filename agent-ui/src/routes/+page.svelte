<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { createRedisSubscriber, type StatusUpdate } from '$lib/redis-subscriber';

  let statusUpdates: StatusUpdate[] = [];
  let subscriber = createRedisSubscriber();
  let stockSymbol = '';
  let isRunningResearch = false;
  let redisConnectionError = false;

  onMount(() => {
    console.log('Auto-subscribing to Redis status updates...');
    subscriber.subscribe(
      (data: StatusUpdate) => {
        console.log('Received status update:', data);
        statusUpdates = [...statusUpdates, data];
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

<div class="container mx-auto p-8">
  <h1 class="text-3xl font-bold mb-6">Market Research Agent - Status Updates</h1>
  
  <div class="mb-6">
    <h2 class="text-xl font-semibold mb-4">Research Controls</h2>
    
    <div class="flex gap-4 items-end mb-4">
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
        />
      </div>
      
      <button 
        class="btn btn-primary" 
        on:click={runResearch}
        disabled={isRunningResearch || !stockSymbol.trim()}
      >
        {isRunningResearch ? 'Running Research...' : 'Run Research'}
      </button>
    </div>
  </div>

  <div class="mb-4">
    <h2 class="text-xl font-semibold">Redis Pub/Sub Status Updates</h2>
    <p class="text-gray-600">Raw status messages from research flows:</p>
  </div>

  <div class="bg-black text-green-400 p-4 rounded-lg font-mono text-sm max-h-96 overflow-y-auto">
    {#if redisConnectionError}
      <div class="text-red-400">❌ Redis is not reachable - status updates unavailable</div>
    {:else if statusUpdates.length === 0}
      <div class="text-gray-500">Listening for status updates...</div>
    {/if}
    
    {#each statusUpdates as update, index}
      <div class="mb-2">
        <span class="text-gray-400">[{index + 1}]</span> 
        {JSON.stringify(update)}
      </div>
    {/each}
  </div>
  
  <div class="mt-4 text-sm text-gray-500">
    Total messages received: {statusUpdates.length}
  </div>
</div>