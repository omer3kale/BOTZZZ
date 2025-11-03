// Admin Tickets Management with Real Modals

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

// Add ticket
function addTicket() {
    const content = `
        <form id="addTicketForm" onsubmit="submitAddTicket(event)" class="admin-form">
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
                    <label>Category *</label>
                    <select name="category" required>
                        <option value="Orders">Orders</option>
                        <option value="Payment">Payment</option>
                        <option value="Account">Account</option>
                        <option value="Technical">Technical</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Priority *</label>
                    <select name="priority" required>
                        <option value="Low">Low</option>
                        <option value="Medium" selected>Medium</option>
                        <option value="High">High</option>
                        <option value="Urgent">Urgent</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label>Subject *</label>
                <input type="text" name="subject" placeholder="Brief description of the issue" required>
            </div>
            <div class="form-group">
                <label>Message *</label>
                <textarea name="message" rows="5" placeholder="Detailed description of the issue..." required></textarea>
            </div>
            <div class="form-group">
                <label>Assign To</label>
                <select name="assignee">
                    <option value="">Unassigned</option>
                    <option value="support1">Support Agent 1</option>
                    <option value="support2">Support Agent 2</option>
                    <option value="admin">Admin</option>
                </select>
            </div>
            <div class="form-group">
                <label>Related Order ID</label>
                <input type="text" name="orderId" placeholder="Optional order ID if ticket is order-related">
            </div>
        </form>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="submit" form="addTicketForm" class="btn-primary">
            <i class="fas fa-plus"></i> Create Ticket
        </button>
    `;
    
    createModal('Add New Ticket', content, actions);
}

function submitAddTicket(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const ticketData = Object.fromEntries(formData);
    
    console.log('Creating ticket:', ticketData);
    showNotification('Ticket created successfully!', 'success');
    closeModal();
}

// View ticket
function viewTicket(ticketId) {
    const content = `
        <div class="ticket-details">
            <div class="ticket-header" style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 16px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h3 style="margin: 0 0 8px;">Order #12345 - Delivery Issue</h3>
                        <div style="color: #888; font-size: 14px;">
                            Ticket #${ticketId} • Created 2 days ago
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span class="badge badge-warning">Open</span>
                        <div style="color: #888; font-size: 12px; margin-top: 4px;">Priority: High</div>
                    </div>
                </div>
                <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.1);">
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; font-size: 13px;">
                        <div>
                            <div style="color: #888;">User</div>
                            <div>john_doe</div>
                        </div>
                        <div>
                            <div style="color: #888;">Category</div>
                            <div>Orders</div>
                        </div>
                        <div>
                            <div style="color: #888;">Assigned To</div>
                            <div>Support Agent 1</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="ticket-conversation" style="max-height: 400px; overflow-y: auto; margin-bottom: 20px;">
                <div class="message user-message" style="background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; padding: 12px; border-radius: 8px; margin-bottom: 12px;">
                    <div style="font-weight: 600; margin-bottom: 4px; display: flex; justify-content: space-between;">
                        <span>john_doe</span>
                        <span style="font-size: 12px; color: #888;">2 days ago</span>
                    </div>
                    <p style="margin: 0;">I ordered 1000 Instagram followers but only received 500. Can you please check this?</p>
                </div>

                <div class="message admin-message" style="background: rgba(255, 20, 147, 0.1); border-left: 3px solid #FF1494; padding: 12px; border-radius: 8px; margin-bottom: 12px;">
                    <div style="font-weight: 600; margin-bottom: 4px; display: flex; justify-content: space-between;">
                        <span>Support Agent 1</span>
                        <span style="font-size: 12px; color: #888;">1 day ago</span>
                    </div>
                    <p style="margin: 0;">Thank you for contacting us. I've checked your order and will process a refill immediately.</p>
                </div>
            </div>

            <form id="replyTicketForm" onsubmit="submitReplyTicket(event, ${ticketId})" class="admin-form">
                <div class="form-group">
                    <label>Reply Message</label>
                    <textarea name="replyMessage" rows="4" placeholder="Type your reply..." required></textarea>
                </div>
                <div style="display: flex; gap: 12px; align-items: center;">
                    <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
                        <input type="checkbox" name="closeTicket">
                        <span>Close ticket after sending</span>
                    </label>
                </div>
            </form>
        </div>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Close</button>
        <button type="submit" form="replyTicketForm" class="btn-primary">
            <i class="fas fa-reply"></i> Send Reply
        </button>
    `;
    
    createModal(`Ticket #${ticketId}`, content, actions);
}

function submitReplyTicket(event, ticketId) {
    event.preventDefault();
    showNotification(`Reply sent to ticket #${ticketId}`, 'success');
    closeModal();
}

// Reply to ticket (quick reply)
function replyTicket(ticketId) {
    const content = `
        <form id="quickReplyForm" onsubmit="submitQuickReply(event, ${ticketId})" class="admin-form">
            <div class="form-group">
                <label>Quick Reply *</label>
                <textarea name="message" rows="5" placeholder="Type your reply message..." required></textarea>
            </div>
            <div class="form-group">
                <label>Quick Responses</label>
                <select onchange="insertQuickResponse(this.value)" style="margin-bottom: 8px;">
                    <option value="">-- Use Template --</option>
                    <option value="working">We're working on your issue</option>
                    <option value="resolved">Your issue has been resolved</option>
                    <option value="refund">Refund has been processed</option>
                    <option value="info">We need more information</option>
                </select>
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" name="internal">
                    Internal note (not visible to user)
                </label>
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" name="autoClose">
                    Close ticket after sending
                </label>
            </div>
        </form>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="submit" form="quickReplyForm" class="btn-primary">
            <i class="fas fa-reply"></i> Send Reply
        </button>
    `;
    
    createModal(`Reply to Ticket #${ticketId}`, content, actions);
}

function submitQuickReply(event, ticketId) {
    event.preventDefault();
    showNotification(`Reply sent to ticket #${ticketId}`, 'success');
    closeModal();
}

function insertQuickResponse(text) {
    const templates = {
        'working': "Thank you for contacting us. We're currently working on resolving your issue and will update you soon.",
        'resolved': "Your issue has been resolved. Please check and let us know if you need further assistance.",
        'refund': "Your refund has been processed and should appear in your account within 3-5 business days.",
        'info': "We need some additional information to help you better. Please provide more details about your issue."
    };
    
    if (templates[text]) {
        const textarea = document.querySelector('textarea[name="message"]');
        if (textarea) textarea.value = templates[text];
    }
}

// Update ticket status
function updateTicketStatus(ticketId, status) {
    showNotification(`Ticket #${ticketId} status updated to ${status}`, 'success');
}

// Assign ticket
function assignTicket(ticketId, assignee) {
    showNotification(`Ticket #${ticketId} assigned to ${assignee}`, 'success');
}

// Close ticket
function closeTicket(ticketId) {
    const content = `
        <div class="confirmation-message">
            <i class="fas fa-check-circle" style="font-size: 48px; color: #10b981; margin-bottom: 20px;"></i>
            <p>Close ticket #${ticketId}?</p>
            <p style="color: #888; font-size: 14px; margin-top: 10px;">
                The ticket will be marked as closed. You can reopen it later if needed.
            </p>
        </div>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="button" class="btn-primary" onclick="confirmCloseTicket(${ticketId})">
            <i class="fas fa-check"></i> Close Ticket
        </button>
    `;
    
    createModal('Close Ticket', content, actions);
}

function confirmCloseTicket(ticketId) {
    showNotification(`Ticket #${ticketId} has been closed`, 'success');
    closeModal();
}

// Delete ticket
function deleteTicket(ticketId) {
    const content = `
        <div class="confirmation-message danger">
            <i class="fas fa-exclamation-triangle" style="font-size: 48px; color: #ef4444; margin-bottom: 20px;"></i>
            <p>Delete ticket #${ticketId}?</p>
            <p style="color: #888; font-size: 14px; margin-top: 10px;">
                This will permanently delete the ticket and all its messages. This action cannot be undone.
            </p>
        </div>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="button" class="btn-danger" onclick="confirmDeleteTicket(${ticketId})">
            <i class="fas fa-trash"></i> Delete Ticket
        </button>
    `;
    
    createModal('Delete Ticket', content, actions);
}

function confirmDeleteTicket(ticketId) {
    showNotification(`Ticket #${ticketId} deleted successfully`, 'success');
    closeModal();
}

// Show unread tickets
function showUnread() {
    const rows = document.querySelectorAll('#ticketsTableBody tr');
    let unreadCount = 0;
    
    rows.forEach(row => {
        if (row.classList.contains('unread-ticket')) {
            row.style.display = '';
            unreadCount++;
        } else {
            row.style.display = 'none';
        }
    });
    
    showNotification(`Showing ${unreadCount} unread tickets`, 'success');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    handleSearch('ticketSearch', 'ticketsTable');
});
