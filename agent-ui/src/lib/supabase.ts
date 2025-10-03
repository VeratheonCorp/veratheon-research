/**
 * Supabase client configuration for frontend
 */

import { createClient } from '@supabase/supabase-js';
import { browser } from '$app/environment';

// Get Supabase URL and anon key from environment variables
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'http://127.0.0.1:54321';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || '';

// Create Supabase client (only in browser)
export const supabase = browser
	? createClient(supabaseUrl, supabaseAnonKey, {
			realtime: {
				params: {
					eventsPerSecond: 10
				}
			}
		})
	: null;
