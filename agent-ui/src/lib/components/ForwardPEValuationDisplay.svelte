<script lang="ts">
  export let analysis: any;
</script>

<div class="collapse collapse-arrow bg-base-100 shadow mb-4">
  <input type="checkbox" />
  <div class="collapse-title text-lg font-medium">
    Forward PE Valuation
  </div>
  <div class="collapse-content">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      {#if analysis.current_forward_pe}
        <div class="stat bg-base-200 rounded-lg">
          <div class="stat-title">Current Forward PE</div>
          <div class="stat-value text-lg">{analysis.current_forward_pe?.toFixed(1) || 'N/A'}</div>
        </div>
      {/if}
      {#if analysis.fair_value_range}
        <div class="stat bg-base-200 rounded-lg">
          <div class="stat-title">Fair Value Range</div>
          <div class="stat-value text-sm">
            {analysis.fair_value_range?.min?.toFixed(1) || 'N/A'} - {analysis.fair_value_range?.max?.toFixed(1) || 'N/A'}
          </div>
        </div>
      {/if}
    </div>
    {#if analysis.valuation_summary}
      <div class="mt-4 p-4 bg-base-200 rounded-lg">
        <p class="text-sm whitespace-pre-wrap">{analysis.valuation_summary}</p>
      </div>
    {/if}
  </div>
</div>
