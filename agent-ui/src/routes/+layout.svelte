<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { supabase } from '$lib/supabase';
	import UserAvatar from '$lib/components/UserAvatar.svelte';
	import type { User } from '$lib/types/auth';

	let { children } = $props();

	type Theme = 'light' | 'dark';
	let theme = $state<Theme>('light');
	let mobileMenuOpen = $state(false);
	let showDisclaimer = $state(false);
	let user = $state<User | null>(null);
	let authLoading = $state(true);

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
		// Theme setup
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

		// Add click outside listener
		document.addEventListener('click', handleClickOutside);

		// Auth check
		const checkAuth = async () => {
			const {
				data: { user: currentUser }
			} = await supabase!.auth.getUser();

			user = currentUser;
			authLoading = false;

			// Redirect to login if not authenticated and not on login page
			const currentPath = window.location.pathname;
			if (!currentUser && currentPath !== '/login') {
				goto('/login');
			} else if (currentUser && currentPath === '/login') {
				goto('/');
			}

			// Check if disclaimer has been accepted (only for authenticated users)
			if (currentUser) {
				try {
					const accepted = sessionStorage.getItem('disclaimerAccepted');
					if (!accepted) {
						showDisclaimer = true;
					}
				} catch (e) {
					// if sessionStorage fails, show disclaimer to be safe
					showDisclaimer = true;
				}
			}
		};

		checkAuth();

		// Listen for auth state changes
		const {
			data: { subscription }
		} = supabase!.auth.onAuthStateChange((_event, session) => {
			user = session?.user || null;
			const currentPath = window.location.pathname;

			if (!session?.user && currentPath !== '/login') {
				goto('/login');
			} else if (session?.user && currentPath === '/login') {
				goto('/');
				// Show disclaimer after successful login
				try {
					const accepted = sessionStorage.getItem('disclaimerAccepted');
					if (!accepted) {
						showDisclaimer = true;
					}
				} catch (e) {
					showDisclaimer = true;
				}
			}
		});

		return () => {
			document.removeEventListener('click', handleClickOutside);
			subscription.unsubscribe();
		};
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{#if authLoading}
	<div class="flex min-h-dvh items-center justify-center bg-base-200">
		<span class="loading loading-spinner loading-lg"></span>
	</div>
{:else}
	<div class="flex min-h-dvh flex-col bg-base-200">
		{#if user}
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

						<!-- Right: Theme Toggle + User Avatar + Mobile Menu -->
						<div class="flex items-center gap-2">
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
										<path
											d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"
										></path>
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

							<!-- User Avatar (desktop) -->
							<div class="hidden md:block">
								<UserAvatar {user} />
							</div>

							<!-- Mobile Menu Button (only on small screens) -->
							<div class="md:hidden relative mobile-menu-container">
								<button
									class="p-2 rounded-full hover:bg-base-200"
									aria-label="Open menu"
									onclick={toggleMobileMenu}
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="h-5 w-5"
										fill="none"
										viewBox="0 0 24 24"
										stroke="currentColor"
										aria-hidden="true"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M4 6h16M4 12h8m-8 6h16"
										/>
									</svg>
								</button>
								{#if mobileMenuOpen}
									<div class="absolute right-0 mt-2 w-48 bg-base-100 rounded-md shadow-lg py-1 z-10">
										<a href="/" class="block px-4 py-2 hover:bg-base-200">Home</a>
										<a href="/trades" class="block px-4 py-2 hover:bg-base-200">Trades</a>
										<div class="border-t border-base-300 my-1"></div>
										<a href="/settings" class="block px-4 py-2 hover:bg-base-200">Settings</a>
									</div>
								{/if}
							</div>
						</div>
					</div>
				</div>
			</div>
		{/if}

		<main class="container mx-auto w-full flex-1 px-4 py-6">
			{@render children?.()}
		</main>

		{#if user}
			<footer class="footer-center footer bg-base-100 p-4 text-base-content">
				<aside>
					<div class="flex items-center justify-center gap-3 text-sm opacity-80">
						<!-- Tech Icons -->
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
								class="h-5 w-auto transition-opacity hover:opacity-100"
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
								class="h-5 w-auto transition-opacity hover:opacity-100"
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
								class="h-5 w-auto transition-opacity hover:opacity-100"
							/>
						</a>

						<!-- Divider -->
						<span class="mx-1 text-xs opacity-50">|</span>

						<!-- Copyright -->
						<div class="flex items-center gap-1">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="2"
								stroke-linecap="round"
								stroke-linejoin="round"
								class="h-3.5 w-3.5"
							>
								<circle cx="12" cy="12" r="10"></circle>
								<path d="M14.83 14.83a4 4 0 1 1 0-5.66"></path>
							</svg>
							<span>2025</span>
							<a
								href="https://www.linkedin.com/in/ryan-fritts-8697b864/"
								target="_blank"
								rel="noreferrer"
								class="link link-hover"
							>
								Ryan Fritts
							</a>
						</div>

						<!-- Social Media Icons -->
						<a
							href="https://www.linkedin.com/in/ryan-fritts-8697b864/"
							target="_blank"
							rel="noreferrer"
							class="btn flex btn-circle h-5 min-h-0 w-5 items-center justify-center p-0 btn-ghost"
							aria-label="LinkedIn Profile"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 24 24"
								fill="currentColor"
								class="h-3 w-3"
							>
								<path
									d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"
								/>
							</svg>
						</a>
						<a
							href="https://x.com/restless_api"
							target="_blank"
							rel="noreferrer"
							class="btn flex btn-circle h-5 min-h-0 w-5 items-center justify-center p-0 btn-ghost"
							aria-label="X (Twitter) Profile"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 24 24"
								fill="currentColor"
								class="h-3 w-3"
							>
								<path
									d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"
								/>
							</svg>
						</a>
					</div>
				</aside>
			</footer>
		{/if}
	</div>
{/if}

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
