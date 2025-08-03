"""
SMM Panel Web Application with PayPal Integration
Flask web app demonstrating the integration of SMM panel providers with PayPal payments
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
from datetime import datetime
import logging
from smm_panel_paypal_integration import SMMPanelManager, SMMProviderConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Load configuration
config_path = '../config/smm_panel_integration_config.json'
with open(config_path, 'r') as f:
    config = json.load(f)

# Initialize SMM Panel Manager
panel_manager = SMMPanelManager(
    paypal_client_id=os.getenv('PAYPAL_CLIENT_ID', 'demo_client_id'),
    paypal_client_secret=os.getenv('PAYPAL_CLIENT_SECRET', 'demo_client_secret'),
    sandbox=True  # Set to False for production
)

@app.route('/')
def index():
    """Homepage with service selection"""
    return render_template('index.html', 
                         providers=config['smm_panel_integration']['providers'])

@app.route('/services/<provider_name>')
def services(provider_name):
    """Display services for a specific provider"""
    if provider_name not in config['smm_panel_integration']['providers']:
        return jsonify({'error': 'Provider not found'}), 404
    
    provider_config = config['smm_panel_integration']['providers'][provider_name]
    return render_template('services.html', 
                         provider=provider_config,
                         provider_name=provider_name)

@app.route('/calculate_price', methods=['POST'])
def calculate_price():
    """Calculate price for selected service"""
    try:
        data = request.json
        provider_name = data['provider']
        service_id = int(data['service_id'])
        quantity = int(data['quantity'])
        
        # Calculate pricing
        pricing = panel_manager.calculate_pricing(provider_name, service_id, quantity)
        
        return jsonify({
            'success': True,
            'pricing': pricing
        })
        
    except Exception as e:
        logger.error(f"Price calculation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/create_order', methods=['POST'])
def create_order():
    """Create new SMM order"""
    try:
        data = request.form
        
        # Get user ID from session (in production, use proper authentication)
        user_id = session.get('user_id', 'anonymous_user')
        
        # Create order
        order_result = panel_manager.create_order(
            user_id=user_id,
            provider_name=data['provider'],
            service_id=int(data['service_id']),
            target_link=data['target_link'],
            quantity=int(data['quantity'])
        )
        
        # Store order ID in session
        session['current_order_id'] = order_result['order_id']
        
        # Redirect to PayPal for payment
        return redirect(order_result['paypal_approval_url'])
        
    except Exception as e:
        logger.error(f"Order creation error: {str(e)}")
        return render_template('error.html', error=str(e))

@app.route('/payment/success')
def payment_success():
    """Handle successful PayPal payment"""
    try:
        order_id = request.args.get('order')
        paypal_order_id = request.args.get('token')  # PayPal returns this as 'token'
        
        if not order_id or not paypal_order_id:
            return render_template('error.html', error='Missing payment parameters')
        
        # Process payment success
        result = panel_manager.process_payment_success(order_id, paypal_order_id)
        
        if result['success']:
            return render_template('payment_success.html', 
                                 order_id=order_id,
                                 result=result)
        else:
            return render_template('error.html', error=result['error'])
            
    except Exception as e:
        logger.error(f"Payment success handling error: {str(e)}")
        return render_template('error.html', error=str(e))

@app.route('/payment/cancel')
def payment_cancel():
    """Handle cancelled PayPal payment"""
    order_id = request.args.get('order')
    return render_template('payment_cancel.html', order_id=order_id)

@app.route('/order_status/<order_id>')
def order_status(order_id):
    """Check order status"""
    try:
        status = panel_manager.check_order_status(order_id)
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        logger.error(f"Order status check error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/dashboard')
def dashboard():
    """User dashboard with order history"""
    user_id = session.get('user_id', 'anonymous_user')
    orders = panel_manager.get_user_orders(user_id)
    
    return render_template('dashboard.html', 
                         orders=orders,
                         user_id=user_id)

@app.route('/api/webhook/paypal', methods=['POST'])
def paypal_webhook():
    """Handle PayPal webhooks"""
    try:
        event_data = request.json
        event_type = event_data.get('event_type')
        
        logger.info(f"Received PayPal webhook: {event_type}")
        
        # Process different webhook events
        if event_type == 'PAYMENT.CAPTURE.COMPLETED':
            # Handle successful payment capture
            payment_data = event_data['resource']
            order_id = payment_data.get('custom_id')
            
            if order_id:
                # Update order status
                logger.info(f"Payment completed for order: {order_id}")
        
        elif event_type == 'PAYMENT.CAPTURE.DENIED':
            # Handle failed payment
            payment_data = event_data['resource']
            order_id = payment_data.get('custom_id')
            
            if order_id:
                logger.warning(f"Payment denied for order: {order_id}")
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        return jsonify({'error': 'Processing failed'}), 500

@app.route('/admin/analytics')
def admin_analytics():
    """Admin analytics dashboard"""
    # Calculate basic analytics
    all_orders = []
    for order_list in panel_manager.orders.values():
        if isinstance(order_list, dict):
            all_orders.append(order_list)
    
    analytics = {
        'total_orders': len(all_orders),
        'total_revenue': sum(order.get('pricing', {}).get('total_cost', 0) for order in all_orders),
        'successful_payments': len([o for o in all_orders if o.get('payment_status') == 'completed']),
        'pending_orders': len([o for o in all_orders if o.get('status') == 'processing']),
        'average_order_value': 0
    }
    
    if analytics['total_orders'] > 0:
        analytics['average_order_value'] = analytics['total_revenue'] / analytics['total_orders']
    
    return render_template('admin_analytics.html', analytics=analytics)

# HTML Templates (in production, these should be in templates/ directory)

@app.route('/demo')
def demo():
    """Demo page with embedded forms"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SMM Panel Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .service-card { border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 8px; }
            .price-display { background: #f0f8ff; padding: 15px; border-radius: 5px; margin: 10px 0; }
            .order-form { background: #f9f9f9; padding: 20px; border-radius: 8px; }
            input, select { margin: 5px 0; padding: 8px; width: 100%; max-width: 300px; }
            button { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #005a87; }
            .error { color: red; padding: 10px; background: #ffe6e6; border-radius: 5px; }
            .success { color: green; padding: 10px; background: #e6ffe6; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>SMM Panel PayPal Integration Demo</h1>
            
            <div class="service-card">
                <h3>Instagram Followers</h3>
                <p>High-quality Instagram followers from GoUpSocial</p>
                
                <div class="order-form">
                    <form id="order-form">
                        <label>Target Instagram URL:</label><br>
                        <input type="url" id="target_link" placeholder="https://instagram.com/username" required><br>
                        
                        <label>Quantity (50-10000):</label><br>
                        <input type="number" id="quantity" min="50" max="10000" value="1000" required><br>
                        
                        <label>Provider:</label><br>
                        <select id="provider">
                            <option value="goupsocial">GoUpSocial</option>
                        </select><br>
                        
                        <input type="hidden" id="service_id" value="1">
                        
                        <button type="button" onclick="calculatePrice()">Calculate Price</button>
                    </form>
                    
                    <div id="price-display" class="price-display" style="display:none;">
                        <h4>Pricing Breakdown:</h4>
                        <p>Base Cost: $<span id="base-cost">0.00</span></p>
                        <p>PayPal Fee: $<span id="paypal-fee">0.00</span></p>
                        <p>Platform Markup: $<span id="markup">0.00</span></p>
                        <p><strong>Total Cost: $<span id="total-cost">0.00</span></strong></p>
                        
                        <button onclick="createOrder()" style="background: #ffc439; color: #000;">
                            Pay with PayPal
                        </button>
                    </div>
                    
                    <div id="message" style="margin-top: 10px;"></div>
                </div>
            </div>
            
            <div class="service-card">
                <h3>Order Status Checker</h3>
                <input type="text" id="status-order-id" placeholder="Enter Order ID">
                <button onclick="checkOrderStatus()">Check Status</button>
                <div id="status-result"></div>
            </div>
        </div>
        
        <script>
            function calculatePrice() {
                const data = {
                    provider: document.getElementById('provider').value,
                    service_id: document.getElementById('service_id').value,
                    quantity: document.getElementById('quantity').value
                };
                
                fetch('/calculate_price', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('base-cost').textContent = data.pricing.base_cost.toFixed(2);
                        document.getElementById('paypal-fee').textContent = data.pricing.paypal_fee.toFixed(2);
                        document.getElementById('markup').textContent = data.pricing.markup.toFixed(2);
                        document.getElementById('total-cost').textContent = data.pricing.total_cost.toFixed(2);
                        document.getElementById('price-display').style.display = 'block';
                        document.getElementById('message').innerHTML = '';
                    } else {
                        document.getElementById('message').innerHTML = '<div class="error">Error: ' + data.error + '</div>';
                    }
                })
                .catch(error => {
                    document.getElementById('message').innerHTML = '<div class="error">Network error: ' + error + '</div>';
                });
            }
            
            function createOrder() {
                const formData = new FormData();
                formData.append('provider', document.getElementById('provider').value);
                formData.append('service_id', document.getElementById('service_id').value);
                formData.append('target_link', document.getElementById('target_link').value);
                formData.append('quantity', document.getElementById('quantity').value);
                
                // Show loading message
                document.getElementById('message').innerHTML = '<div class="success">Creating order and redirecting to PayPal...</div>';
                
                // Submit form to create order
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '/create_order';
                
                for (let [key, value] of formData.entries()) {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = key;
                    input.value = value;
                    form.appendChild(input);
                }
                
                document.body.appendChild(form);
                form.submit();
            }
            
            function checkOrderStatus() {
                const orderId = document.getElementById('status-order-id').value;
                if (!orderId) {
                    alert('Please enter an order ID');
                    return;
                }
                
                fetch('/order_status/' + orderId)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const status = data.status;
                        document.getElementById('status-result').innerHTML = `
                            <div class="success">
                                <h4>Order Status: ${status.status}</h4>
                                <p>Payment Status: ${status.payment_status}</p>
                                <p>Total Cost: $${status.pricing.total_cost}</p>
                                <p>Created: ${new Date(status.created_at).toLocaleString()}</p>
                                ${status.provider_order_id ? '<p>Provider Order ID: ' + status.provider_order_id + '</p>' : ''}
                            </div>
                        `;
                    } else {
                        document.getElementById('status-result').innerHTML = '<div class="error">Error: ' + data.error + '</div>';
                    }
                })
                .catch(error => {
                    document.getElementById('status-result').innerHTML = '<div class="error">Network error: ' + error + '</div>';
                });
            }
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    # Set user ID in session for demo purposes
    with app.test_request_context():
        app.preprocess_request()
        
    app.run(debug=True, host='0.0.0.0', port=5000)
