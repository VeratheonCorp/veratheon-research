<script lang="ts">
  export let analysis: any;
</script>

<div class="collapse collapse-arrow bg-base-100 shadow mb-4">
  <input type="checkbox" />
  <div class="collapse-title text-lg font-medium">
    Trade Ideas
  </div>
  <div class="collapse-content">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      {#if analysis.recommendation}
        <div class="stat bg-base-200 rounded-lg">
          <div class="stat-title">Recommendation</div>
          <div class="stat-value text-sm">
            <div class="badge badge-primary badge-lg">
              {analysis.recommendation?.replace(/_/g, ' ') || 'N/A'}
            </div>
          </div>
        </div>
      {/if}
      {#if analysis.confidence_score}
        <div class="stat bg-base-200 rounded-lg">
          <div class="stat-title">Confidence Score</div>
          <div class="stat-value text-lg">
            {analysis.confidence_score || 'N/A'}/100
          </div>
        </div>
      {/if}
    </div>
    {#if analysis.rationale}
      <div class="mt-4 p-4 bg-base-200 rounded-lg">
        <p class="text-sm whitespace-pre-wrap">{analysis.rationale}</p>
      </div>
    {/if}
  </div>
</div>
