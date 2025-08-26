import redis from 'redis';

export async function GET() {
  const redisUrl = process.env.REDIS_URL || 'redis://localhost:6379/0';
  
  const readable = new ReadableStream({
    start(controller) {
      const client = redis.createClient({ url: redisUrl });
      let isConnected = false;
      
      async function setupRedisSubscription() {
        try {
          await client.connect();
          isConnected = true;
          
          // Subscribe to the research status updates channel
          await client.subscribe('research_status_updates', (message) => {
            try {
              // Check if controller is still open before sending
              if (controller.desiredSize !== null) {
                const data = `data: ${message}\n\n`;
                controller.enqueue(new TextEncoder().encode(data));
              }
            } catch (err) {
              console.error('Error processing Redis message:', err);
            }
          });
          
          console.log('Connected to Redis and subscribed to research_status_updates');
        } catch (err) {
          console.error('Redis connection error:', err);
          if (controller.desiredSize !== null) {
            controller.error(err);
          }
        }
      }
      
      setupRedisSubscription();
      
      // Handle client disconnect
      return async () => {
        try {
          if (isConnected) {
            await client.unsubscribe('research_status_updates');
            await client.disconnect();
          }
        } catch (err) {
          console.error('Error during cleanup:', err);
        }
      };
    }
  });
  
  return new Response(readable, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Cache-Control'
    }
  });
}