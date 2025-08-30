<script lang="ts">
  export let analysis: any;
</script>

<div class="collapse collapse-arrow bg-base-100 shadow mb-4">
  <input type="checkbox" />
  <div class="collapse-title text-lg font-medium">
    News Sentiment Analysis
  </div>
  <div class="collapse-content">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      {#if analysis.overall_sentiment}
        <div class="stat bg-base-200 rounded-lg">
          <div class="stat-title">Overall Sentiment</div>
          <div class="stat-value text-sm">
            <div class="badge badge-info badge-lg">
              {analysis.overall_sentiment?.replace(/_/g, ' ') || 'N/A'}
            </div>
          </div>
        </div>
      {/if}
      {#if analysis.sentiment_score}
        <div class="stat bg-base-200 rounded-lg">
          <div class="stat-title">Sentiment Score</div>
          <div class="stat-value text-lg">
            {analysis.sentiment_score?.toFixed(2) || 'N/A'}
          </div>
        </div>
      {/if}
    </div>
    {#if analysis.sentiment_summary}
      <div class="mt-4 p-4 bg-base-200 rounded-lg">
        <p class="text-sm whitespace-pre-wrap">{analysis.sentiment_summary}</p>
      </div>
    {/if}
  </div>
</div>
