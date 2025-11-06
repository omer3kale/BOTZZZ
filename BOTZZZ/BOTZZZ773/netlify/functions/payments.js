// Payments API - Process Payments, Add Balance
const { supabase, supabaseAdmin } = require('./utils/supabase');
const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET;
const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET;

// Validate required environment variables
const requiredEnvVars = ['JWT_SECRET', 'SUPABASE_URL', 'SUPABASE_SERVICE_KEY'];
requiredEnvVars.forEach(varName => {
  if (!process.env[varName]) {
    console.error(`❌ Missing required environment variable: ${varName}`);
  }
});

function getStripeClient() {
  const key = (STRIPE_SECRET_KEY || '').trim();
  if (!key || key === 'undefined' || key === 'null' || key === '') {
    return null;
  }

  try {
    const stripe = require('stripe');
    return stripe(key);
  } catch (error) {
    console.error('Failed to initialize Stripe:', error.message);
    return null;
  }
}

function getUserFromToken(authHeader) {
  if (!authHeader || !authHeader.startsWith('Bearer ')) return null;
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
    'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  const authHeader = event.headers.authorization || event.headers.Authorization;
  const user = getUserFromToken(authHeader);
  if (!user) {
    return {
      statusCode: 401,
      headers,
      body: JSON.stringify({ error: 'Unauthorized - Please sign in.' })
    };
  }

  if (!user.userId || !user.email) {
    return {
      statusCode: 403,
      headers,
      body: JSON.stringify({ error: 'Access denied - Invalid user credentials.' })
    };
  }

  try {
    const body = JSON.parse(event.body || '{}');
    const { action } = body;

    switch (action) {
      case 'create-checkout':
        return await handleCreateCheckout(user, body, headers);
      case 'webhook':
        return await handleWebhook(event, headers);
      case 'history':
        return await handleGetHistory(user, headers);
      case 'export':
        if (user.role !== 'admin') {
          return { statusCode: 403, headers, body: JSON.stringify({ error: 'Admin access required' }) };
        }
        return await handleExportPayments(body, headers);
      case 'admin-add-payment':
        if (user.role !== 'admin') {
          return { statusCode: 403, headers, body: JSON.stringify({ error: 'Admin access required' }) };
        }
        return await handleAdminAddPayment(user, body, headers);
      case 'admin-modify-balance':
        if (user.role !== 'admin') {
          return { statusCode: 403, headers, body: JSON.stringify({ error: 'Admin access required' }) };
        }
        return await handleAdminModifyBalance(user, body, headers);
      default:
        return { statusCode: 400, headers, body: JSON.stringify({ error: 'Invalid action' }) };
    }
  } catch (error) {
    console.error('Payments API error:', error);
    return { statusCode: 500, headers, body: JSON.stringify({ error: 'Internal server error' }) };
  }
};

// --- (senin diğer fonksiyonların olduğu kısım değişmeden duruyor) ---

// ⚡️ Yeni eklenen fonksiyon
async function handleAdminModifyBalance(adminUser, data, headers) {
  try {
    const { userId, amount, memo } = data;

    if (!userId || typeof amount !== 'number') {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'userId and numeric amount are required.' })
      };
    }

    // Kullanıcıyı getir
    const { data: targetUser, error: userError } = await supabaseAdmin
      .from('users')
      .select('id, username, balance')
      .eq('id', userId)
      .single();

    if (userError || !targetUser) {
      return {
        statusCode: 404,
        headers,
        body: JSON.stringify({ error: 'Target user not found.' })
      };
    }

    const oldBalance = parseFloat(targetUser.balance) || 0;
    const newBalance = oldBalance + amount; // amount negatifse azalır

    if (newBalance < 0) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Balance cannot go below zero.' })
      };
    }

    // Güncelle
    const { error: updateError } = await supabaseAdmin
      .from('users')
      .update({
        balance: newBalance.toFixed(2),
        updated_at: new Date().toISOString()
      })
      .eq('id', userId);

    if (updateError) {
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Failed to update balance.' })
      };
    }

    // Log kaydı oluştur
    await supabaseAdmin.from('activity_logs').insert({
      user_id: userId,
      action: 'balance_adjusted',
      details: {
        change: amount,
        old_balance: oldBalance,
        new_balance: newBalance,
        admin_id: adminUser.userId,
        memo: memo || null
      }
    });

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: `User balance updated from $${oldBalance.toFixed(2)} to $${newBalance.toFixed(2)}`,
        newBalance: newBalance.toFixed(2)
      })
    };
  } catch (error) {
    console.error('Admin modify balance error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error while modifying balance.' })
    };
  }
}
