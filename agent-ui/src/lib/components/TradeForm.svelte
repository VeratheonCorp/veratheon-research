<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { HelpCircle } from '@lucide/svelte';
  
  // Trade form properties
  export let symbol: string = '';
  export let companyName: string = '';
  
  // Trade types
  type InstrumentType = 'stock' | 'option';
  type Direction = 'long' | 'short';
  type OptionType = 'call' | 'put' | null;
  
  // Form data
  let instrumentType: InstrumentType = 'stock';
  let direction: Direction = 'long';
  let optionType: OptionType = null;
  let strikePrice: number | null = null;
  let expirationDate: string = '';
  let isHedge: boolean = false;
  let rationale: string = '';
  let isSubmitting = false;
  
  // Validation
  let errors: Record<string, string> = {};
  let formSubmitted = false;
  
  // Event dispatcher for form submission
  const dispatch = createEventDispatcher<{
    submit: {
      symbol: string;
      instrumentType: InstrumentType;
      direction: Direction;
      optionType: OptionType;
      strikePrice: number | null;
      expirationDate: string;
      isHedge: boolean;
      rationale: string;
    };
  }>();
  
  function validateForm(): boolean {
    errors = {};
    
    if (!symbol) {
      errors.symbol = 'Stock symbol is required';
    }
    
    if (instrumentType === 'option') {
      if (!optionType) {
        errors.optionType = 'Option type is required';
      }
      
      if (!strikePrice || strikePrice <= 0) {
        errors.strikePrice = 'Strike price must be greater than 0';
      }
      
      if (!expirationDate) {
        errors.expirationDate = 'Expiration date is required';
      }
    }
    
    return Object.keys(errors).length === 0;
  }
  
  async function handleSubmit() {
    formSubmitted = true;
    
    if (validateForm()) {
      isSubmitting = true;
      
      try {
        dispatch('submit', {
          symbol,
          instrumentType,
          direction,
          optionType,
          strikePrice,
          expirationDate,
          isHedge,
          rationale
        });
      } finally {
        // In a real implementation, we might want to wait for the submission to complete
        // before resetting the form or closing the modal
        isSubmitting = false;
      }
    }
  }
  
  // Reset form
  export function resetForm() {
    instrumentType = 'stock';
    direction = 'long';
    optionType = null;
    strikePrice = null;
    expirationDate = '';
    isHedge = false;
    rationale = '';
    errors = {};
    formSubmitted = false;
    isSubmitting = false;
  }
  
  // Reactive statement to handle instrument type changes
  $: if (instrumentType === 'stock') {
    optionType = null;
    strikePrice = null;
    expirationDate = '';
  } else if (instrumentType === 'option') {
    // For options, we always set direction to 'long' since we're hiding the direction selector
    direction = 'long';
  }
  
  // Get today's date in YYYY-MM-DD format for the min date in the date picker
  const today = new Date().toISOString().split('T')[0];
</script>

<div class="card bg-base-100 shadow-lg border border-base-200">
  <div class="card-body p-6">
    <h2 class="card-title text-xl font-bold text-primary mb-4">
      Trade Hypothesis
      {#if symbol}
        <span class="badge badge-secondary">{symbol}</span>
      {/if}
    </h2>
    
    {#if companyName}
      <p class="text-sm text-base-content/70 mb-4">{companyName}</p>
    {/if}
    
    <form on:submit|preventDefault={handleSubmit} class="space-y-4">
      <!-- Instrument Type Selection -->
      <div class="form-control">
        <span id="instrument-type-label" class="label">
          <span class="label-text font-medium">Instrument Type</span>
        </span>
        <div class="join w-full" id="instrument-type-group" role="radiogroup" aria-labelledby="instrument-type-label">
          <button 
            type="button"
            class="join-item btn flex-1 {instrumentType === 'stock' ? 'btn-primary' : 'btn-outline'}"
            on:click={() => instrumentType = 'stock'}
            aria-checked={instrumentType === 'stock'}
            role="radio"
          >
            Stock
          </button>
          <button 
            type="button"
            class="join-item btn flex-1 {instrumentType === 'option' ? 'btn-primary' : 'btn-outline'}"
            on:click={() => instrumentType = 'option'}
            aria-checked={instrumentType === 'option'}
            role="radio"
          >
            Option
          </button>
        </div>
      </div>
      
      <!-- Direction Selection (only for stocks) -->
      {#if instrumentType === 'stock'}
        <div class="form-control">
          <span id="direction-label" class="label">
            <span class="label-text font-medium">Direction</span>
          </span>
          <div class="join w-full" id="direction-group" role="radiogroup" aria-labelledby="direction-label">
            <button 
              type="button"
              class="join-item btn flex-1 {direction === 'long' ? 'btn-success' : 'btn-outline'}"
              on:click={() => direction = 'long'}
              aria-checked={direction === 'long'}
              role="radio"
            >
              Long
            </button>
            <button 
              type="button"
              class="join-item btn flex-1 {direction === 'short' ? 'btn-error' : 'btn-outline'}"
              on:click={() => direction = 'short'}
              aria-checked={direction === 'short'}
              role="radio"
            >
              Short
            </button>
          </div>
        </div>
      {/if}
      
      <!-- Option-specific fields -->
      {#if instrumentType === 'option'}
        <!-- Option Type Selection -->
        <div class="form-control">
          <span id="option-type-label" class="label">
            <span class="label-text font-medium">Option Type</span>
          </span>
          <div class="join w-full" id="option-type-group" role="radiogroup" aria-labelledby="option-type-label">
            <button 
              type="button"
              class="join-item btn flex-1 {optionType === 'call' ? 'btn-success' : 'btn-outline'}"
              on:click={() => optionType = 'call'}
              aria-checked={optionType === 'call'}
              role="radio"
            >
              Call
            </button>
            <button 
              type="button"
              class="join-item btn flex-1 {optionType === 'put' ? 'btn-error' : 'btn-outline'}"
              on:click={() => optionType = 'put'}
              aria-checked={optionType === 'put'}
              role="radio"
            >
              Put
            </button>
          </div>
          {#if errors.optionType && formSubmitted}
            <div class="label">
              <span class="label-text-alt text-error">{errors.optionType}</span>
            </div>
          {/if}
        </div>
        
        <!-- Strike Price -->
        <div class="form-control">
          <label for="strike-price" class="label">
            <span class="label-text font-medium">Strike Price ($)</span>
          </label>
          <input
            id="strike-price"
            type="number"
            min="0.01"
            step="0.01"
            placeholder="Enter strike price"
            class="input input-bordered w-full {errors.strikePrice && formSubmitted ? 'input-error' : ''}"
            bind:value={strikePrice}
          />
          {#if errors.strikePrice && formSubmitted}
            <div class="label">
              <span class="label-text-alt text-error">{errors.strikePrice}</span>
            </div>
          {/if}
        </div>
        
        <!-- Expiration Date -->
        <div class="form-control">
          <label for="expiration-date" class="label">
            <span class="label-text font-medium">Expiration Date</span>
          </label>
          <input
            id="expiration-date"
            type="date"
            min={today}
            class="input input-bordered w-full {errors.expirationDate && formSubmitted ? 'input-error' : ''}"
            bind:value={expirationDate}
          />
          {#if errors.expirationDate && formSubmitted}
            <div class="label">
              <span class="label-text-alt text-error">{errors.expirationDate}</span>
            </div>
          {/if}
        </div>
      {/if}
      
      <!-- Hedge Checkbox -->
      <div class="form-control">
        <label class="label cursor-pointer">
          <div class="flex items-center gap-2">
            <span class="label-text font-medium">Is this trade intended as a hedge?</span>
            <div class="tooltip tooltip-bottom" data-tip="A hedge is a trade that reduces risk exposure from other positions in your portfolio. This trade will be evaluated as a risk management strategy rather than a directional bet.">
              <HelpCircle class="w-4 h-4 text-info cursor-help" />
            </div>
          </div>
          <input 
            type="checkbox" 
            class="checkbox checkbox-primary" 
            bind:checked={isHedge}
          />
        </label>
      </div>
      
      <!-- Trade Rationale -->
      <div class="form-control">
        <label for="rationale" class="label">
          <span class="label-text font-medium">Trade Rationale (Optional)</span>
        </label>
        <textarea
          id="rationale"
          class="textarea textarea-bordered h-24"
          placeholder="Enter your rationale for this trade..."
          bind:value={rationale}
        ></textarea>
      </div>
      
      <!-- Submit Button -->
      <div class="form-control mt-6">
        <button type="submit" class="btn btn-primary" disabled={isSubmitting}>
          {#if isSubmitting}
            <span class="loading loading-spinner loading-sm"></span>
            Submitting...
          {:else}
            Submit Trade
          {/if}
        </button>
      </div>
    </form>
  </div>
</div>
