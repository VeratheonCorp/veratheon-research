<script lang="ts">
	import { supabase } from '$lib/supabase';
	import { AVAILABLE_MODELS, type ModelValue } from '$lib/types/auth';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import {
		User,
		Monitor,
		Database,
		Mail,
		Save,
		X,
		CircleCheckBig,
		CircleAlert
	} from '@lucide/svelte';

	type TabType = 'account' | 'model' | 'data';

	let user = $state<any>(null);
	let selectedModel = $state<ModelValue>('xai_grok_4_fast_reasoning');
	let loading = $state(true);
	let saving = $state(false);
	let successMessage = $state('');
	let errorMessage = $state('');
	let activeTab = $state<TabType>('account');

	onMount(async () => {
		// Get current user
		const {
			data: { user: currentUser }
		} = await supabase!.auth.getUser();

		if (!currentUser) {
			goto('/login');
			return;
		}

		user = currentUser;

		// Load saved model preference from localStorage
		try {
			const savedModel = localStorage.getItem('preferredModel');
			if (savedModel && AVAILABLE_MODELS.some((m) => m.value === savedModel)) {
				selectedModel = savedModel as ModelValue;
			}
		} catch (e) {
			// ignore storage errors
		}

		loading = false;
	});

	const handleSave = async () => {
		saving = true;
		successMessage = '';
		errorMessage = '';

		try {
			// Save to localStorage
			localStorage.setItem('preferredModel', selectedModel);
			successMessage = 'Settings saved successfully!';

			setTimeout(() => {
				successMessage = '';
			}, 3000);
		} catch (e) {
			errorMessage = 'Failed to save settings. Please try again.';
		} finally {
			saving = false;
		}
	};

	const handleCancel = () => {
		goto('/');
	};
</script>

<div class="min-h-screen bg-base-200 p-6">
	<div class="max-w-5xl mx-auto">
		<h1 class="text-2xl font-bold mb-6">Settings</h1>

		{#if loading}
			<div class="flex justify-center py-12">
				<span class="loading loading-spinner loading-lg"></span>
			</div>
		{:else}
			<div class="flex gap-6">
				<!-- Sidebar Navigation -->
				<div class="w-56 flex-shrink-0">
					<div class="bg-base-100 rounded-lg shadow-md p-3">
						<ul class="menu gap-1">
							<li>
								<button
									class={`font-medium ${activeTab === 'account' ? 'active bg-primary text-primary-content' : 'hover:bg-base-200'}`}
									onclick={() => (activeTab = 'account')}
								>
									<User class="h-4 w-4" />
									Account
								</button>
							</li>
							<li>
								<button
									class={`font-medium ${activeTab === 'model' ? 'active bg-primary text-primary-content' : 'hover:bg-base-200'}`}
									onclick={() => (activeTab = 'model')}
								>
									<Monitor class="h-4 w-4" />
									Model Preferences
								</button>
							</li>
							<li>
								<button
									class={`font-medium ${activeTab === 'data' ? 'active bg-primary text-primary-content' : 'hover:bg-base-200'}`}
									onclick={() => (activeTab = 'data')}
								>
									<Database class="h-4 w-4" />
									Data Controls
								</button>
							</li>
						</ul>
					</div>
				</div>

					<!-- Content Area -->
				<div class="flex-1">
					<div class="bg-base-100 rounded-lg shadow-md p-6">
						{#if successMessage}
							<div class="alert alert-success mb-4">
								<CircleCheckBig class="h-5 w-5" />
								<span>{successMessage}</span>
							</div>
						{/if}

						{#if errorMessage}
							<div class="alert alert-error mb-4">
								<CircleAlert class="h-5 w-5" />
								<span>{errorMessage}</span>
							</div>
						{/if}

						{#if activeTab === 'account'}
							<!-- Account Section -->
							<div class="space-y-4">
								<div class="flex items-center gap-2">
									<User class="h-5 w-5" />
									<h2 class="text-xl font-bold">Account</h2>
								</div>
								<p class="text-sm text-base-content/70">Manage your account information</p>
								<div class="divider my-3"></div>
								<div class="form-control">
									<label class="label">
										<span class="label-text font-medium flex items-center gap-2">
											<Mail class="h-4 w-4" />
											Email
										</span>
									</label>
									<input
										type="email"
										value={user?.email || ''}
										class="input input-bordered w-full"
										disabled
										readonly
									/>
									<label class="label">
										<span class="label-text-alt">Your email address (cannot be changed)</span>
									</label>
								</div>
							</div>
						{:else if activeTab === 'model'}
							<!-- Model Preferences Section -->
							<div class="space-y-4">
								<div class="flex items-center gap-2">
									<Monitor class="h-5 w-5" />
									<h2 class="text-xl font-bold">Model Preferences</h2>
								</div>
								<p class="text-sm text-base-content/70">Configure your AI model settings</p>
								<div class="divider my-3"></div>
								<div class="form-control">
									<label class="label">
										<span class="label-text font-medium">Preferred Inference Model</span>
									</label>
									<select class="select select-bordered w-full" bind:value={selectedModel}>
										{#each AVAILABLE_MODELS as model}
											<option value={model.value}>{model.label}</option>
										{/each}
									</select>
									<label class="label">
										<span class="label-text-alt"
											>This model will be used for generating market research reports</span
										>
									</label>
								</div>
							</div>
						{:else if activeTab === 'data'}
							<!-- Data Controls Section -->
							<div class="space-y-4">
								<div class="flex items-center gap-2">
									<Database class="h-5 w-5" />
									<h2 class="text-xl font-bold">Data Controls</h2>
								</div>
								<p class="text-sm text-base-content/70">Manage your data and privacy settings</p>
								<div class="divider my-3"></div>
								<p class="text-sm text-base-content/70">Data control settings coming soon...</p>
							</div>
						{/if}

						<!-- Action Buttons -->
						<div class="divider my-4"></div>
						<div class="flex justify-end gap-2">
							<button class="btn btn-ghost" onclick={handleCancel} disabled={saving}>
								<X class="h-4 w-4" />
								Cancel
							</button>
							<button class="btn btn-primary" onclick={handleSave} disabled={saving}>
								{#if saving}
									<span class="loading loading-spinner loading-sm"></span>
								{:else}
									<Save class="h-4 w-4" />
								{/if}
								Save Changes
							</button>
						</div>
					</div>
				</div>
			</div>
		{/if}
	</div>
</div>
