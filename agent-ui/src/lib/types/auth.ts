import type { User } from '@supabase/supabase-js';

export type { User };

export interface AuthState {
	user: User | null;
	loading: boolean;
}

export const AVAILABLE_MODELS = [
	{ value: 'local_gemma27b', label: 'Gemma 27B (Local)' },
	{ value: 'nord_gemma27b', label: 'Gemma 27B (Nord)' },
	{ value: 'local_gemma12b', label: 'Gemma 12B (Local)' },
	{ value: 'nord_gemma12b', label: 'Gemma 12B (Nord)' },
	{ value: 'local_gemma4b', label: 'Gemma 4B (Local)' },
	{ value: 'nord_gemma4b', label: 'Gemma 4B (Nord)' },
	{ value: 'local_gptoss', label: 'GPT-OSS 20B (Local)' },
	{ value: 'nord_gptoss', label: 'GPT-OSS 20B (Nord)' },
	{ value: 'xai_grok_4_fast_reasoning', label: 'XAI Grok-4 Fast Reasoning' },
	{ value: 'o4_mini', label: 'OpenAI o4-mini' }
] as const;

export type ModelValue = typeof AVAILABLE_MODELS[number]['value'];
