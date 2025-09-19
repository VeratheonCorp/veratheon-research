<script lang="ts">
  import { DollarSign, ArrowUpRight, ArrowDownRight, Calendar, HelpCircle } from '@lucide/svelte';
  import type { Trade } from '$lib/research-types';
  
  export let trades: Trade[] = [];
  export let showEmpty: boolean = true;
  
  // Format the expiration date
  function formatDate(dateString: string): string {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  }
  
  // Generate a display string for the trade
  function getTradeDisplayString(trade: Trade): string {
    let result = '';
    
    if (trade.instrumentType === 'stock') {
      result = `${trade.direction.toUpperCase()} ${trade.symbol}`;
    } else if (trade.instrumentType === 'option') {
      result = `${trade.symbol} ${trade.optionType?.toUpperCase()} @ $${trade.strikePrice} exp. ${formatDate(trade.expirationDate)}`;
    }
    
    if (trade.isHedge) {
      result += ' (Hedge)';
    }
    
    return result;
  }
</script>

<div class="card bg-base-100 shadow-lg border border-base-200">
  <div class="card-body p-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="card-title text-xl font-bold text-primary">Trade History</h2>
      <div class="badge badge-secondary badge-lg">{trades.length} Trades</div>
    </div>
    
    {#if trades.length === 0 && showEmpty}
      <div class="flex flex-col items-center justify-center py-8 text-base-content/60">
        <div class="text-4xl mb-4">
          <DollarSign class="w-12 h-12 opacity-40" />
        </div>
        <p class="text-lg font-medium mb-1">No trades yet</p>
        <p class="text-sm">Your trade history will appear here</p>
      </div>
    {:else}
      <div class="overflow-x-auto">
        <table class="table table-zebra w-full">
          <thead>
            <tr>
              <th>Trade</th>
              <th>Type</th>
              <th>Details</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {#each trades as trade (trade.id)}
              <tr class="hover:bg-base-200 cursor-pointer" title={trade.rationale || 'No rationale provided'}>
                <td class="font-medium">{trade.symbol}</td>
                <td>
                  <div class="flex flex-col gap-1">
                    {#if trade.instrumentType === 'stock'}
                      <div class="flex items-center gap-1">
                        {#if trade.direction === 'long'}
                          <span class="text-success flex items-center gap-1">
                            <ArrowUpRight class="w-4 h-4" />
                            Long
                          </span>
                        {:else}
                          <span class="text-error flex items-center gap-1">
                            <ArrowDownRight class="w-4 h-4" />
                            Short
                          </span>
                        {/if}
                      </div>
                    {:else}
                      <span class="badge {trade.optionType === 'call' ? 'badge-success' : 'badge-error'}">{trade.optionType}</span>
                    {/if}
                    
                    {#if trade.isHedge}
                      <div class="tooltip tooltip-bottom" data-tip="A hedge is a trade that reduces risk exposure from other positions in your portfolio. This trade will be evaluated as a risk management strategy rather than a directional bet.">
                        <span class="badge badge-sm badge-outline flex items-center gap-1">
                          Hedge
                          <HelpCircle class="w-3 h-3" />
                        </span>
                      </div>
                    {/if}
                  </div>
                </td>
                <td>
                  {#if trade.instrumentType === 'stock'}
                    Stock
                  {:else if trade.instrumentType === 'option'}
                    <div class="flex items-center gap-1">
                      <span>${trade.strikePrice}</span>
                      <span class="flex items-center gap-1 text-xs">
                        <Calendar class="w-3 h-3" />
                        {formatDate(trade.expirationDate)}
                      </span>
                    </div>
                  {/if}
                </td>
                <td>
                  <div class="badge {
                    trade.status === 'validated' ? 'badge-success' : 
                    trade.status === 'invalidated' ? 'badge-error' : 
                    'badge-warning'
                  }">
                    {trade.status}
                  </div>
                </td>
                <td class="text-sm text-base-content/70">
                  {new Date(trade.timestamp).toLocaleDateString()}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>
</div>
