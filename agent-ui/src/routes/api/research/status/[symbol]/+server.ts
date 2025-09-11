import { json } from '@sveltejs/kit';

export async function GET({ params, url }) {
  try {
    const { symbol } = params;
    
    if (!symbol || typeof symbol !== 'string') {
      return json({ error: 'Invalid symbol' }, { status: 400 });
    }
    
    const apiUrl = process.env.API_URL || 'http://localhost:8085';
    const job_id = url.searchParams.get('job_id');
    
    try {
      let response;
      
      if (job_id) {
        // Check specific job status by job ID
        response = await fetch(`${apiUrl}/jobs/${job_id}`, {
          method: 'GET'
        });
      } else {
        // Check most recent job for symbol
        response = await fetch(`${apiUrl}/jobs/symbol/${symbol.trim().toUpperCase()}`, {
          method: 'GET'
        });
      }
      
      if (response.ok) {
        const result = await response.json();
        
        // Transform to match expected UI format
        return json({
          job_id: result.job_id,
          symbol: result.symbol,
          status: result.status,
          completed: result.status === 'completed',
          result: result.result,
          error: result.error,
          steps: result.steps,
          created_at: result.created_at,
          updated_at: result.updated_at
        });
      } else if (response.status === 404) {
        // Job not found
        return json({ 
          completed: false, 
          message: 'No research job found',
          symbol: symbol.trim().toUpperCase()
        });
      } else {
        throw new Error(`Backend returned ${response.status}`);
      }
    } catch (fetchError) {
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