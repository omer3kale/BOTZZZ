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
function addPayment() {
    const content = `
        <form id="addPaymentForm" onsubmit="submitAddPayment(event)" class="admin-form">
            <div class="form-group">
                <label>User *</label>
                <select name="userId" required>
                    <option value="">Select user...</option>
                    <option value="1">john_doe (@john_doe)</option>
                    <option value="2">jane_smith (@jane_smith)</option>
                    <option value="3">bob_wilson (@bob_wilson)</option>
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
                    <option value="Completed">Completed</option>
                    <option value="Pending">Pending</option>
                    <option value="Failed">Failed</option>
                    <option value="Refunded">Refunded</option>
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
    
    console.log('Adding payment:', paymentData);
    showNotification(`Payment of $${paymentData.amount} added successfully!`, 'success');
    closeModal();
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
                        <div style="font-size: 20px; font-weight: 600;">1,247</div>
                    </div>
                    <div>
                        <div style="color: #888; font-size: 12px;">Total Amount</div>
                        <div style="font-size: 20px; font-weight: 600; color: #10b981;">$45,892.50</div>
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

function submitExportPayments(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const exportData = Object.fromEntries(formData);
    
    console.log('Exporting payments:', exportData);
    showNotification(`Generating ${exportData.format.toUpperCase()} export...`, 'success');
    closeModal();
    
    setTimeout(() => {
        showNotification(`Export complete! Download started.`, 'success');
    }, 1500);
}

// Update payment method
function updatePaymentMethod(paymentId, method) {
    showNotification(`Payment #${paymentId} method updated to ${method}`, 'success');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    handleSearch('paymentSearch', 'paymentsTable');
});
