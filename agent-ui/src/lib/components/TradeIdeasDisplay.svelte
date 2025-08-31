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
    Trade Ideas
  </div>
  <div class="collapse-content">
    {#if analysis.high_level_trade_idea}
      <div class="mb-4 p-4 bg-base-200 rounded-lg">
        <h4 class="font-medium mb-2">Trade Idea</h4>
        <p class="text-sm prose prose-sm max-w-none">{@html renderMarkdown(analysis.high_level_trade_idea)}</p>
      </div>
    {/if}
    {#if analysis.reasoning}
      <div class="mb-4 p-4 bg-base-200 rounded-lg">
        <h4 class="font-medium mb-2">Reasoning</h4>
        <p class="text-sm prose prose-sm max-w-none">{@html renderMarkdown(analysis.reasoning)}</p>
      </div>
    {/if}
    {#if analysis.simple_equity_trade_specifics}
      <div class="mb-4 p-4 bg-base-200 rounded-lg">
        <h4 class="font-medium mb-2">Equity Trade Specifics</h4>
        <p class="text-sm prose prose-sm max-w-none">{@html renderMarkdown(analysis.simple_equity_trade_specifics)}</p>
        {#if analysis.simple_equity_trade_specifics_confidence_score}
          <p class="text-xs text-base-content/70 mt-1">Confidence: {analysis.simple_equity_trade_specifics_confidence_score}/100</p>
        {/if}
      </div>
    {/if}
    {#if analysis.option_play}
      <div class="mb-4 p-4 bg-base-200 rounded-lg">
        <h4 class="font-medium mb-2">Option Strategy</h4>
        <p class="text-sm prose prose-sm max-w-none">{@html renderMarkdown(analysis.option_play)}</p>
        {#if analysis.option_play_confidence_score}
          <p class="text-xs text-base-content/70 mt-1">Confidence: {analysis.option_play_confidence_score}/100</p>
        {/if}
      </div>
    {/if}
    {#if analysis.risk_hedge}
      <div class="mb-4 p-4 bg-base-200 rounded-lg">
        <h4 class="font-medium mb-2">Risk Management</h4>
        <p class="text-sm prose prose-sm max-w-none">{@html renderMarkdown(analysis.risk_hedge)}</p>
      </div>
    {/if}
  </div>
</div>
