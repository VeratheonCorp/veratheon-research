import { json } from '@sveltejs/kit';

export async function POST({ request }) {
  try {
    const { symbol } = await request.json();
    
    if (!symbol || typeof symbol !== 'string') {
      return json({ error: 'Invalid symbol' }, { status: 400 });
    }
    
    // Call the FastAPI backend research endpoint
    const apiUrl = process.env.API_URL || 'http://localhost:8085';
    const response = await fetch(`${apiUrl}/research`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ symbol: symbol.trim().toUpperCase() }),
    });
    
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