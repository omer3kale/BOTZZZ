// TikTok Webhook Handler - Netlify Function
exports.handler = async (event, context) => {
  console.log('TikTok webhook received:', {
    method: event.httpMethod,
    headers: event.headers,
    body: event.body
  });

  // Set CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, X-TikTok-Signature',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  try {
    // Handle GET requests (test endpoint)
    if (event.httpMethod === 'GET') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          status: 'success',
          message: 'TikTok webhook endpoint is active',
          timestamp: new Date().toISOString(),
          service: 'BOTZZZ TikTok Integration'
        })
      };
    }

    // Handle POST requests (actual webhooks)
    if (event.httpMethod === 'POST') {
      // Parse webhook data
      let webhookData = {};
      try {
        webhookData = JSON.parse(event.body || '{}');
      } catch (e) {
        console.log('Failed to parse webhook body:', e);
      }

      // Get signature for verification
      const signature = event.headers['x-tiktok-signature'] || '';
      
      console.log('Webhook data received:', webhookData);
      console.log('Signature:', signature);

      // Handle different event types
      const eventType = webhookData.type || 'unknown';
      
      let response = {
        status: 'success',
        message: 'Webhook processed successfully',
        eventType: eventType,
        timestamp: new Date().toISOString(),
        receivedData: webhookData
      };

      // Process specific event types
      if (eventType === 'authorization') {
        console.log('User authorization event:', webhookData.user_id);
        response.message = 'Authorization event processed';
      } else if (eventType === 'deauthorization') {
        console.log('User deauthorization event:', webhookData.user_id);
        response.message = 'Deauthorization event processed';
      } else {
        console.log('Unknown webhook event type:', eventType);
        response.message = `Unknown event type: ${eventType}`;
      }

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(response)
      };
    }

    // Method not allowed
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({
        error: 'Method not allowed',
        allowed: ['GET', 'POST', 'OPTIONS']
      })
    };

  } catch (error) {
    console.error('Webhook error:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Internal server error',
        message: error.message,
        timestamp: new Date().toISOString()
      })
    };
  }
};
