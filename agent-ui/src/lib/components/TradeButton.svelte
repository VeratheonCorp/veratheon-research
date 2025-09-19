<script lang="ts">
  import { TrendingUp } from '@lucide/svelte';
  
  export let symbol: string = '';
  export let companyName: string = '';
  export let variant: 'primary' | 'secondary' | 'accent' | 'success' | 'error' = 'primary';
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let disabled: boolean = false;
  
  // Event dispatcher for click event
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher<{
    click: { symbol: string; companyName: string };
  }>();
  
  function handleClick() {
    if (!disabled) {
      dispatch('click', { symbol, companyName });
    }
  }
  
  // Compute button classes based on props
  $: buttonClasses = `
    btn 
    btn-${variant} 
    ${size === 'sm' ? 'btn-sm' : size === 'lg' ? 'btn-lg' : ''} 
    ${disabled ? 'btn-disabled' : ''}
  `;
</script>

<button 
  class={buttonClasses} 
  on:click={handleClick}
  disabled={disabled}
  title={disabled ? 'Trading not available' : `Create trade hypothesis for ${symbol}`}
>
  <TrendingUp class="w-5 h-5" />
  <slot>Create Hypothesis</slot>
</button>
