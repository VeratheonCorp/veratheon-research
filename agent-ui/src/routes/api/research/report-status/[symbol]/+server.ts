import { json } from '@sveltejs/kit';

export async function GET({ params }) {
  try {
    const { symbol } = params;
    
    if (!symbol || typeof symbol !== 'string') {
      return json({ error: 'Invalid symbol' }, { status: 400 });
    }
    
    // In Docker Compose, the FastAPI service is named 'api' and runs on port 8085
    // When running locally, use localhost
    const apiUrl = process.env.API_URL || 
                  (process.env.NODE_ENV === 'production' ? 'http://api:8085' : 'http://localhost:8085');
    
    // Call FastAPI backend to check report status
    const response = await fetch(`${apiUrl}/report-status/${symbol.trim().toUpperCase()}`, {
      method: 'GET'
    });
    
    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
    }
    
    const result = await response.json();
    
    return json(result);
    
  } catch (error) {
    console.error('Report status check error:', error);
    return json(
      { error: error.message || 'Failed to check report status' }, 
      { status: 500 }
    );
  }
}
