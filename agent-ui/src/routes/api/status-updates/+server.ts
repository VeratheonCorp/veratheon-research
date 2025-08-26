import redis from 'redis';

export async function GET() {
  const redisUrl = process.env.REDIS_URL || 'redis://redis:6379/0';
  
  const readable = new ReadableStream({
    start(controller) {
      const client = redis.createClient({ url: redisUrl });
      
      async function setupRedisSubscription() {
        try {
          await client.connect();
          
          // Subscribe to the research status updates channel
          await client.subscribe('research_status_updates', (message) => {
            try {
              const data = `data: ${message}\n\n`;
              controller.enqueue(new TextEncoder().encode(data));
            } catch (err) {
              console.error('Error processing Redis message:', err);
            }
          });
          
          console.log('Connected to Redis and subscribed to research_status_updates');
        } catch (err) {
          console.error('Redis connection error:', err);
          controller.error(err);
        }
      }
      
      setupRedisSubscription();
      
      // Handle client disconnect
      return () => {
        client.disconnect().catch(console.error);
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