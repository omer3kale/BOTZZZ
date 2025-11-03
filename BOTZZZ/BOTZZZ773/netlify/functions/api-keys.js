// API Keys Management - Generate, List, Delete API Keys
const { supabaseAdmin } = require('./utils/supabase');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

const JWT_SECRET = process.env.JWT_SECRET;

function getUserFromToken(authHeader) {
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return null;
  }
  const token = authHeader.substring(7);
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (error) {
    return null;
  }
}

function generateApiKey() {
  return 'sk_' + crypto.randomBytes(32).toString('hex');
}

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  const user = getUserFromToken(event.headers.authorization);
  if (!user) {
    return {
      statusCode: 401,
      headers,
      body: JSON.stringify({ error: 'Unauthorized - Please sign in to access API keys' })
    };
  }

  // Only authenticated users can access API keys
  // Regular customers get API access after login
  if (!user.userId || !user.email) {
    return {
      statusCode: 403,
      headers,
      body: JSON.stringify({ error: 'Access denied - Invalid user credentials' })
    };
  }

  try {
    const body = JSON.parse(event.body || '{}');

    switch (event.httpMethod) {
      case 'GET':
        return await handleGetKeys(user, headers);
      case 'POST':
        return await handleCreateKey(user, body, headers);
      case 'DELETE':
        return await handleDeleteKey(user, body, headers);
      default:
        return {
          statusCode: 405,
          headers,
          body: JSON.stringify({ error: 'Method not allowed' })
        };
    }
  } catch (error) {
    console.error('API Keys error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
};

async function handleGetKeys(user, headers) {
  try {
    const { data: keys, error } = await supabaseAdmin
      .from('api_keys')
      .select('*')
      .eq('user_id', user.userId)
      .eq('status', 'active')
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Get API keys error:', error);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Failed to fetch API keys' })
      };
    }

    // Mask keys in response (show first 20 chars only)
    const maskedKeys = keys.map(key => ({
      ...key,
      key: key.key.substring(0, 20) + '••••••••••••••••'
    }));

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ keys: maskedKeys })
    };
  } catch (error) {
    console.error('Get API keys error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
}

async function handleCreateKey(user, data, headers) {
  try {
    const { name, permissions } = data;

    if (!name) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'API key name is required' })
      };
    }

    // Generate new API key
    const apiKey = generateApiKey();

    const { data: key, error } = await supabaseAdmin
      .from('api_keys')
      .insert({
        user_id: user.userId,
        name,
        key: apiKey,
        permissions: permissions || ['read'],
        status: 'active',
        last_used: null
      })
      .select()
      .single();

    if (error) {
      console.error('Create API key error:', error);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Failed to create API key' })
      };
    }

    return {
      statusCode: 201,
      headers,
      body: JSON.stringify({
        success: true,
        key: key // Return full key only on creation
      })
    };
  } catch (error) {
    console.error('Create API key error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
}

async function handleDeleteKey(user, data, headers) {
  try {
    const { keyId } = data;

    if (!keyId) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Key ID is required' })
      };
    }

    // Verify key belongs to user
    const { data: key } = await supabaseAdmin
      .from('api_keys')
      .select('user_id')
      .eq('id', keyId)
      .single();

    if (!key || key.user_id !== user.userId) {
      return {
        statusCode: 403,
        headers,
        body: JSON.stringify({ error: 'Forbidden' })
      };
    }

    // Soft delete (set status to inactive)
    const { error } = await supabaseAdmin
      .from('api_keys')
      .update({ status: 'inactive' })
      .eq('id', keyId);

    if (error) {
      console.error('Delete API key error:', error);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Failed to delete API key' })
      };
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ success: true })
    };
  } catch (error) {
    console.error('Delete API key error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
}
