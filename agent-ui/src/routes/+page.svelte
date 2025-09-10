<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { flip } from 'svelte/animate';
  import { fade } from 'svelte/transition';
  import { createRedisSubscriber, type StatusUpdate } from '$lib/redis-subscriber';
  import { marked } from 'marked';
  import type { ResearchResult } from '$lib/research-types';

  let statusUpdates: StatusUpdate[] = [];
  let subscriber = createRedisSubscriber();
  let stockSymbol = '';
  let forceRecompute = false;
  let isRunningResearch = false;
  let redisConnectionError = false;
  let researchResult: ResearchResult | null = null;
  let isUpdatesCollapsed = true;
  let slideOffset = 0;
  let isAnimating = false;
  let showModal = false;

  function renderMarkdown(text: string) {
    return marked(text);
  }

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
        body: JSON.stringify({ 
          symbol: stockSymbol.trim().toUpperCase(),
          force_recompute: forceRecompute
        })
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

          <div class="form-control">
            <label class="label" for="force-recompute">
              <span class="label-text">Force Recompute</span>
              <span class="label-text-alt text-xs">Skip cache</span>
            </label>
            <input
              id="force-recompute"
              type="checkbox"
              class="toggle toggle-secondary"
              bind:checked={forceRecompute}
              disabled={isRunningResearch}
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
    <div class="flex items-center gap-4 mb-6">
      <h2 class="text-3xl font-bold">Research Results for {stockSymbol.toUpperCase()}</h2>
      <div class="badge badge-primary badge-lg">Comprehensive Analysis</div>
    </div>
    
    <!-- Comprehensive Report with Rich Markdown Formatting -->
    {#if researchResult.comprehensive_analysis}
      <div class="card bg-base-100 shadow-xl border-2 border-base-200">
        <div class="card-body p-8">
          <div class="flex items-center gap-3 mb-6">
            <div class="text-primary text-2xl">📊</div>
            <h3 class="card-title text-2xl text-primary">Market Research Report</h3>
          </div>
          
          <!-- Critical Insights Section - Prominent display at top -->
          {#if researchResult.critical_insights}
            <div class="bg-gradient-to-r from-primary/15 to-secondary/15 rounded-xl p-8 border-2 border-primary/30 shadow-lg mb-8">
              <div class="flex items-center gap-4 mb-6">
                <div class="text-primary text-3xl">💡</div>
                <h3 class="text-2xl font-bold text-primary">Key Insights</h3>
              </div>
              
              <div class="prose prose-lg max-w-none
                          prose-headings:text-primary prose-headings:font-bold
                          prose-h1:text-2xl prose-h2:text-xl prose-h3:text-lg
                          prose-p:text-base-content prose-p:leading-relaxed prose-p:mb-4
                          prose-strong:text-primary prose-strong:font-semibold
                          prose-ol:space-y-3 prose-ul:space-y-3
                          prose-li:text-base-content prose-li:leading-relaxed prose-li:mb-2
                          prose-code:bg-primary/10 prose-code:px-2 prose-code:py-1 prose-code:rounded
                          prose-blockquote:border-l-4 prose-blockquote:border-primary 
                          prose-blockquote:bg-primary/5 prose-blockquote:p-4 prose-blockquote:rounded-r">
                {@html renderMarkdown(researchResult.critical_insights)}
              </div>
            </div>
          {/if}
          
          <div class="divider divider-primary"></div>
          
          <!-- Comprehensive Analysis Section -->
          <div class="mb-6">
            <div class="flex items-center gap-3 mb-4">
              <div class="text-secondary text-2xl">📈</div>
              <h3 class="text-xl font-bold text-secondary">Detailed Analysis</h3>
            </div>
            
            <div class="prose prose-lg max-w-none 
                        prose-headings:text-primary prose-headings:font-bold
                        prose-h1:text-3xl prose-h1:border-b prose-h1:border-primary prose-h1:pb-3
                        prose-h2:text-2xl prose-h2:text-secondary prose-h2:mt-8 prose-h2:mb-4
                        prose-h3:text-xl prose-h3:text-accent prose-h3:mt-6 prose-h3:mb-3
                        prose-p:text-base-content prose-p:leading-relaxed prose-p:mb-4
                        prose-strong:text-primary prose-strong:font-semibold
                        prose-ul:space-y-2 prose-ol:space-y-2
                        prose-li:text-base-content
                        prose-blockquote:border-l-4 prose-blockquote:border-primary 
                        prose-blockquote:bg-base-200 prose-blockquote:p-4 prose-blockquote:rounded-r
                        prose-code:bg-base-200 prose-code:px-2 prose-code:py-1 prose-code:rounded
                        prose-pre:bg-base-300 prose-pre:p-4 prose-pre:rounded-lg
                        prose-table:w-full prose-table:border-collapse
                        prose-th:bg-primary prose-th:text-primary-content prose-th:p-3
                        prose-td:border prose-td:border-base-300 prose-td:p-3
                        prose-hr:border-base-300 prose-hr:my-8">
              {@html renderMarkdown(researchResult.comprehensive_analysis)}
            </div>
          </div>
          
          <div class="divider divider-primary mt-8"></div>
          
          <!-- Report Footer -->
          <div class="flex justify-between items-center text-sm text-base-content/70 mt-4">
            <div class="flex items-center gap-2">
              <div class="badge badge-outline badge-sm">AI Generated</div>
              <div class="badge badge-outline badge-sm">Market Research Agent</div>
            </div>
            <div>
              Generated: {new Date().toLocaleString()}
            </div>
          </div>
        </div>
      </div>
    {:else}
      <!-- Fallback if no comprehensive report -->
      <div class="card bg-base-100 shadow">
        <div class="card-body text-center py-12">
          <div class="text-6xl mb-4">📈</div>
          <h3 class="text-xl font-semibold mb-2">Research Complete</h3>
          <p class="text-base-content/70">
            Research analysis completed but comprehensive report is not available.
          </p>
        </div>
      </div>
    {/if}
  </div>
{/if}

</div>
