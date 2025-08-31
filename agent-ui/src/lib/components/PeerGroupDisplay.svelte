<script lang="ts">
  import { marked } from 'marked';
  
  export let analysis: any;
  
  function renderMarkdown(text: string) {
    return marked(text);
  }
</script>

<div class="collapse collapse-arrow bg-base-100 shadow mb-4">
  <input type="checkbox" />
  <div class="collapse-title text-lg font-medium">
    Peer Group Analysis
  </div>
  <div class="collapse-content">
    {#if analysis.peer_group && analysis.peer_group.length > 0}
      <div class="mb-4">
        <h4 class="font-medium mb-2">Comparable Companies</h4>
        <div class="flex flex-wrap gap-2">
          {#each analysis.peer_group as peer}
            <div class="badge badge-outline">{peer}</div>
          {/each}
        </div>
      </div>
    {/if}
    {#if analysis.original_symbol}
      <div class="mb-4 p-4 bg-base-200 rounded-lg">
        <p class="text-sm prose prose-sm max-w-none">{@html renderMarkdown(analysis.comparison_summary || '')}</p>
      </div>
    {/if}
  </div>
</div>
