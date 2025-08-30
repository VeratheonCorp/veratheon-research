<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="min-h-dvh bg-base-200 text-base-content flex flex-col" data-theme="corporate">
  <header class="navbar bg-base-100 shadow">
    <div class="container mx-auto px-4">
      <div class="flex-1">
        <a class="btn btn-ghost text-xl">Market Research Agent</a>
      </div>
    </div>
  </header>

  <main class="container mx-auto px-4 py-6 flex-grow">
    {@render children?.()}
  </main>

  <footer class="footer footer-center bg-base-100 text-base-content p-4 border-t">
    <aside>
      <p class="text-sm">Built with SvelteKit, Tailwind CSS, and daisyUI</p>
    </aside>
  </footer>
</div>
