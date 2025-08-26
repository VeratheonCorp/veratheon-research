<script lang="ts">
  import { onDestroy } from 'svelte';
  import { createRedisSubscriber, type StatusUpdate } from '$lib/redis-subscriber';

  let statusUpdates: StatusUpdate[] = [];
  let subscriber = createRedisSubscriber();
  let isSubscribed = false;

  function toggleSubscription() {
    if (isSubscribed) {
      console.log('Unsubscribing from Redis status updates...');
      subscriber.unsubscribe();
      isSubscribed = false;
    } else {
      console.log('Subscribing to Redis status updates...');
      subscriber.subscribe(
        (data: StatusUpdate) => {
          console.log('Received status update:', data);
          statusUpdates = [...statusUpdates, data];
        },
        (error) => {
          console.error('Status update error:', error);
        }
      );
      isSubscribed = true;
    }
  }

  onDestroy(() => {
    subscriber.unsubscribe();
  });
</script>

<div class="container mx-auto p-8">
  <h1 class="text-3xl font-bold mb-6">Market Research Agent - Status Updates</h1>
  
  <div class="mb-4">
    <h2 class="text-xl font-semibold">Redis Pub/Sub Status Updates</h2>
    <p class="text-gray-600">Raw status messages from research flows:</p>
    
    <button 
      class="btn {isSubscribed ? 'btn-error' : 'btn-success'} mt-2"
      on:click={toggleSubscription}
    >
      {isSubscribed ? 'Stop Listening' : 'Start Listening'}
    </button>
  </div>

  <div class="bg-black text-green-400 p-4 rounded-lg font-mono text-sm max-h-96 overflow-y-auto">
    {#if !isSubscribed}
      <div class="text-gray-500">Click "Start Listening" to begin receiving status updates...</div>
    {:else if statusUpdates.length === 0}
      <div class="text-gray-500">Listening for status updates...</div>
    {/if}
    
    {#each statusUpdates as update, index}
      <div class="mb-2">
        <span class="text-gray-400">[{index + 1}]</span> 
        {JSON.stringify(update)}
      </div>
    {/each}
  </div>
  
  <div class="mt-4 text-sm text-gray-500">
    Total messages received: {statusUpdates.length}
  </div>
</div>