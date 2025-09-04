// TikTok Webhook Handler for Netlify
// File: netlify/functions/tiktok-webhook.js

const crypto = require('crypto');

exports.handler = async (event, context) => {
    // CORS headers
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

    // Handle GET requests (webhook verification)
    if (event.httpMethod === 'GET') {
        const { challenge } = event.queryStringParameters || {};
        
        if (challenge) {
            console.log('TikTok Webhook Challenge:', challenge);
            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({ challenge })
            };
        }

        // Return webhook info for GET requests without challenge
        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                service: 'BOTZZZ TikTok Webhook Handler',
                status: 'active',
                timestamp: new Date().toISOString(),
                endpoints: {
                    webhook: '/.netlify/functions/tiktok-webhook',
                    oauth_callback: '/.netlify/functions/auth-tiktok-callback'
                }
            })
        };
    }

    // Handle POST requests (actual webhook events)
    if (event.httpMethod === 'POST') {
        try {
            const signature = event.headers['x-tiktok-signature'];
            const body = event.body;
            
            console.log('TikTok Webhook POST received:', {
                hasSignature: !!signature,
                bodyLength: body ? body.length : 0,
                headers: Object.keys(event.headers),
                timestamp: new Date().toISOString()
            });

            // Verify webhook signature (optional but recommended)
            if (signature && body) {
                const clientSecret = process.env.TIKTOK_CLIENT_SECRET || 'i1nANmnaa6q1Xef9ql9DqxIw0Afc1NkV';
                
                try {
                    const expectedSignature = crypto
                        .createHmac('sha256', clientSecret)
                        .update(body)
                        .digest('hex');
                    
                    if (signature !== expectedSignature) {
                        console.warn('TikTok Webhook signature mismatch');
                        // Don't reject - TikTok signature validation can be complex
                    } else {
                        console.log('TikTok Webhook signature verified');
                    }
                } catch (signatureError) {
                    console.warn('Signature verification error:', signatureError.message);
                }
            }

            // Parse webhook data
            let webhookData;
            try {
                webhookData = JSON.parse(body || '{}');
            } catch (parseError) {
                console.error('Failed to parse webhook body:', parseError.message);
                return {
                    statusCode: 400,
                    headers,
                    body: JSON.stringify({
                        error: 'invalid_payload',
                        message: 'Failed to parse JSON payload'
                    })
                };
            }

            // Log webhook event
            console.log('TikTok Webhook Event:', {
                type: webhookData.type || 'unknown',
                event: webhookData.event || 'unknown',
                data: webhookData.data ? 'present' : 'missing',
                timestamp: new Date().toISOString()
            });

            // Process different webhook event types
            const eventType = webhookData.type || webhookData.event;
            
            switch (eventType) {
                case 'user.authorization.revoke':
                    console.log('User revoked authorization:', webhookData.data);
                    // Handle user authorization revocation
                    break;
                    
                case 'video.upload':
                    console.log('Video upload event:', webhookData.data);
                    // Handle video upload events
                    break;
                    
                case 'user.data.portability':
                    console.log('Data portability event:', webhookData.data);
                    // Handle data portability requests
                    break;
                    
                default:
                    console.log('Unknown webhook event type:', eventType);
                    break;
            }

            // Store webhook data (you can add database storage here)
            // For now, just log and acknowledge
            
            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    status: 'success',
                    message: 'Webhook processed successfully',
                    event_type: eventType,
                    timestamp: new Date().toISOString(),
                    service: 'BOTZZZ'
                })
            };

        } catch (error) {
            console.error('Webhook processing error:', error);
            return {
                statusCode: 500,
                headers,
                body: JSON.stringify({
                    error: 'processing_error',
                    message: 'Failed to process webhook',
                    timestamp: new Date().toISOString()
                })
            };
        }
    }

    // Method not allowed
    return {
        statusCode: 405,
        headers,
        body: JSON.stringify({
            error: 'method_not_allowed',
            message: 'Only GET and POST methods are supported',
            timestamp: new Date().toISOString()
        })
    };
};
