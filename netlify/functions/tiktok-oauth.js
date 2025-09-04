// TikTok OAuth Callback Handler - Netlify Function
exports.handler = async (event, context) => {
  console.log('TikTok OAuth callback received:', {
    method: event.httpMethod,
    queryParams: event.queryStringParameters,
    headers: event.headers
  });

  // Set CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
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
    // Get OAuth parameters from query string
    const params = event.queryStringParameters || {};
    const {
      code,
      state,
      error,
      error_description,
      scopes
    } = params;

    console.log('OAuth parameters:', { code, state, error, error_description, scopes });

    // Handle OAuth errors
    if (error) {
      console.error('OAuth error received:', error, error_description);
      
      return {
        statusCode: 400,
        headers: {
          ...headers,
          'Content-Type': 'text/html'
        },
        body: `
          <!DOCTYPE html>
          <html>
          <head>
            <title>OAuth Error - BOTZZZ</title>
            <style>
              body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
              .error { background: #fee; border: 1px solid #fcc; padding: 20px; border-radius: 5px; }
              .error h2 { color: #c00; margin-top: 0; }
            </style>
          </head>
          <body>
            <div class="error">
              <h2>🚫 OAuth Error</h2>
              <p><strong>Error:</strong> ${error}</p>
              <p><strong>Description:</strong> ${error_description || 'No description provided'}</p>
              <p><strong>State:</strong> ${state || 'No state provided'}</p>
              <p><a href="javascript:window.close()">Close Window</a></p>
            </div>
          </body>
          </html>
        `
      };
    }

    // Handle successful authorization
    if (code) {
      console.log('OAuth success - Authorization code received:', code);
      
      // In a real app, you would exchange this code for an access token
      // For now, just display success message
      
      return {
        statusCode: 200,
        headers: {
          ...headers,
          'Content-Type': 'text/html'
        },
        body: `
          <!DOCTYPE html>
          <html>
          <head>
            <title>OAuth Success - BOTZZZ</title>
            <style>
              body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
              .success { background: #efe; border: 1px solid #cfc; padding: 20px; border-radius: 5px; }
              .success h2 { color: #060; margin-top: 0; }
              .code { background: #f5f5f5; padding: 10px; border-radius: 3px; font-family: monospace; word-break: break-all; }
              .details { margin: 20px 0; }
              .details dt { font-weight: bold; }
              .details dd { margin-bottom: 10px; }
            </style>
          </head>
          <body>
            <div class="success">
              <h2>✅ OAuth Authorization Successful!</h2>
              <p>BOTZZZ has been successfully authorized to access your TikTok account.</p>
              
              <div class="details">
                <dl>
                  <dt>Authorization Code:</dt>
                  <dd class="code">${code}</dd>
                  
                  <dt>State:</dt>
                  <dd>${state || 'No state provided'}</dd>
                  
                  <dt>Scopes:</dt>
                  <dd>${scopes || 'Default scopes'}</dd>
                  
                  <dt>Timestamp:</dt>
                  <dd>${new Date().toISOString()}</dd>
                </dl>
              </div>
              
              <p><strong>Next Steps:</strong></p>
              <ul>
                <li>This authorization code will be exchanged for an access token</li>
                <li>BOTZZZ can now access your TikTok data according to the granted permissions</li>
                <li>You can close this window</li>
              </ul>
              
              <p><a href="javascript:window.close()">Close Window</a></p>
            </div>
            
            <script>
              console.log('OAuth callback successful:', {
                code: '${code}',
                state: '${state}',
                scopes: '${scopes}',
                timestamp: '${new Date().toISOString()}'
              });
              
              // Auto-close after 5 seconds
              setTimeout(() => {
                window.close();
              }, 5000);
            </script>
          </body>
          </html>
        `
      };
    }

    // No code or error - invalid request
    return {
      statusCode: 400,
      headers: {
        ...headers,
        'Content-Type': 'text/html'
      },
      body: `
        <!DOCTYPE html>
        <html>
        <head>
          <title>Invalid OAuth Request - BOTZZZ</title>
          <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
            .warning { background: #fff8dc; border: 1px solid #f0e68c; padding: 20px; border-radius: 5px; }
            .warning h2 { color: #b8860b; margin-top: 0; }
          </style>
        </head>
        <body>
          <div class="warning">
            <h2>⚠️ Invalid OAuth Request</h2>
            <p>This OAuth callback was called without a valid authorization code or error.</p>
            <p><strong>Received parameters:</strong></p>
            <pre>${JSON.stringify(params, null, 2)}</pre>
            <p><a href="javascript:window.close()">Close Window</a></p>
          </div>
        </body>
        </html>
      `
    };

  } catch (error) {
    console.error('OAuth callback error:', error);
    
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
