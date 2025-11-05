// Admin Payments Management with Real Modals

// Modal Helper Functions
function createModal(title, content, actions = '') {
    const modalHTML = `
        <div class="modal-overlay" id="activeModal" onclick="if(event.target === this) closeModal()">
            <div class="modal-content" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                <div class="modal-body">
                    ${content}
                </div>
                ${actions ? `<div class="modal-footer">${actions}</div>` : ''}
            </div>
        </div>
    `;
    
    const existing = document.getElementById('activeModal');
    if (existing) existing.remove();
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    setTimeout(() => document.getElementById('activeModal').classList.add('show'), 10);
}

function closeModal() {
    const modal = document.getElementById('activeModal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => modal.remove(), 300);
    }
}

// Add payment
async function addPayment() {
    // Fetch real users from backend
    let usersOptions = '<option value="">Loading users...</option>';
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/.netlify/functions/users', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const result = await response.json();
            const users = result.users || [];
            usersOptions = '<option value="">Select user...</option>' + 
                users.map(user => `<option value="${user.id}">${user.username} (${user.email})</option>`).join('');
        }
    } catch (error) {
        console.error('Error loading users:', error);
        usersOptions = '<option value="">Error loading users</option>';
    }
    
    const content = `
        <form id="addPaymentForm" onsubmit="submitAddPayment(event)" class="admin-form">
            <div class="form-group">
                <label>User *</label>
                <select name="userId" required>
                    ${usersOptions}
                </select>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Amount *</label>
                    <input type="number" name="amount" placeholder="100.00" min="0.01" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Payment Method *</label>
                    <select name="method" required>
                        <option value="payeer">Payeer</option>
                        <option value="stripe">Stripe</option>
                        <option value="paypal">PayPal</option>
                        <option value="crypto">Cryptocurrency</option>
                        <option value="bank">Bank Transfer</option>
                        <option value="cash">Cash</option>
                        <option value="other">Other</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label>Transaction ID</label>
                <input type="text" name="transactionId" placeholder="TXN123456789">
            </div>
            <div class="form-group">
                <label>Status *</label>
                <select name="status" required>
                    <option value="completed">Completed</option>
                    <option value="pending">Pending</option>
                    <option value="failed">Failed</option>
                    <option value="refunded">Refunded</option>
                </select>
            </div>
            <div class="form-group">
                <label>Memo/Note</label>
                <textarea name="memo" rows="3" placeholder="Optional payment note or description..."></textarea>
            </div>
        </form>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="submit" form="addPaymentForm" class="btn-primary">
            <i class="fas fa-plus"></i> Add Payment
        </button>
    `;
    
    createModal('Add Manual Payment', content, actions);
}

function submitAddPayment(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const paymentData = Object.fromEntries(formData);
    
    console.log('Submitting payment with data:', paymentData);
    
    // Show loading state
    const submitBtn = event.target.querySelector('button[type="submit"]');
    if (!submitBtn) {
        const formSubmitBtn = document.querySelector('button[form="addPaymentForm"]');
        if (formSubmitBtn) {
            formSubmitBtn.disabled = true;
            formSubmitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        }
    } else {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    }
    
    // Call backend API to add payment
    const token = localStorage.getItem('token');
    
    const requestBody = {
        action: 'admin-add-payment',
        userId: paymentData.userId,
        amount: parseFloat(paymentData.amount),
        method: paymentData.method,
        transactionId: paymentData.transactionId || null,
        status: paymentData.status,
        memo: paymentData.memo || null
    };
    
    console.log('Sending request:', requestBody);
    
    fetch('/.netlify/functions/payments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(requestBody)
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.success) {
            showNotification(data.message || `Payment of $${paymentData.amount} added successfully!`, 'success');
            closeModal();
            // Reload the page to show updated data
            setTimeout(() => window.location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to add payment', 'error');
            console.error('Payment creation failed:', data.error);
            // Re-enable button
            const btn = document.querySelector('button[form="addPaymentForm"]');
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-plus"></i> Add Payment';
            }
        }
    })
    .catch(error => {
        console.error('Add payment error:', error);
        showNotification('Failed to add payment. Please try again.', 'error');
        // Re-enable button
        const btn = document.querySelector('button[form="addPaymentForm"]');
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-plus"></i> Add Payment';
        }
    });
}

// Export payments data
function exportData() {
    const content = `
        <form id="exportPaymentsForm" onsubmit="submitExportPayments(event)" class="admin-form">
            <div class="form-group">
                <label>Export Format *</label>
                <select name="format" required>
                    <option value="csv">CSV (Excel)</option>
                    <option value="pdf">PDF Report</option>
                    <option value="json">JSON Data</option>
                </select>
            </div>
            <div class="form-group">
                <label>Date Range</label>
                <select name="dateRange">
                    <option value="all">All Time</option>
                    <option value="today">Today</option>
                    <option value="week">Last 7 Days</option>
                    <option value="month">Last 30 Days</option>
                    <option value="custom">Custom Range</option>
                </select>
            </div>
            <div class="form-group">
                <label>Payment Status</label>
                <select name="statusFilter">
                    <option value="all">All Statuses</option>
                    <option value="Completed">Completed Only</option>
                    <option value="Pending">Pending Only</option>
                    <option value="Failed">Failed Only</option>
                </select>
            </div>
            <div class="export-summary" style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 16px; margin-top: 20px;">
                <h4 style="margin-bottom: 12px; color: #FF1494;">Export Summary</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
                    <div>
                        <div style="color: #888; font-size: 12px;">Total Records</div>
                        <div id="exportRecordCount" style="font-size: 20px; font-weight: 600;">-</div>
                    </div>
                    <div>
                        <div style="color: #888; font-size: 12px;">Total Amount</div>
                        <div id="exportTotalAmount" style="font-size: 20px; font-weight: 600; color: #10b981;">-</div>
                    </div>
                </div>
            </div>
        </form>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="submit" form="exportPaymentsForm" class="btn-primary">
            <i class="fas fa-file-export"></i> Export Data
        </button>
    `;
    
    createModal('Export Payments Data', content, actions);
}

async function submitExportPayments(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const exportData = Object.fromEntries(formData);
    
    const submitBtn = document.querySelector('button[form="exportPaymentsForm"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Exporting...';
    }
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/.netlify/functions/payments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                action: 'export',
                format: exportData.format,
                dateFrom: exportData.dateFrom,
                dateTo: exportData.dateTo,
                status: exportData.status
            })
        });
        
        const data = await response.json();
        if (data.success) {
            // Create download link
            const blob = new Blob([data.content], { type: data.mimeType });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = data.filename || `payments-export.${exportData.format}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showNotification('Export complete! Download started.', 'success');
            closeModal();
        } else {
            showNotification(data.error || 'Failed to export payments', 'error');
        }
        
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-download"></i> Export';
        }
    } catch (error) {
        console.error('Export payments error:', error);
        showNotification('Failed to export payments. Please try again.', 'error');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-download"></i> Export';
        }
    }
}

// Update payment method
async function updatePaymentMethod(paymentId, method) {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/.netlify/functions/payments', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                action: 'update-method',
                paymentId: paymentId,
                method: method
            })
        });
        
        const data = await response.json();
        if (data.success) {
            showNotification(`Payment #${paymentId} method updated to ${method}`, 'success');
            setTimeout(() => window.location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to update payment method', 'error');
        }
    } catch (error) {
        console.error('Update payment method error:', error);
        showNotification('Failed to update payment method. Please try again.', 'error');
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    handleSearch('paymentSearch', 'paymentsTable');
    await loadPayments();
});

// Load real payments from database
async function loadPayments() {
    const tbody = document.getElementById('paymentsTableBody');
    if (!tbody) return;

    tbody.innerHTML = '<tr><td colspan="11" style="text-align: center; padding: 20px;"><i class="fas fa-spinner fa-spin"></i> Loading payments...</td></tr>';

    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/.netlify/functions/payments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ action: 'history' })
        });

        const data = await response.json();
        
        if (data.payments && data.payments.length > 0) {
            tbody.innerHTML = '';
            
            // Fetch users to get username mapping
            const usersResponse = await fetch('/.netlify/functions/users', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            const usersData = await usersResponse.json();
            const users = usersData.users || [];
            const userMap = {};
            users.forEach(u => {
                userMap[u.id] = { username: u.username, balance: u.balance };
            });
            
            data.payments.forEach(payment => {
                const user = userMap[payment.user_id] || { username: 'Unknown', balance: 0 };
                const createdDate = new Date(payment.created_at).toLocaleString();
                const updatedDate = payment.updated_at ? new Date(payment.updated_at).toLocaleString() : createdDate;
                
                const statusClass = payment.status === 'completed' ? 'completed' : 
                                  payment.status === 'pending' ? 'pending' : 
                                  payment.status === 'failed' ? 'failed' : 'refunded';
                
                const row = `
                    <tr>
                        <td>${payment.id}</td>
                        <td>${user.username}</td>
                        <td>$${parseFloat(user.balance || 0).toFixed(2)}</td>
                        <td>$${parseFloat(payment.amount).toFixed(2)}</td>
                        <td>
                            <select class="inline-select" onchange="updatePaymentMethod('${payment.id}', this.value)">
                                <option ${payment.method === 'payeer' ? 'selected' : ''}>payeer</option>
                                <option ${payment.method === 'stripe' ? 'selected' : ''}>stripe</option>
                                <option ${payment.method === 'paypal' ? 'selected' : ''}>paypal</option>
                                <option ${payment.method === 'crypto' ? 'selected' : ''}>crypto</option>
                                <option ${payment.method === 'bank' ? 'selected' : ''}>bank</option>
                                <option ${payment.method === 'cash' ? 'selected' : ''}>cash</option>
                                <option ${payment.method === 'other' ? 'selected' : ''}>other</option>
                            </select>
                        </td>
                        <td><span class="status-badge ${statusClass}">${payment.status}</span></td>
                        <td><span class="risk-badge low">Low</span></td>
                        <td>${payment.memo || '-'}</td>
                        <td>${createdDate}</td>
                        <td>${updatedDate}</td>
                        <td>${payment.gateway_response?.manual ? 'Manual' : 'Live'}</td>
                    </tr>
                `;
                tbody.insertAdjacentHTML('beforeend', row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="11" style="text-align: center; padding: 20px; color: #888;">No payments found</td></tr>';
        }
    } catch (error) {
        console.error('Load payments error:', error);
        tbody.innerHTML = '<tr><td colspan="11" style="text-align: center; padding: 20px; color: #ef4444;">Failed to load payments. Please refresh the page.</td></tr>';
    }
}
