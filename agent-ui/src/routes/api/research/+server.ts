import { json } from '@sveltejs/kit';

// Long timeout wrapper for research operations
async function longTimeoutFetch(url: string, options: RequestInit) {
  // Use a very long timeout since research can take 30+ minutes
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 60 * 60 * 1000); // 1 hour
  
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    throw error;
  }
}

export async function POST({ request }) {
  try {
    const { symbol, force_recompute } = await request.json();
    
    if (!symbol || typeof symbol !== 'string') {
      return json({ error: 'Invalid symbol' }, { status: 400 });
    }
    
    // Call the FastAPI backend research endpoint
    const apiUrl = process.env.API_URL || 'http://localhost:8085';
    
    const response = await longTimeoutFetch(
      `${apiUrl}/research`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          symbol: symbol.trim().toUpperCase(),
          force_recompute: Boolean(force_recompute)
        })
      }
    );
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Research API failed: ${response.status} ${errorText}`);
    }
    
    const result = await response.json();
    return json(result);
    
  } catch (error) {
    console.error('Research endpoint error:', error);
    return json(
      { error: error.message || 'Research failed' }, 
      { status: 500 }
    );
  }
}