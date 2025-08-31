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
    News Sentiment Analysis
  </div>
  <div class="collapse-content">
    {#if analysis.overall_sentiment_label}
      <div class="mb-4 p-4 bg-base-200 rounded-lg">
        <h4 class="font-medium mb-2">Overall Sentiment</h4>
        <div class="badge badge-info badge-lg">
          {analysis.overall_sentiment_label?.replace(/_/g, ' ') || 'N/A'}
        </div>
      </div>
    {/if}
    {#if analysis.symbol}
      <div class="mb-4 p-4 bg-base-200 rounded-lg">
        <h4 class="font-medium mb-2">Symbol</h4>
        <p class="text-sm">{analysis.symbol}</p>
      </div>
    {/if}
    {#if analysis.news_sentiment_analysis}
      <div class="mb-4 p-4 bg-base-200 rounded-lg">
        <h4 class="font-medium mb-2">News Sentiment Analysis</h4>
        <p class="text-sm prose prose-sm max-w-none">{@html renderMarkdown(analysis.news_sentiment_analysis)}</p>
      </div>
    {/if}
  </div>
</div>
