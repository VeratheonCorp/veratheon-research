<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { onMount } from 'svelte';

	let { children } = $props();

	type Theme = 'light' | 'dark';
	let theme = $state<Theme>('light');
	let mobileMenuOpen = $state(false);
	let showDisclaimer = $state(false);

	const applyTheme = (t: Theme) => {
		// add a temporary class to animate color changes
		document.documentElement.classList.add('theme-transition');
		document.documentElement.setAttribute('data-theme', t);
		setTimeout(() => {
			document.documentElement.classList.remove('theme-transition');
		}, 500);
		try {
			localStorage.setItem('theme', t);
		} catch (e) {
			// ignore storage errors (e.g., SSR or privacy mode)
		}
	};

	const toggleTheme = () => {
		theme = theme === 'light' ? 'dark' : 'light';
		applyTheme(theme);
	};

	const toggleMobileMenu = () => {
		mobileMenuOpen = !mobileMenuOpen;
	};

	// Close mobile menu when clicking outside
	const handleClickOutside = (event: MouseEvent) => {
		const target = event.target as HTMLElement;
		if (mobileMenuOpen && !target.closest('.mobile-menu-container')) {
			mobileMenuOpen = false;
		}
	};

	const acceptDisclaimer = () => {
		try {
			sessionStorage.setItem('disclaimerAccepted', 'true');
		} catch (e) {
			// ignore storage errors
		}
		showDisclaimer = false;
	};

	onMount(() => {
		let saved: Theme | null = null;
		try {
			const v = localStorage.getItem('theme');
			if (v === 'light' || v === 'dark') saved = v;
		} catch (e) {
			// ignore
		}
		if (!saved) {
			const prefersDark =
				typeof window !== 'undefined' &&
				window.matchMedia &&
				window.matchMedia('(prefers-color-scheme: dark)').matches;
			saved = prefersDark ? 'dark' : 'light';
		}
		theme = saved;
		applyTheme(theme);

		// Check if disclaimer has been accepted
		try {
			const accepted = sessionStorage.getItem('disclaimerAccepted');
			if (!accepted) {
				showDisclaimer = true;
			}
		} catch (e) {
			// if sessionStorage fails, show disclaimer to be safe
			showDisclaimer = true;
		}

		// Add click outside listener
		document.addEventListener('click', handleClickOutside);
		return () => {
			document.removeEventListener('click', handleClickOutside);
		};
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="flex min-h-dvh flex-col bg-base-200">
  <div class="bg-base-100 shadow">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center h-16">
        <!-- Left: Title/Brand -->
        <div>
          <a class="text-xl font-bold" href="/">Market Research Agent</a>
        </div>
        
        <!-- Middle: Navigation (desktop only) -->
        <ul class="hidden md:flex space-x-4 mx-4">
          <li><a href="/" class="font-medium hover:text-primary">Home</a></li>
          <li><a href="/trades" class="font-medium hover:text-primary">Trades</a></li>
        </ul>
        
        <!-- Right: Theme Toggle + Mobile Menu -->
        <div class="flex items-center">
          <!-- Theme Toggle Button -->
          <button 
            class="p-2 rounded-full hover:bg-base-200" 
            aria-label="Toggle theme"
            onclick={toggleTheme}
          >
            {#if theme === 'dark'}
              <!-- Sun icon for light mode -->
              <svg
                class="h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <circle cx="12" cy="12" r="5"></circle>
                <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"></path>
              </svg>
            {:else}
              <!-- Moon icon for dark mode -->
              <svg
                class="h-5 w-5 fill-current"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"></path>
              </svg>
            {/if}
          </button>
          
          <!-- Mobile Menu Button (only on small screens) -->
          <div class="md:hidden ml-2 relative mobile-menu-container">
            <button 
              class="p-2 rounded-full hover:bg-base-200" 
              aria-label="Open menu"
              onclick={toggleMobileMenu}
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
              </svg>
            </button>
            {#if mobileMenuOpen}
              <div class="absolute right-0 mt-2 w-48 bg-base-100 rounded-md shadow-lg py-1 z-10">
                <a href="/" class="block px-4 py-2 hover:bg-base-200">Home</a>
                <a href="/trades" class="block px-4 py-2 hover:bg-base-200">Trades</a>
              </div>
            {/if}
          </div>
        </div>
      </div>
    </div>
  </div>

  <main class="container mx-auto w-full flex-1 px-4 py-6">
    {@render children?.()}
  </main>

  <footer class="footer-center footer bg-base-100 p-4 text-base-content">
    <aside>
      <div class="mt-2 flex items-center justify-center gap-4">
        <a
          href="https://svelte.dev"
          target="_blank"
          rel="noreferrer"
          class="inline-flex items-center"
          aria-label="Svelte"
        >
          <img
            alt="Svelte logo"
            src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Svelte_Logo.svg"
            class="h-6 w-auto opacity-80 transition-opacity hover:opacity-100"
          />
        </a>
        <a
          href="https://tailwindcss.com"
          target="_blank"
          rel="noreferrer"
          class="inline-flex items-center"
          aria-label="Tailwind CSS"
        >
          <img
            alt="Tailwind CSS logo"
            src="https://upload.wikimedia.org/wikipedia/commons/d/d5/Tailwind_CSS_Logo.svg"
            class="h-6 w-auto opacity-80 transition-opacity hover:opacity-100"
          />
        </a>
        <a
          href="https://daisyui.com"
          target="_blank"
          rel="noreferrer"
          class="inline-flex items-center"
          aria-label="daisyUI"
        >
          <img
            alt="daisyUI logo"
            src="https://img.daisyui.com/images/daisyui/mark.svg"
            class="h-6 w-auto opacity-80 transition-opacity hover:opacity-100"
          />
        </a>
      </div>
    </aside>
  </footer>
</div>

<!-- Disclaimer Modal -->
{#if showDisclaimer}
  <dialog class="modal modal-open">
    <div class="modal-box max-w-2xl">
      <h3 class="font-bold text-lg mb-4">Important Disclaimer</h3>

      <div class="space-y-4 text-sm">
        <p class="font-semibold text-warning">
          ⚠️ NOT FINANCIAL ADVICE
        </p>

        <p>
          This website is for <strong>informational and educational purposes only</strong>.
          The content provided is generated by Large Language Models (LLMs) and should NOT be
          used as the basis for any financial, investment, or trading decisions. Furthermore, this website is still actively under development.
        </p>

        <div class="bg-base-200 p-3 rounded-lg">
          <p class="font-semibold mb-2">Key Limitations:</p>
          <ul class="list-disc list-inside space-y-1 ml-2">
            <li>LLMs can and will <strong>hallucinate</strong> (generate false or misleading information)</li>
            <li>Analysis may be incomplete, inaccurate, or outdated</li>
            <li>No warranty or guarantee of accuracy is provided</li>
            <li>Past performance does not indicate future results</li>
          </ul>
        </div>

        <p>
          <strong>Always consult with a qualified financial advisor</strong> before making any
          investment decisions. You are solely responsible for your own financial decisions and
          any consequences thereof.
        </p>

        <div class="border-t border-base-300 pt-4 mt-4">
          <p class="text-error font-bold text-center text-base">
            Making investment decisions based solely on this AI-generated content is an exceptionally bad idea and will almost certainly result in your financial loss.
          </p>
        </div>

        <p class="text-xs opacity-70">
          By continuing to use this website, you acknowledge that you have read and understood
          this disclaimer and agree to use the information provided at your own risk.
        </p>
      </div>

      <div class="modal-action">
        <button class="btn btn-primary" onclick={acceptDisclaimer}>
          I Understand, and Accept
        </button>
      </div>
    </div>
  </dialog>
{/if}
