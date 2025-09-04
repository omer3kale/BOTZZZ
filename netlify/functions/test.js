// Simple test function for Netlify
exports.handler = async (event, context) => {
    return {
        statusCode: 200,
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
            message: 'BOTZZZ TikTok Test Function Working!',
            timestamp: new Date().toISOString(),
            path: event.path,
            method: event.httpMethod
        })
    };
};
