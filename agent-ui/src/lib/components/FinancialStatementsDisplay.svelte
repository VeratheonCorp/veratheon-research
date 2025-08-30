<script lang="ts">
  export let analysis: any;
</script>

<div class="collapse collapse-arrow bg-base-100 shadow mb-4">
  <input type="checkbox" />
  <div class="collapse-title text-lg font-medium">
    Financial Statements Analysis
  </div>
  <div class="collapse-content">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="stat bg-base-200 rounded-lg">
        <div class="stat-title">Revenue Driver Trend</div>
        <div class="stat-value text-sm">
          <div class="badge badge-primary">
            {analysis.revenue_driver_trend?.replace(/_/g, ' ') || 'N/A'}
          </div>
        </div>
      </div>
      <div class="stat bg-base-200 rounded-lg">
        <div class="stat-title">Cost Structure Trend</div>
        <div class="stat-value text-sm">
          <div class="badge badge-secondary">
            {analysis.cost_structure_trend?.replace(/_/g, ' ') || 'N/A'}
          </div>
        </div>
      </div>
      <div class="stat bg-base-200 rounded-lg">
        <div class="stat-title">Working Capital Trend</div>
        <div class="stat-value text-sm">
          <div class="badge badge-accent">
            {analysis.working_capital_trend?.replace(/_/g, ' ') || 'N/A'}
          </div>
        </div>
      </div>
    </div>
    {#if analysis.full_analysis}
      <div class="mt-4 p-4 bg-base-200 rounded-lg">
        <p class="text-sm whitespace-pre-wrap">{analysis.full_analysis}</p>
      </div>
    {/if}
  </div>
</div>
