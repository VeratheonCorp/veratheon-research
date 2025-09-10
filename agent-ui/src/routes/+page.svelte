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
  <div class="mb-8">
    <div class="card bg-base-100 shadow-lg border border-base-200">
      <div class="card-body p-6">
        <h2 class="card-title text-xl font-bold text-primary mb-4">Market Research Controls</h2>
        
        <div class="flex flex-wrap gap-6 items-end">
          <!-- Stock Symbol Input -->
          <div class="form-control">
            <label class="label pb-2">
              <span class="label-text font-medium text-base-content">Stock Symbol</span>
            </label>
            <input
              id="stock-symbol"
              type="text"
              placeholder="AAPL"
              class="input input-bordered input-primary w-24 focus:input-primary"
              bind:value={stockSymbol}
              disabled={isRunningResearch}
              on:keydown={(e) => {
                if (e.key === 'Enter' && !isRunningResearch && stockSymbol.trim()) {
                  runResearch();
                }
              }}
            />
          </div>

          <!-- Spacer -->
          <div class="flex-1"></div>

          <!-- Recompute and Button Group -->
          <div class="flex items-center gap-3">
            <!-- Recompute Checkbox -->
            <div class="flex items-center gap-2">
              <span class="text-sm text-base-content/70">Recompute</span>
              <input
                id="force-recompute"
                type="checkbox"
                class="checkbox checkbox-primary checkbox-lg"
                bind:checked={forceRecompute}
                disabled={isRunningResearch}
              />
            </div>
            
            <!-- Start Research Button -->
            <button
              class="btn btn-primary btn-lg shadow-md"
              class:btn-disabled={isRunningResearch || !stockSymbol.trim()}
              on:click={runResearch}
              disabled={isRunningResearch || !stockSymbol.trim()}
            >
              {#if isRunningResearch}
                <span class="loading loading-spinner loading-sm"></span>
                Analyzing...
              {:else}
                <span class="text-lg">🔍</span>
                Start Research
              {/if}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

<!-- Research & Status Unified Section -->
{#if isRunningResearch || statusUpdates.length > 0 || researchResult}
  <div class="mt-8">
    <!-- Unified Research Card -->
    <div class="card bg-base-100 shadow-2xl border border-primary/20">
      <div class="card-body p-8">
        <!-- Header with Status -->
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center gap-4">
            <div class="text-primary text-3xl">
              {#if isRunningResearch}
                <span class="loading loading-spinner loading-lg text-primary"></span>
              {:else if researchResult}
                📊
              {:else}
                ✅
              {/if}
            </div>
            <div>
              <h2 class="text-3xl font-bold text-primary">
                {#if isRunningResearch}
                  Research in Progress
                {:else if researchResult}
                  Research Results for {stockSymbol.toUpperCase()}
                {:else}
                  Research Complete
                {/if}
              </h2>
              <div class="flex items-center gap-3 mt-1">
                <p class="text-base-content/70">
                  {#if redisConnectionError}
                    Connection issues - status updates may be delayed
                  {:else if isRunningResearch}
                    Analyzing {stockSymbol.toUpperCase()} • Real-time updates
                  {:else if researchResult}
                    Comprehensive market analysis complete
                  {:else}
                    Analysis completed for {stockSymbol.toUpperCase()}
                  {/if}
                </p>
                {#if researchResult}
                  <div class="badge badge-primary badge-lg">Comprehensive Analysis</div>
                {/if}
              </div>
            </div>
          </div>
          
          <!-- Process Toggle Button -->
          {#if statusUpdates.length > 0}
            <div class="flex gap-2">
              <button 
                class="btn btn-outline btn-secondary"
                on:click={() => showModal = true}
              >
                View Process ({statusUpdates.length} steps)
              </button>
            </div>
          {/if}
        </div>

        <!-- Progress indicator for running research -->
        {#if isRunningResearch}
          <div class="mb-8">
            <div class="flex justify-between text-sm text-base-content/60 mb-2">
              <span>Research Progress</span>
              <span>{statusUpdates.length} steps completed</span>
            </div>
            <progress class="progress progress-primary w-full" value="{statusUpdates.length}" max="10"></progress>
            
            <!-- Current step indicator -->
            {#if statusUpdates.length > 0}
              <div class="mt-4 p-4 bg-primary/5 rounded-lg border border-primary/20">
                <div class="flex items-center gap-3">
                  <div class="w-3 h-3 rounded-full bg-primary animate-pulse"></div>
                  <div class="font-medium text-base-content">
                    {statusUpdates[statusUpdates.length - 1].details.flow ? 
                      statusUpdates[statusUpdates.length - 1].details.flow.replace(/_/g, ' ').replace(/flow/g, '').trim() : 
                      'Processing'}
                  </div>
                </div>
              </div>
            {:else}
              <div class="mt-4 p-4 bg-primary/5 rounded-lg">
                <div class="flex items-center gap-3">
                  <div class="loading loading-dots loading-sm text-primary"></div>
                  <p class="text-base-content/60">Initializing research pipeline...</p>
                </div>
              </div>
            {/if}
          </div>
        {/if}

        <!-- PROMINENT REPORT SECTION -->
        {#if researchResult?.comprehensive_report?.comprehensive_analysis}
          <!-- Critical Insights Section - Prominent display at top -->
          {#if researchResult.comprehensive_report.critical_insights}
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
                {@html renderMarkdown(researchResult.comprehensive_report.critical_insights)}
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
              {@html renderMarkdown(researchResult.comprehensive_report.comprehensive_analysis)}
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
        {:else if !isRunningResearch}
          <!-- Fallback when no report is available -->
          <div class="text-center py-12">
            <div class="text-6xl mb-4">📈</div>
            <h3 class="text-xl font-semibold mb-2">Research Complete</h3>
            <p class="text-base-content/70">
              Research analysis completed but comprehensive report is not available.
            </p>
          </div>
        {/if}
      </div>
    </div>
  </div>
{/if}

<!-- Process Details Modal -->
<div class="modal" class:modal-open={showModal}>
  <div class="modal-box max-w-4xl">
    <div class="flex items-center gap-3 mb-4">
      <div class="text-primary text-2xl">🔄</div>
      <h3 class="font-bold text-xl text-primary">Research Process Details</h3>
    </div>
    
    <div class="mb-4">
      <div class="stats shadow w-full">
        <div class="stat">
          <div class="stat-title">Total Steps</div>
          <div class="stat-value text-primary">{statusUpdates.length}</div>
        </div>
        <div class="stat">
          <div class="stat-title">Symbol</div>
          <div class="stat-value text-secondary">{stockSymbol.toUpperCase() || 'N/A'}</div>
        </div>
        <div class="stat">
          <div class="stat-title">Status</div>
          <div class="stat-value text-accent">
            {#if isRunningResearch}
              In Progress
            {:else}
              Complete
            {/if}
          </div>
        </div>
      </div>
    </div>
    
    <div class="py-4">
      {#if statusUpdates.length === 0}
        <div class="text-center py-8 text-base-content/60">
          No process steps recorded yet
        </div>
      {:else}
        <div class="space-y-3 max-h-96 overflow-y-auto">
          {#each statusUpdates as update (update)}
            <div class="card bg-base-100 shadow-sm border border-base-200">
              <div class="card-body p-4">
                <div class="flex justify-between items-start">
                  <div class="flex items-start gap-3 flex-1">
                    <div class="w-3 h-3 rounded-full mt-2 {update.status === 'completed' ? 'bg-success' : update.status === 'starting' ? 'bg-info' : 'bg-secondary'}"></div>
                    <div class="flex-1">
                      <div class="font-medium text-base-content mb-1">
                        {update.details.flow ? 
                          update.details.flow.replace(/_/g, ' ').replace(/flow/g, '').trim() : 
                          'Processing Step'}
                      </div>
                      <div class="text-sm text-base-content/60">
                        {#if update.details.duration_seconds}
                          Completed in {update.details.duration_seconds}s
                        {/if}
                        • {new Date(update.timestamp || Date.now()).toLocaleString()}
                      </div>
                    </div>
                  </div>
                  <div class="badge {update.status === 'completed' ? 'badge-success' : update.status === 'starting' ? 'badge-info' : 'badge-secondary'} badge-sm">
                    {update.status}
                  </div>
                </div>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
    
    <div class="modal-action">
      <button class="btn btn-primary" on:click={() => showModal = false}>Close</button>
    </div>
  </div>
</div>

</div>
