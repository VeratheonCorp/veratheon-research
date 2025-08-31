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
    Forward PE Valuation
  </div>
  <div class="collapse-content">
    {#if analysis.analysis}
      <div class="mb-4 p-4 bg-base-200 rounded-lg">
        <h4 class="font-medium mb-2">Forward PE Analysis</h4>
        <p class="text-sm prose prose-sm max-w-none">{@html renderMarkdown(analysis.analysis)}</p>
      </div>
    {/if}
    {#if analysis.analysis_confidence_score}
      <div class="mb-4 p-4 bg-base-200 rounded-lg">
        <h4 class="font-medium mb-2">Confidence Score</h4>
        <p class="text-sm">{analysis.analysis_confidence_score}/100</p>
      </div>
    {/if}
  </div>
</div>
