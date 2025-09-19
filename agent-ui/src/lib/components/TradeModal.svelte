<script lang="ts">
  import TradeForm from './TradeForm.svelte';
  import { createEventDispatcher } from 'svelte';
  import type { TradeDetails } from '$lib/research-types';
  
  export let isOpen = false;
  export let symbol: string = '';
  export let companyName: string = '';
  
  // Create a reference to the TradeForm component
  let tradeFormComponent: TradeForm;
  
  const dispatch = createEventDispatcher<{
    close: void;
    submit: TradeDetails;
  }>();
  
  function handleClose() {
    dispatch('close');
  }
  
  function handleSubmit(event: CustomEvent) {
    dispatch('submit', event.detail);
    handleClose();
  }
  
  // Reset form when modal is opened
  $: if (isOpen && tradeFormComponent) {
    tradeFormComponent.resetForm();
  }
</script>

<div class="modal {isOpen ? 'modal-open' : ''}" on:click|self={handleClose} on:keydown={(e) => e.key === 'Escape' && handleClose()} role="dialog" aria-modal="true" aria-label="Trade specification" tabindex="-1">
  <div class="modal-box max-w-md">
    <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" on:click={handleClose}>✕</button>
    
    <TradeForm 
      bind:this={tradeFormComponent}
      {symbol} 
      {companyName} 
      on:submit={handleSubmit} 
    />
  </div>
</div>
