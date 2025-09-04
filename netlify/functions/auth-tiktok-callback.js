// TikTok OAuth Callback Handler for Netlify
// File: netlify/functions/auth-tiktok-callback.js

exports.handler = async (event, context) => {
    // CORS headers for cross-origin requests
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
        const { code, state, error, error_description } = event.queryStringParameters || {};

        console.log('TikTok OAuth Callback:', {
            method: event.httpMethod,
            hasCode: !!code,
            hasError: !!error,
            state,
            timestamp: new Date().toISOString()
        });

        // Handle OAuth errors
        if (error) {
            console.error('TikTok OAuth Error:', error, error_description);
            return {
                statusCode: 400,
                headers: {
                    'Content-Type': 'text/html'
                },
                body: `
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>TikTok OAuth Error - BOTZZZ</title>
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <style>
                            body { 
                                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                                margin: 0; padding: 40px 20px; background: #f5f5f5; 
                            }
                            .container { 
                                max-width: 600px; margin: 0 auto; 
                                background: white; padding: 40px; border-radius: 8px; 
                                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                            }
                            .error { color: #dc3545; }
                            .btn { 
                                background: #007bff; color: white; border: none; 
                                padding: 12px 24px; border-radius: 4px; cursor: pointer;
                                font-size: 16px; margin-top: 20px;
                            }
                            .btn:hover { background: #0056b3; }
                            h1 { color: #333; margin-bottom: 20px; }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>🚫 TikTok OAuth Error</h1>
                            <p class="error"><strong>Error:</strong> ${error}</p>
                            <p><strong>Description:</strong> ${error_description || 'Unknown error occurred'}</p>
                            <p>Please try again or contact BOTZZZ support if the issue persists.</p>
                            <button class="btn" onclick="window.close()">Close Window</button>
                            <script>
                                console.error('TikTok OAuth Error:', {
                                    error: '${error}',
                                    description: '${error_description}',
                                    timestamp: new Date().toISOString()
                                });
                            </script>
                        </div>
                    </body>
                    </html>
                `
            };
        }

        // Handle successful OAuth callback
        if (code) {
            console.log('TikTok OAuth Success:', { 
                code: code.substring(0, 10) + '...', 
                state,
                length: code.length 
            });
            
            return {
                statusCode: 200,
                headers: {
                    'Content-Type': 'text/html'
                },
                body: `
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>TikTok OAuth Success - BOTZZZ</title>
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <style>
                            body { 
                                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                                margin: 0; padding: 40px 20px; background: #f5f5f5; 
                            }
                            .container { 
                                max-width: 600px; margin: 0 auto; 
                                background: white; padding: 40px; border-radius: 8px; 
                                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                            }
                            .success { color: #28a745; }
                            .code-box { 
                                background: #f8f9fa; padding: 15px; border-radius: 4px; 
                                font-family: 'Monaco', 'Menlo', monospace; margin: 15px 0;
                                border-left: 4px solid #28a745; word-break: break-all;
                            }
                            .btn { 
                                background: #28a745; color: white; border: none; 
                                padding: 12px 24px; border-radius: 4px; cursor: pointer;
                                font-size: 16px; margin-top: 20px;
                            }
                            .btn:hover { background: #1e7e34; }
                            h1 { color: #333; margin-bottom: 20px; }
                            .auto-close { color: #6c757d; font-size: 14px; margin-top: 15px; }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1 class="success">🎉 TikTok OAuth Successful!</h1>
                            <p><strong>BOTZZZ</strong> has been authorized successfully with TikTok!</p>
                            
                            <div class="code-box">
                                <strong>Authorization Code:</strong><br>
                                ${code.substring(0, 30)}...
                            </div>
                            
                            <div class="code-box">
                                <strong>State:</strong> ${state || 'N/A'}<br>
                                <strong>Timestamp:</strong> ${new Date().toISOString()}
                            </div>
                            
                            <p>Your TikTok integration is now <strong>100% complete</strong>!</p>
                            <p class="auto-close">This window will close automatically in 5 seconds.</p>
                            
                            <button class="btn" onclick="window.close()">Close Window</button>
                            
                            <script>
                                // Log success for debugging
                                console.log('BOTZZZ TikTok OAuth Success:', {
                                    code: '${code}',
                                    state: '${state}',
                                    timestamp: new Date().toISOString(),
                                    app: 'BOTZZZ'
                                });
                                
                                // Auto-close after 5 seconds
                                setTimeout(() => {
                                    window.close();
                                }, 5000);
                                
                                // Try to communicate with parent window
                                try {
                                    if (window.opener) {
                                        window.opener.postMessage({
                                            type: 'BOTZZZ_TIKTOK_OAUTH_SUCCESS',
                                            code: '${code}',
                                            state: '${state}',
                                            timestamp: new Date().toISOString()
                                        }, '*');
                                    }
                                    
                                    // Also try parent window
                                    if (window.parent && window.parent !== window) {
                                        window.parent.postMessage({
                                            type: 'BOTZZZ_TIKTOK_OAUTH_SUCCESS',
                                            code: '${code}',
                                            state: '${state}',
                                            timestamp: new Date().toISOString()
                                        }, '*');
                                    }
                                } catch (e) {
                                    console.log('Could not communicate with parent window:', e);
                                }
                            </script>
                        </div>
                    </body>
                    </html>
                `
            };
        }

        // No code or error - invalid request
        return {
            statusCode: 400,
            headers: {
                'Content-Type': 'text/html'
            },
            body: `
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Invalid OAuth Request - BOTZZZ</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <style>
                        body { 
                            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                            margin: 0; padding: 40px 20px; background: #f5f5f5; 
                        }
                        .container { 
                            max-width: 600px; margin: 0 auto; 
                            background: white; padding: 40px; border-radius: 8px; 
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        }
                        .warning { color: #ffc107; }
                        .btn { 
                            background: #6c757d; color: white; border: none; 
                            padding: 12px 24px; border-radius: 4px; cursor: pointer;
                            font-size: 16px; margin-top: 20px;
                        }
                        h1 { color: #333; margin-bottom: 20px; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1 class="warning">⚠️ Invalid OAuth Request</h1>
                        <p>This endpoint handles TikTok OAuth callbacks for <strong>BOTZZZ</strong>.</p>
                        <p>No authorization code or error parameter was provided.</p>
                        <p>Please initiate the OAuth flow from your application.</p>
                        <button class="btn" onclick="window.close()">Close Window</button>
                    </div>
                </body>
                </html>
            `
        };

    } catch (error) {
        console.error('Netlify Function Error:', error);
        return {
            statusCode: 500,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                error: 'internal_error',
                message: 'An internal error occurred in BOTZZZ TikTok integration',
                timestamp: new Date().toISOString()
            })
        };
    }
};
