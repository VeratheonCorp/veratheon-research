<script lang="ts">
  export let analysis: any;
</script>

<div class="collapse collapse-arrow bg-base-100 shadow mb-4">
  <input type="checkbox" />
  <div class="collapse-title text-lg font-medium">
    Peer Group Analysis
  </div>
  <div class="collapse-content">
    {#if analysis.peers && analysis.peers.length > 0}
      <div class="mb-4">
        <h4 class="font-medium mb-2">Comparable Companies</h4>
        <div class="flex flex-wrap gap-2">
          {#each analysis.peers as peer}
            <div class="badge badge-outline">{peer}</div>
          {/each}
        </div>
      </div>
    {/if}
    {#if analysis.comparison_summary}
      <div class="p-4 bg-base-200 rounded-lg">
        <p class="text-sm whitespace-pre-wrap">{analysis.comparison_summary}</p>
      </div>
    {/if}
  </div>
</div>
