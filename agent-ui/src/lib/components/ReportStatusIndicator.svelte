<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { CheckCircle } from '@lucide/svelte';

  export let symbol: string = '';
  export let size: string = 'md'; // sm, md, lg

  let hasReport: boolean = false;
  let isLoading: boolean = false;
  let error: string | null = null;
  let completedAt: string | null = null;

  let debounceTimer: ReturnType<typeof setTimeout> | null = null;
  
  $: if (symbol) {
    // Clear any existing timer
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
    
    // Set a new timer with 1000ms delay
    debounceTimer = setTimeout(() => {
      checkReportStatus();
    }, 1000);
  }

  async function checkReportStatus() {
    if (!symbol.trim()) return;
    
    isLoading = true;
    error = null;
    
    try {
      const response = await fetch(`/api/research/report-status/${symbol.trim().toUpperCase()}`);
      
      if (!response.ok) {
        throw new Error(`Failed to check report status: ${response.statusText}`);
      }
      
      const data = await response.json();
      hasReport = data.has_report;
      completedAt = data.completed_at;
      
    } catch (err) {
      console.error('Error checking report status:', err);
      error = err.message || 'Failed to check report status';
      hasReport = false;
    } finally {
      isLoading = false;
    }
  }

  // Format the completed date for the tooltip
  $: formattedDate = completedAt ? new Date(completedAt).toLocaleString() : '';
  
  // Determine size classes based on the size prop
  $: iconSize = size === 'sm' ? 'w-4 h-4' : size === 'lg' ? 'w-6 h-6' : 'w-5 h-5';
  $: tooltipSize = size === 'sm' ? 'tooltip-sm' : size === 'lg' ? 'tooltip-lg' : '';
  
  // Clean up the timer when component is destroyed
  onDestroy(() => {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
  });
</script>

{#if symbol && !isLoading && hasReport}
  <div class="tooltip {tooltipSize}" data-tip="Comprehensive report already available for {symbol.toUpperCase()} (completed on {formattedDate})">
    <CheckCircle class="{iconSize} text-success" />
  </div>
{:else if isLoading}
  <div class="loading loading-spinner loading-xs text-base-content/50"></div>
{/if}
