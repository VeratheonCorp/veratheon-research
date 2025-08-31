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
    Earnings Projections Analysis
  </div>
  <div class="collapse-content">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="stat bg-base-200 rounded-lg">
        <div class="stat-title">Next Quarter EPS Projection</div>
        <div class="stat-value text-lg text-success">
          ${analysis.next_quarter_projection?.projected_eps?.toFixed(2) || 'N/A'}
        </div>
        <div class="stat-desc">Projected earnings per share</div>
      </div>
      <div class="stat bg-base-200 rounded-lg">
        <div class="stat-title">Overall Confidence</div>
        <div class="stat-value text-lg">
          <div class="badge badge-info badge-lg">
            {analysis.overall_confidence?.replace(/_/g, ' ') || 'N/A'}
          </div>
        </div>
      </div>
    </div>
    {#if analysis.detailed_analysis}
      <div class="mt-4 p-4 bg-base-200 rounded-lg">
        <p class="text-sm prose prose-sm max-w-none">{@html renderMarkdown(analysis.detailed_analysis)}</p>
      </div>
    {/if}
  </div>
</div>
