import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const API_URL = process.env.API_URL || 'http://localhost:8085';

export const GET: RequestHandler = async ({ url }) => {
  const query = url.searchParams.get('query');
  
  if (!query) {
    return json({ error: 'Query parameter is required' }, { status: 400 });
  }
  
  try {
    const response = await fetch(`${API_URL}/ticker-search?query=${encodeURIComponent(query)}`);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('Error from API:', errorText);
      return json({ error: 'Failed to fetch ticker search results' }, { status: response.status });
    }
    
    const data = await response.json();
    return json(data);
  } catch (error) {
    console.error('Error in ticker search:', error);
    return json({ error: 'Failed to search for tickers' }, { status: 500 });
  }
};
