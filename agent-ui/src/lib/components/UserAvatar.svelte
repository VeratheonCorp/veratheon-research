<script lang="ts">
	import type { User } from '$lib/types/auth';
	import { supabase } from '$lib/supabase';
	import { goto } from '$app/navigation';

	let { user }: { user: User } = $props();
	let dropdownOpen = $state(false);

	const toggleDropdown = () => {
		dropdownOpen = !dropdownOpen;
	};

	const handleSignOut = async () => {
		await supabase!.auth.signOut();
		goto('/login');
	};

	const handleSettings = () => {
		dropdownOpen = false;
		goto('/settings');
	};

	// Get user initials for avatar fallback
	const getInitials = (email: string): string => {
		return email.substring(0, 2).toUpperCase();
	};

	// Get avatar URL from user metadata (GitHub OAuth provides this)
	const getAvatarUrl = (): string | null => {
		return user.user_metadata?.avatar_url || null;
	};

	// Close dropdown when clicking outside
	const handleClickOutside = (event: MouseEvent) => {
		const target = event.target as HTMLElement;
		if (dropdownOpen && !target.closest('.user-avatar-container')) {
			dropdownOpen = false;
		}
	};

	$effect(() => {
		if (typeof document !== 'undefined') {
			document.addEventListener('click', handleClickOutside);
			return () => {
				document.removeEventListener('click', handleClickOutside);
			};
		}
	});
</script>

<div class="relative user-avatar-container">
	<button
		class="btn btn-ghost btn-circle avatar"
		aria-label="User menu"
		onclick={toggleDropdown}
	>
		<div class="w-10 rounded-full">
			{#if getAvatarUrl()}
				<img src={getAvatarUrl()} alt="User avatar" class="rounded-full" />
			{:else}
				<div class="bg-neutral text-neutral-content rounded-full w-10 h-10 flex items-center justify-center">
					<span class="text-sm">{getInitials(user.email || '')}</span>
				</div>
			{/if}
		</div>
	</button>

	{#if dropdownOpen}
		<div class="absolute right-0 mt-2 w-52 bg-base-100 rounded-md shadow-lg py-1 z-50 border border-base-300">
			<div class="px-4 py-3 border-b border-base-300">
				<div class="flex items-center gap-3">
					{#if getAvatarUrl()}
						<img src={getAvatarUrl()} alt="User avatar" class="w-10 h-10 rounded-full" />
					{:else}
						<div class="bg-neutral text-neutral-content rounded-full w-10 h-10 flex items-center justify-center">
							<span class="text-sm">{getInitials(user.email || '')}</span>
						</div>
					{/if}
					<div class="flex-1 min-w-0">
						{#if user.user_metadata?.full_name}
							<p class="text-sm font-medium truncate">{user.user_metadata.full_name}</p>
						{/if}
						<p class="text-xs text-base-content/70 truncate">{user.email}</p>
					</div>
				</div>
			</div>
			<button
				class="block w-full text-left px-4 py-2 hover:bg-base-200 text-sm"
				onclick={handleSettings}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-4 w-4 inline mr-2"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
					/>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
					/>
				</svg>
				Settings
			</button>
			<button
				class="block w-full text-left px-4 py-2 hover:bg-base-200 text-sm text-error"
				onclick={handleSignOut}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-4 w-4 inline mr-2"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
					/>
				</svg>
				Sign Out
			</button>
		</div>
	{/if}
</div>
