<script lang="ts">
	import { supabase } from '$lib/supabase';
	import { goto } from '$app/navigation';

	let mode: 'signin' | 'signup' = $state('signin');
	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let loading = $state(false);
	let error = $state('');

	const handleSignIn = async () => {
		if (!email || !password) {
			error = 'Please fill in all fields';
			return;
		}

		loading = true;
		error = '';

		const { error: signInError } = await supabase!.auth.signInWithPassword({
			email,
			password
		});

		loading = false;

		if (signInError) {
			error = signInError.message;
		} else {
			goto('/');
		}
	};

	const handleSignUp = async () => {
		if (!email || !password || !confirmPassword) {
			error = 'Please fill in all fields';
			return;
		}

		if (password !== confirmPassword) {
			error = 'Passwords do not match';
			return;
		}

		if (password.length < 6) {
			error = 'Password must be at least 6 characters';
			return;
		}

		loading = true;
		error = '';

		const { error: signUpError } = await supabase!.auth.signUp({
			email,
			password
		});

		loading = false;

		if (signUpError) {
			error = signUpError.message;
		} else {
			// After signup, sign in automatically
			handleSignIn();
		}
	};

	const handleSubmit = (e: Event) => {
		e.preventDefault();
		if (mode === 'signin') {
			handleSignIn();
		} else {
			handleSignUp();
		}
	};

	const toggleMode = () => {
		mode = mode === 'signin' ? 'signup' : 'signin';
		error = '';
		password = '';
		confirmPassword = '';
	};

	const handleGitHubLogin = async () => {
		loading = true;
		error = '';

		const { error: oauthError } = await supabase!.auth.signInWithOAuth({
			provider: 'github',
			options: {
				redirectTo: `${window.location.origin}/`
			}
		});

		loading = false;

		if (oauthError) {
			error = oauthError.message;
		}
		// Note: If successful, the user will be redirected to GitHub for authentication,
		// then to Supabase's callback URL, and finally back to our app.
		// The layout component handles the session after redirect.
	};
</script>

<div class="flex min-h-screen items-center justify-center bg-base-200 px-4">
	<div class="card w-full max-w-md bg-base-100 shadow-xl">
		<div class="card-body">
			<h2 class="card-title text-2xl font-bold justify-center mb-4">
				{mode === 'signin' ? 'Sign In' : 'Sign Up'}
			</h2>

			{#if error}
				<div class="alert alert-error mb-4">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-6 w-6 shrink-0 stroke-current"
						fill="none"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
					<span>{error}</span>
				</div>
			{/if}

			<form onsubmit={handleSubmit}>
				<div class="form-control w-full">
					<label class="label justify-start" for="email">
						<span class="label-text">Email</span>
					</label>
					<input
						id="email"
						type="email"
						placeholder="your@email.com"
						class="input input-bordered w-full"
						bind:value={email}
						disabled={loading}
						required
					/>
				</div>

				<div class="form-control w-full mt-4">
					<label class="label justify-start" for="password">
						<span class="label-text">Password</span>
					</label>
					<input
						id="password"
						type="password"
						placeholder="••••••••"
						class="input input-bordered w-full"
						bind:value={password}
						disabled={loading}
						required
					/>
				</div>

				{#if mode === 'signup'}
					<div class="form-control w-full mt-4">
						<label class="label justify-start" for="confirmPassword">
							<span class="label-text">Confirm Password</span>
						</label>
						<input
							id="confirmPassword"
							type="password"
							placeholder="••••••••"
							class="input input-bordered w-full"
							bind:value={confirmPassword}
							disabled={loading}
							required
						/>
					</div>
				{/if}

				<div class="mt-6 flex justify-end">
					<button type="submit" class="btn btn-primary" disabled={loading}>
						{#if loading}
							<span class="loading loading-spinner"></span>
						{/if}
						{mode === 'signin' ? 'Sign In' : 'Sign Up'}
					</button>
				</div>
			</form>

			<div class="divider">OR</div>

			<button class="btn btn-outline" onclick={handleGitHubLogin} disabled={loading}>
				{#if loading}
					<span class="loading loading-spinner"></span>
				{:else}
					<svg class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
						<path
							d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
						/>
					</svg>
				{/if}
				Continue with GitHub
			</button>

			<div class="text-center mt-4">
				<button type="button" class="link link-primary" onclick={toggleMode}>
					{mode === 'signin'
						? "Don't have an account? Sign up"
						: 'Already have an account? Sign in'}
				</button>
			</div>
		</div>
	</div>
</div>
