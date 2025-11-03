// Services API - Get, Create, Update, Delete Services
const { supabase, supabaseAdmin } = require('./utils/supabase');
const jwt = require('jsonwebtoken');
const axios = require('axios');

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

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  const user = getUserFromToken(event.headers.authorization);
  
  try {
    const body = JSON.parse(event.body || '{}');

    switch (event.httpMethod) {
      case 'GET':
        return await handleGetServices(user, headers);
      case 'POST':
        return await handleCreateService(user, body, headers);
      case 'PUT':
        return await handleUpdateService(user, body, headers);
      case 'DELETE':
        return await handleDeleteService(user, body, headers);
      default:
        return {
          statusCode: 405,
          headers,
          body: JSON.stringify({ error: 'Method not allowed' })
        };
    }
  } catch (error) {
    console.error('Services API error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
};

async function handleGetServices(user, headers) {
  try {
    // Get all active services (public endpoint)
    const { data: services, error } = await supabase
      .from('services')
      .select(`
        *,
        provider:providers(id, name, status)
      `)
      .eq('status', 'active')
      .order('category', { ascending: true })
      .order('name', { ascending: true });

    if (error) {
      console.error('Get services error:', error);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Failed to fetch services' })
      };
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ services })
    };
  } catch (error) {
    console.error('Get services error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
}

async function handleCreateService(user, data, headers) {
  try {
    // Only admins can create services
    if (!user || user.role !== 'admin') {
      return {
        statusCode: 403,
        headers,
        body: JSON.stringify({ error: 'Admin access required' })
      };
    }

    const {
      providerId,
      providerServiceId,
      name,
      category,
      description,
      price,
      minOrder,
      maxOrder,
      status
    } = data;

    if (!providerId || !providerServiceId || !name || !category || !price) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Missing required fields' })
      };
    }

    const { data: service, error } = await supabaseAdmin
      .from('services')
      .insert({
        provider_id: providerId,
        provider_service_id: providerServiceId,
        name,
        category,
        description: description || '',
        price,
        min_order: minOrder || 10,
        max_order: maxOrder || 100000,
        status: status || 'active'
      })
      .select()
      .single();

    if (error) {
      console.error('Create service error:', error);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Failed to create service' })
      };
    }

    return {
      statusCode: 201,
      headers,
      body: JSON.stringify({
        success: true,
        service
      })
    };
  } catch (error) {
    console.error('Create service error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
}

async function handleUpdateService(user, data, headers) {
  try {
    // Only admins can update services
    if (!user || user.role !== 'admin') {
      return {
        statusCode: 403,
        headers,
        body: JSON.stringify({ error: 'Admin access required' })
      };
    }

    const { serviceId, ...updateData } = data;

    if (!serviceId) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Service ID is required' })
      };
    }

    const { data: service, error } = await supabaseAdmin
      .from('services')
      .update(updateData)
      .eq('id', serviceId)
      .select()
      .single();

    if (error) {
      console.error('Update service error:', error);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Failed to update service' })
      };
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        service
      })
    };
  } catch (error) {
    console.error('Update service error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
}

async function handleDeleteService(user, data, headers) {
  try {
    // Only admins can delete services
    if (!user || user.role !== 'admin') {
      return {
        statusCode: 403,
        headers,
        body: JSON.stringify({ error: 'Admin access required' })
      };
    }

    const { serviceId } = data;

    if (!serviceId) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Service ID is required' })
      };
    }

    const { error } = await supabaseAdmin
      .from('services')
      .delete()
      .eq('id', serviceId);

    if (error) {
      console.error('Delete service error:', error);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Failed to delete service' })
      };
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ success: true })
    };
  } catch (error) {
    console.error('Delete service error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
}
