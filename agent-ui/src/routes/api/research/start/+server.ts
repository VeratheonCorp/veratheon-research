import { json } from '@sveltejs/kit';

export async function POST({ request }) {
  try {
    const { symbol, force_recompute } = await request.json();
    
    if (!symbol || typeof symbol !== 'string') {
      return json({ error: 'Invalid symbol' }, { status: 400 });
    }
    
    const symbolUpper = symbol.trim().toUpperCase();
    // In Docker Compose, the FastAPI service is named 'api' and runs on port 8085
    // When running locally, use localhost
    const apiUrl = process.env.API_URL || 
                  (process.env.NODE_ENV === 'production' ? 'http://api:8085' : 'http://localhost:8085');
    
    // Call FastAPI backend to start research job
    const response = await fetch(`${apiUrl}/research`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        symbol: symbolUpper,
        force_recompute: Boolean(force_recompute)
      })
    });
    
    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
    }
    
    const result = await response.json();
    
    return json({ 
      success: true,
      job_id: result.job_id,
      message: result.message,
      symbol: symbolUpper
    });
    
  } catch (error) {
    console.error('Start research endpoint error:', error);
    return json(
      { error: error.message || 'Failed to start research' }, 
      { status: 500 }
    );
  }
}