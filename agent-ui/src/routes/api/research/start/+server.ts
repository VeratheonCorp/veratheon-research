import { json } from '@sveltejs/kit';

export async function POST({ request }) {
  try {
    const { symbol, force_recompute } = await request.json();
    
    if (!symbol || typeof symbol !== 'string') {
      return json({ error: 'Invalid symbol' }, { status: 400 });
    }
    
    const symbolUpper = symbol.trim().toUpperCase();
    const apiUrl = process.env.API_URL || 'http://localhost:8085';
    
    // Start research in background without waiting - use setTimeout to make it truly async
    setTimeout(() => {
      fetch(`${apiUrl}/research`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          symbol: symbolUpper,
          force_recompute: Boolean(force_recompute)
        })
      }).catch(error => {
        console.error('Background research error:', error);
      });
    }, 0);
    
    return json({ 
      success: true, 
      message: `Research started for ${symbolUpper}`,
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