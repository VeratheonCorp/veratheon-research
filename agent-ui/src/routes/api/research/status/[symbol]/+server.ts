import { json } from '@sveltejs/kit';

export async function GET({ params }) {
  try {
    const { symbol } = params;
    
    if (!symbol || typeof symbol !== 'string') {
      return json({ error: 'Invalid symbol' }, { status: 400 });
    }
    
    // Check with FastAPI backend for research status
    const apiUrl = process.env.API_URL || 'http://localhost:8085';
    
    try {
      const response = await fetch(`${apiUrl}/research/status/${symbol.trim().toUpperCase()}`, {
        method: 'GET'
      });
      
      if (response.ok) {
        const result = await response.json();
        return json(result);
      } else if (response.status === 404) {
        // Research not found or not started yet
        return json({ 
          completed: false, 
          message: 'Research not found or still starting',
          symbol: symbol.trim().toUpperCase()
        });
      } else {
        throw new Error(`Backend returned ${response.status}`);
      }
    } catch (fetchError) {
      // If backend is unreachable or returns error, assume research is still running
      console.error('Status check error:', fetchError);
      return json({ 
        completed: false, 
        message: 'Research in progress or backend unavailable',
        symbol: symbol.trim().toUpperCase()
      });
    }
    
  } catch (error) {
    console.error('Status endpoint error:', error);
    return json(
      { error: error.message || 'Failed to check research status' }, 
      { status: 500 }
    );
  }
}