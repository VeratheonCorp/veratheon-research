import type { User } from '@supabase/supabase-js';

export type { User };

export interface AuthState {
	user: User | null;
	loading: boolean;
}

export const AVAILABLE_MODELS = [
	{ value: 'xai_grok_4_fast_reasoning', label: 'XAI Grok-4 Fast Reasoning' },
	{ value: 'o4_mini', label: 'OpenAI o4-mini' }
] as const;

export type ModelValue = typeof AVAILABLE_MODELS[number]['value'];
