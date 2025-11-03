// Payment Integration with Backend
// Load this AFTER api-client.js

document.addEventListener('DOMContentLoaded', () => {
    setupPaymentButtons();
    loadPaymentHistory();
});

// Setup payment buttons
function setupPaymentButtons() {
    // Payeer payment
    const payeerBtn = document.getElementById('payeerPaymentBtn');
    if (payeerBtn) {
        payeerBtn.addEventListener('click', handlePayeerPayment);
    }

    // Stripe payment
    const stripeBtn = document.getElementById('stripePaymentBtn');
    if (stripeBtn) {
        stripeBtn.addEventListener('click', handleStripePayment);
    }

    // Amount selection
    document.querySelectorAll('.amount-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const amount = parseFloat(btn.dataset.amount);
            document.getElementById('customAmount').value = amount;
            updatePaymentSummary(amount);
        });
    });

    // Custom amount
    const customAmountInput = document.getElementById('customAmount');
    if (customAmountInput) {
        customAmountInput.addEventListener('input', (e) => {
            const amount = parseFloat(e.target.value) || 0;
            updatePaymentSummary(amount);
        });
    }
}

// Handle Payeer payment
async function handlePayeerPayment() {
    const amount = parseFloat(document.getElementById('customAmount')?.value);
    
    if (!amount || amount < 5) {
        showNotification('Minimum payment amount is $5', 'error');
        return;
    }

    if (!isLoggedIn()) {
        showNotification('Please login to add funds', 'error');
        setTimeout(() => {
            window.location.href = 'signin.html';
        }, 2000);
        return;
    }

    const btn = document.getElementById('payeerPaymentBtn');
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Processing...';

    try {
        const data = await api.createPayment(amount, 'payeer');
        
        if (data.success && data.paymentUrl) {
            showNotification('Redirecting to Payeer...', 'success');
            // Redirect to Payeer payment page
            window.location.href = data.paymentUrl;
        } else {
            showNotification(data.error || 'Payment initiation failed', 'error');
            btn.disabled = false;
            btn.textContent = originalText;
        }
    } catch (error) {
        console.error('Payeer payment error:', error);
        showNotification(error.message || 'Payment failed. Please try again.', 'error');
        btn.disabled = false;
        btn.textContent = originalText;
    }
}

// Handle Stripe payment
async function handleStripePayment() {
    const amount = parseFloat(document.getElementById('customAmount')?.value);
    
    if (!amount || amount < 5) {
        showNotification('Minimum payment amount is $5', 'error');
        return;
    }

    if (!isLoggedIn()) {
        showNotification('Please login to add funds', 'error');
        setTimeout(() => {
            window.location.href = 'signin.html';
        }, 2000);
        return;
    }

    const btn = document.getElementById('stripePaymentBtn');
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Processing...';

    try {
        const data = await api.createPayment(amount, 'stripe');
        
        if (data.success && data.checkoutUrl) {
            showNotification('Redirecting to Stripe...', 'success');
            // Redirect to Stripe checkout
            window.location.href = data.checkoutUrl;
        } else {
            showNotification(data.error || 'Payment initiation failed', 'error');
            btn.disabled = false;
            btn.textContent = originalText;
        }
    } catch (error) {
        console.error('Stripe payment error:', error);
        showNotification(error.message || 'Payment failed. Please try again.', 'error');
        btn.disabled = false;
        btn.textContent = originalText;
    }
}

// Update payment summary
function updatePaymentSummary(amount) {
    const fee = amount * 0.025; // 2.5% fee
    const total = amount + fee;

    document.getElementById('subtotal').textContent = `$${amount.toFixed(2)}`;
    document.getElementById('fee').textContent = `$${fee.toFixed(2)}`;
    document.getElementById('total').textContent = `$${total.toFixed(2)}`;
}

// Load payment history
async function loadPaymentHistory() {
    const historyContainer = document.getElementById('paymentHistory');
    if (!historyContainer) return;

    try {
        const data = await api.getPaymentHistory();
        
        if (data.payments && data.payments.length > 0) {
            renderPaymentHistory(data.payments);
        } else {
            historyContainer.innerHTML = '<p class="text-center text-gray-500">No payment history found</p>';
        }
    } catch (error) {
        console.error('Failed to load payment history:', error);
        historyContainer.innerHTML = '<p class="text-center text-red-500">Failed to load payment history</p>';
    }
}

// Render payment history
function renderPaymentHistory(payments) {
    const historyContainer = document.getElementById('paymentHistory');
    
    const html = `
        <table class="payment-table">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Amount</th>
                    <th>Method</th>
                    <th>Status</th>
                    <th>Transaction ID</th>
                </tr>
            </thead>
            <tbody>
                ${payments.map(payment => `
                    <tr>
                        <td>${formatDate(payment.created_at)}</td>
                        <td>$${parseFloat(payment.amount).toFixed(2)}</td>
                        <td>${capitalizeFirst(payment.method)}</td>
                        <td>
                            <span class="status-badge status-${payment.status}">
                                ${capitalizeFirst(payment.status)}
                            </span>
                        </td>
                        <td class="transaction-id">${payment.transaction_id}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    historyContainer.innerHTML = html;
}

// Helper functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 9999;
        animation: slideIn 0.3s ease;
        max-width: 400px;
    `;

    if (type === 'success') {
        notification.style.background = '#10b981';
    } else if (type === 'error') {
        notification.style.background = '#ef4444';
    }

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}
