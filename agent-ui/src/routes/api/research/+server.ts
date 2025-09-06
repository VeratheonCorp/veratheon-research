import { json } from '@sveltejs/kit';

// Custom fetch wrapper with extended timeouts for long-running operations
async function fetchWithTimeout(url: string, options: RequestInit, timeoutMs: number) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
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
    const { symbol } = await request.json();
    
    if (!symbol || typeof symbol !== 'string') {
      return json({ error: 'Invalid symbol' }, { status: 400 });
    }
    
    // Call the FastAPI backend research endpoint
    const apiUrl = process.env.API_URL || 'http://localhost:8085';
    
    const response = await fetchWithTimeout(
      `${apiUrl}/research`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symbol: symbol.trim().toUpperCase() }),
      },
      5 * 60 * 1000 // 5 minutes timeout
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