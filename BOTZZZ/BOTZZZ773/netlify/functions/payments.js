// Payments API - Process Payments, Add Balance
const { supabase, supabaseAdmin } = require('./utils/supabase');
const jwt = require('jsonwebtoken');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

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
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
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
      body: JSON.stringify({ 
        error: 'Unauthorized - You must be signed in to add funds. Please sign in or create an account.' 
      })
    };
  }

  // Verify user has valid userId and email
  if (!user.userId || !user.email) {
    return {
      statusCode: 403,
      headers,
      body: JSON.stringify({ 
        error: 'Access denied - Invalid user credentials. Please sign in again.' 
      })
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
      default:
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ error: 'Invalid action' })
        };
    }
  } catch (error) {
    console.error('Payments API error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
};

async function handleCreateCheckout(user, data, headers) {
  try {
    const { amount, method } = data;

    if (!amount || amount < 1) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Invalid amount' })
      };
    }

    if (method === 'stripe') {
      // Create Stripe checkout session
      const session = await stripe.checkout.sessions.create({
        payment_method_types: ['card'],
        line_items: [
          {
            price_data: {
              currency: 'usd',
              product_data: {
                name: 'Account Balance',
                description: `Add $${amount} to your account`
              },
              unit_amount: Math.round(amount * 100) // Convert to cents
            },
            quantity: 1
          }
        ],
        mode: 'payment',
        success_url: `${process.env.SITE_URL}/dashboard?payment=success`,
        cancel_url: `${process.env.SITE_URL}/dashboard?payment=cancelled`,
        client_reference_id: user.userId,
        metadata: {
          userId: user.userId,
          amount: amount.toString()
        }
      });

      // Create payment record
      await supabaseAdmin
        .from('payments')
        .insert({
          user_id: user.userId,
          amount: amount,
          method: 'stripe',
          status: 'pending',
          transaction_id: session.id
        });

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          checkoutUrl: session.url
        })
      };
    } else if (method === 'paypal') {
      // TODO: Implement PayPal checkout
      return {
        statusCode: 501,
        headers,
        body: JSON.stringify({ error: 'PayPal integration coming soon' })
      };
    } else {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Invalid payment method' })
      };
    }
  } catch (error) {
    console.error('Create checkout error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Failed to create checkout session' })
    };
  }
}

async function handleWebhook(event, headers) {
  try {
    const sig = event.headers['stripe-signature'];
    let stripeEvent;

    try {
      stripeEvent = stripe.webhooks.constructEvent(
        event.body,
        sig,
        process.env.STRIPE_WEBHOOK_SECRET
      );
    } catch (err) {
      console.error('Webhook signature verification failed:', err);
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Invalid signature' })
      };
    }

    // Handle the event
    if (stripeEvent.type === 'checkout.session.completed') {
      const session = stripeEvent.data.object;
      
      // Update payment record
      const { data: payment } = await supabaseAdmin
        .from('payments')
        .update({ status: 'completed' })
        .eq('transaction_id', session.id)
        .select()
        .single();

      if (payment) {
        // Add balance to user
        const { data: userData } = await supabaseAdmin
          .from('users')
          .select('balance')
          .eq('id', payment.user_id)
          .single();

        await supabaseAdmin
          .from('users')
          .update({ 
            balance: (parseFloat(userData.balance) + parseFloat(payment.amount)).toFixed(2)
          })
          .eq('id', payment.user_id);

        // Log activity
        await supabaseAdmin
          .from('activity_logs')
          .insert({
            user_id: payment.user_id,
            action: 'payment_completed',
            details: {
              amount: payment.amount,
              method: payment.method,
              transaction_id: payment.transaction_id
            }
          });
      }
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ received: true })
    };
  } catch (error) {
    console.error('Webhook error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Webhook processing failed' })
    };
  }
}

async function handleGetHistory(user, headers) {
  try {
    let query = supabaseAdmin
      .from('payments')
      .select('*')
      .order('created_at', { ascending: false });

    // Non-admins can only see their own payments
    if (user.role !== 'admin') {
      query = query.eq('user_id', user.userId);
    }

    const { data: payments, error } = await query;

    if (error) {
      console.error('Get payment history error:', error);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Failed to fetch payment history' })
      };
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ payments })
    };
  } catch (error) {
    console.error('Get payment history error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
}
