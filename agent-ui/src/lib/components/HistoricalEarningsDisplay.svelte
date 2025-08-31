<script lang="ts">
  import type { HistoricalEarningsAnalysis, EarningsPattern, RevenueGrowthTrend, MarginTrend } from '$lib/research-types';
  import { marked } from 'marked';

  export let analysis: HistoricalEarningsAnalysis;

  function renderMarkdown(text: string) {
    return marked(text);
  }

  function getPatternBadgeClass(pattern: EarningsPattern): string {
    switch (pattern) {
      case 'CONSISTENT_BEATS':
        return 'badge-success';
      case 'CONSISTENT_MISSES':
        return 'badge-error';
      case 'MIXED_PATTERN':
        return 'badge-warning';
      case 'VOLATILE':
        return 'badge-error';
      case 'INSUFFICIENT_DATA':
        return 'badge-ghost';
      default:
        return 'badge-neutral';
    }
  }

  function getTrendBadgeClass(trend: RevenueGrowthTrend | MarginTrend): string {
    switch (trend) {
      case 'ACCELERATING':
      case 'IMPROVING':
      case 'STABLE':
        return 'badge-success';
      case 'DECELERATING':
      case 'DETERIORATING':
        return 'badge-warning';
      case 'DECLINING':
        return 'badge-error';
      case 'VOLATILE':
        return 'badge-error';
      case 'INSUFFICIENT_DATA':
        return 'badge-ghost';
      default:
        return 'badge-neutral';
    }
  }

  function formatEnumValue(value: string): string {
    return value.replace(/_/g, ' ').toLowerCase().replace(/\b\w/g, l => l.toUpperCase());
  }
</script>

<div class="card bg-base-100 shadow mb-6">
  <div class="card-body">
    <h2 class="card-title flex items-center gap-2">
      Historical Earnings Analysis
      <div class="badge badge-outline">{analysis.symbol}</div>
    </h2>
    
    <!-- Key Patterns Row -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
      <!-- Earnings Pattern -->
      <div class="stat bg-base-200 rounded-lg">
        <div class="stat-title">Earnings Pattern</div>
        <div class="stat-value text-lg">
          <div class="badge {getPatternBadgeClass(analysis.earnings_pattern)} badge-lg">
            {formatEnumValue(analysis.earnings_pattern)}
          </div>
        </div>
        <div class="stat-desc text-sm mt-2 prose prose-sm max-w-none whitespace-normal break-words">{@html renderMarkdown(analysis.earnings_pattern_details || '')}</div>
      </div>

      <!-- Revenue Growth Trend -->
      <div class="stat bg-base-200 rounded-lg">
        <div class="stat-title">Revenue Growth</div>
        <div class="stat-value text-lg">
          <div class="badge {getTrendBadgeClass(analysis.revenue_growth_trend)} badge-lg">
            {formatEnumValue(analysis.revenue_growth_trend)}
          </div>
        </div>
        <div class="stat-desc text-sm mt-2 prose prose-sm max-w-none whitespace-normal break-words">{@html renderMarkdown(analysis.revenue_growth_details || '')}</div>
      </div>

      <!-- Margin Trend -->
      <div class="stat bg-base-200 rounded-lg">
        <div class="stat-title">Margin Trend</div>
        <div class="stat-value text-lg">
          <div class="badge {getTrendBadgeClass(analysis.margin_trend)} badge-lg">
            {formatEnumValue(analysis.margin_trend)}
          </div>
        </div>
        <div class="stat-desc text-sm mt-2 prose prose-sm max-w-none whitespace-normal break-words">{@html renderMarkdown(analysis.margin_trend_details || '')}</div>
      </div>
    </div>

    <!-- Confidence Scores -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
      <div class="stat bg-base-200 rounded-lg">
        <div class="stat-title">Analysis Confidence</div>
        <div class="stat-value text-2xl flex items-center gap-2">
          {analysis.analysis_confidence_score}/100
          <progress class="progress progress-primary w-20" value={analysis.analysis_confidence_score} max="100"></progress>
        </div>
      </div>
      
      <div class="stat bg-base-200 rounded-lg">
        <div class="stat-title">Predictability Score</div>
        <div class="stat-value text-2xl flex items-center gap-2">
          {analysis.predictability_score}/100
          <progress class="progress progress-secondary w-20" value={analysis.predictability_score} max="100"></progress>
        </div>
      </div>
    </div>

    <!-- Key Insights -->
    {#if analysis.key_insights.length > 0}
      <div class="mt-6">
        <h3 class="text-lg font-semibold mb-3">Key Insights</h3>
        <div class="space-y-2">
          {#each analysis.key_insights as insight, index}
            <div class="alert alert-info">
              <span class="text-sm prose prose-sm max-w-none">{@html renderMarkdown(insight)}</span>
            </div>
          {/each}
        </div>
      </div>
    {/if}

    <!-- Full Analysis (Collapsible) -->
    <div class="collapse collapse-arrow bg-base-200 mt-6">
      <input type="checkbox" />
      <div class="collapse-title text-lg font-medium">
        Full Analysis Details
      </div>
      <div class="collapse-content">
        <div class="prose prose-sm max-w-none">
          <p>{@html renderMarkdown(analysis.full_analysis || '')}</p>
        </div>
      </div>
    </div>
  </div>
</div>