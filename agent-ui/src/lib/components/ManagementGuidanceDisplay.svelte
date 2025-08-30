<script lang="ts">
  export let analysis: any;
</script>

<div class="collapse collapse-arrow bg-base-100 shadow mb-4">
  <input type="checkbox" />
  <div class="collapse-title text-lg font-medium">
    Management Guidance Analysis
  </div>
  <div class="collapse-content">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="stat bg-base-200 rounded-lg">
        <div class="stat-title">Overall Guidance Tone</div>
        <div class="stat-value text-sm">
          <div class="badge badge-warning badge-lg">
            {analysis.overall_guidance_tone?.replace(/_/g, ' ') || 'N/A'}
          </div>
        </div>
      </div>
      <div class="stat bg-base-200 rounded-lg">
        <div class="stat-title">Consensus Validation</div>
        <div class="stat-value text-sm">
          <div class="badge badge-success badge-lg">
            {analysis.consensus_validation_signal?.replace(/_/g, ' ') || 'N/A'}
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
