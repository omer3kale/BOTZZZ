// Clean TikTok Webhook Handler - UTF-8 Safe
exports.handler = async (event, context) => {
    const headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, X-TikTok-Signature',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    };

    // Handle preflight requests
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: ''
        };
    }

    // Handle GET requests
    if (event.httpMethod === 'GET') {
        const query = event.queryStringParameters || {};
        
        if (query.challenge) {
            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({ challenge: query.challenge })
            };
        }

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                service: 'BOTZZZ TikTok Webhook',
                status: 'active',
                timestamp: new Date().toISOString()
            })
        };
    }

    // Handle POST requests (webhook events)
    if (event.httpMethod === 'POST') {
        try {
            const body = JSON.parse(event.body || '{}');
            
            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    success: true,
                    message: 'Webhook received',
                    timestamp: new Date().toISOString()
                })
            };
        } catch (error) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({
                    error: 'Invalid JSON',
                    message: error.message
                })
            };
        }
    }

    return {
        statusCode: 405,
        headers,
        body: JSON.stringify({ error: 'Method not allowed' })
    };
};
