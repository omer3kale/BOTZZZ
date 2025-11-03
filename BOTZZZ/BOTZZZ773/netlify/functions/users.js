// Users API - Get, Update, Delete User Data
const { supabase, supabaseAdmin } = require('./utils/supabase');
const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET;

// Helper to verify token and get user
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

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, PUT, DELETE, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle OPTIONS request
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  // Verify authentication
  const user = getUserFromToken(event.headers.authorization);
  if (!user) {
    return {
      statusCode: 401,
      headers,
      body: JSON.stringify({ error: 'Unauthorized' })
    };
  }

  try {
    const { action, userId, ...data } = JSON.parse(event.body || '{}');

    // Admin-only actions
    const adminActions = ['list', 'create', 'update-any', 'delete'];
    if (adminActions.includes(action) && user.role !== 'admin') {
      return {
        statusCode: 403,
        headers,
        body: JSON.stringify({ error: 'Admin access required' })
      };
    }

    switch (event.httpMethod) {
      case 'GET':
        return await handleGet(user, headers);
      case 'PUT':
        return await handleUpdate(user, data, headers);
      case 'DELETE':
        return await handleDelete(user, userId, headers);
      default:
        return {
          statusCode: 405,
          headers,
          body: JSON.stringify({ error: 'Method not allowed' })
        };
    }
  } catch (error) {
    console.error('Users API error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
};

async function handleGet(user, headers) {
  try {
    // Admin can get all users
    if (user.role === 'admin') {
      const { data: users, error } = await supabaseAdmin
        .from('users')
        .select('*')
        .order('created_at', { ascending: false });

      if (error) {
        return {
          statusCode: 500,
          headers,
          body: JSON.stringify({ error: 'Failed to fetch users' })
        };
      }

      // Remove password hashes
      users.forEach(u => delete u.password_hash);

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ users })
      };
    }

    // Regular users get their own data
    const { data: userData, error } = await supabase
      .from('users')
      .select('*')
      .eq('id', user.userId)
      .single();

    if (error) {
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Failed to fetch user data' })
      };
    }

    delete userData.password_hash;

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ user: userData })
    };
  } catch (error) {
    console.error('Get users error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
}

async function handleUpdate(user, data, headers) {
  try {
    const targetUserId = data.userId || user.userId;

    // Users can only update their own data unless admin
    if (targetUserId !== user.userId && user.role !== 'admin') {
      return {
        statusCode: 403,
        headers,
        body: JSON.stringify({ error: 'Forbidden' })
      };
    }

    // Don't allow users to change their own role
    if (data.role && targetUserId === user.userId && user.role !== 'admin') {
      delete data.role;
    }

    // Remove sensitive fields
    delete data.password_hash;
    delete data.userId;

    const { data: updatedUser, error } = await supabaseAdmin
      .from('users')
      .update(data)
      .eq('id', targetUserId)
      .select()
      .single();

    if (error) {
      console.error('Update user error:', error);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Failed to update user' })
      };
    }

    delete updatedUser.password_hash;

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        user: updatedUser
      })
    };
  } catch (error) {
    console.error('Update user error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
}

async function handleDelete(user, targetUserId, headers) {
  try {
    // Only admins can delete users
    if (user.role !== 'admin') {
      return {
        statusCode: 403,
        headers,
        body: JSON.stringify({ error: 'Admin access required' })
      };
    }

    // Can't delete yourself
    if (targetUserId === user.userId) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Cannot delete your own account' })
      };
    }

    const { error } = await supabaseAdmin
      .from('users')
      .delete()
      .eq('id', targetUserId);

    if (error) {
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Failed to delete user' })
      };
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ success: true })
    };
  } catch (error) {
    console.error('Delete user error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
}
