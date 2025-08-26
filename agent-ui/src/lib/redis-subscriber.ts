export interface StatusUpdate {
  status: string;
  timestamp?: string;
  details: {
    flow?: string;
    symbol?: string;
    duration_seconds?: number;
    [key: string]: any;
  };
}

export function createRedisSubscriber() {
  let eventSource: EventSource | null = null;
  
  function subscribe(onMessage: (data: StatusUpdate) => void, onError?: (error: Event) => void) {
    // Connect to SSE endpoint for Redis pub/sub data
    eventSource = new EventSource('/api/status-updates');
    
    eventSource.onmessage = (event) => {
      try {
        const data: StatusUpdate = JSON.parse(event.data);
        onMessage(data);
      } catch (err) {
        console.error('Failed to parse status update:', err);
      }
    };
    
    eventSource.onerror = (error) => {
      console.error('EventSource error:', error);
      if (onError) onError(error);
    };
  }
  
  function unsubscribe() {
    if (eventSource) {
      eventSource.close();
      eventSource = null;
    }
  }
  
  return { subscribe, unsubscribe };
}