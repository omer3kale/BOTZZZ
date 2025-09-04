// Clean TikTok OAuth Callback Handler - UTF-8 Safe
exports.handler = async (event, context) => {
    const headers = {
        'Content-Type': 'text/html',
        'Access-Control-Allow-Origin': '*'
    };

    const query = event.queryStringParameters || {};
    
    if (query.code && query.state) {
        // Success page
        const html = `<!DOCTYPE html>
<html>
<head>
    <title>TikTok OAuth Success</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        .success { color: green; font-size: 24px; }
    </style>
</head>
<body>
    <div class="success">
        <h1>TikTok OAuth Success!</h1>
        <p>Authorization code received successfully.</p>
        <p>You can close this window.</p>
    </div>
    <script>
        if (window.opener) {
            window.opener.postMessage({
                type: 'TIKTOK_OAUTH_SUCCESS',
                code: '${query.code}',
                state: '${query.state}'
            }, '*');
        }
    </script>
</body>
</html>`;
        
        return {
            statusCode: 200,
            headers,
            body: html
        };
    }
    
    if (query.error) {
        // Error page
        const html = `<!DOCTYPE html>
<html>
<head>
    <title>TikTok OAuth Error</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        .error { color: red; font-size: 24px; }
    </style>
</head>
<body>
    <div class="error">
        <h1>TikTok OAuth Error</h1>
        <p>Error: ${query.error}</p>
        <p>Description: ${query.error_description || 'Unknown error'}</p>
        <p>You can close this window.</p>
    </div>
</body>
</html>`;
        
        return {
            statusCode: 400,
            headers,
            body: html
        };
    }

    // Default page for invalid requests
    const html = `<!DOCTYPE html>
<html>
<head>
    <title>TikTok OAuth Callback</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
    </style>
</head>
<body>
    <h1>TikTok OAuth Callback</h1>
    <p>Invalid OAuth request. Missing authorization code.</p>
</body>
</html>`;

    return {
        statusCode: 400,
        headers,
        body: html
    };
};
