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
async function addTicket() {
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
        <form id="addTicketForm" onsubmit="submitAddTicket(event)" class="admin-form">
            <div class="form-group">
                <label>User *</label>
                <select name="userId" required>
                    ${usersOptions}
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
    
    // Show loading state
    const submitBtn = document.querySelector('button[form="addTicketForm"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating...';
    }
    
    // Call backend API to create ticket
    const token = localStorage.getItem('token');
    
    fetch('/.netlify/functions/tickets', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            action: 'create',
            userId: ticketData.userId,
            subject: ticketData.subject,
            category: ticketData.category,
            priority: ticketData.priority,
            status: ticketData.status || 'open',
            orderId: ticketData.orderId || null,
            message: ticketData.message || 'Ticket created by admin'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message || 'Ticket created successfully!', 'success');
            closeModal();
            setTimeout(() => window.location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to create ticket', 'error');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-plus"></i> Create Ticket';
            }
        }
    })
    .catch(error => {
        console.error('Create ticket error:', error);
        showNotification('Failed to create ticket. Please try again.', 'error');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-plus"></i> Create Ticket';
        }
    });
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

async function submitReplyTicket(event, ticketId) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const message = formData.get('message');
    
    const submitBtn = document.querySelector('button[form="replyTicketForm"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    }
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/.netlify/functions/tickets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                action: 'reply',
                ticketId: ticketId,
                message: message,
                isAdmin: true
            })
        });
        
        const data = await response.json();
        if (data.success) {
            showNotification(`Reply sent to ticket #${ticketId}`, 'success');
            closeModal();
            setTimeout(() => window.location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to send reply', 'error');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-reply"></i> Send Reply';
            }
        }
    } catch (error) {
        console.error('Reply ticket error:', error);
        showNotification('Failed to send reply. Please try again.', 'error');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-reply"></i> Send Reply';
        }
    }
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

async function submitQuickReply(event, ticketId) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const message = formData.get('message');
    const autoClose = formData.get('autoClose') === 'on';
    
    const submitBtn = document.querySelector('button[form="quickReplyForm"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    }
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/.netlify/functions/tickets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                action: 'reply',
                ticketId: ticketId,
                message: message,
                isAdmin: true,
                autoClose: autoClose
            })
        });
        
        const data = await response.json();
        if (data.success) {
            showNotification(`Reply sent to ticket #${ticketId}`, 'success');
            closeModal();
            setTimeout(() => window.location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to send reply', 'error');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-reply"></i> Send Reply';
            }
        }
    } catch (error) {
        console.error('Quick reply error:', error);
        showNotification('Failed to send reply. Please try again.', 'error');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-reply"></i> Send Reply';
        }
    }
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
async function updateTicketStatus(ticketId, status) {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/.netlify/functions/tickets', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                action: 'update-status',
                ticketId: ticketId,
                status: status
            })
        });
        
        const data = await response.json();
        if (data.success) {
            showNotification(`Ticket #${ticketId} status updated to ${status}`, 'success');
            setTimeout(() => window.location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to update status', 'error');
        }
    } catch (error) {
        console.error('Update status error:', error);
        showNotification('Failed to update status. Please try again.', 'error');
    }
}

// Assign ticket
async function assignTicket(ticketId, assignee) {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/.netlify/functions/tickets', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                action: 'assign',
                ticketId: ticketId,
                assignee: assignee
            })
        });
        
        const data = await response.json();
        if (data.success) {
            showNotification(`Ticket #${ticketId} assigned to ${assignee}`, 'success');
            setTimeout(() => window.location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to assign ticket', 'error');
        }
    } catch (error) {
        console.error('Assign ticket error:', error);
        showNotification('Failed to assign ticket. Please try again.', 'error');
    }
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

async function confirmCloseTicket(ticketId) {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/.netlify/functions/tickets', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                action: 'close',
                ticketId: ticketId
            })
        });
        
        const data = await response.json();
        if (data.success) {
            showNotification(`Ticket #${ticketId} has been closed`, 'success');
            closeModal();
            setTimeout(() => window.location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to close ticket', 'error');
        }
    } catch (error) {
        console.error('Close ticket error:', error);
        showNotification('Failed to close ticket. Please try again.', 'error');
    }
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

async function confirmDeleteTicket(ticketId) {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/.netlify/functions/tickets', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                ticketId: ticketId
            })
        });
        
        const data = await response.json();
        if (data.success) {
            showNotification(`Ticket #${ticketId} deleted successfully`, 'success');
            closeModal();
            setTimeout(() => window.location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to delete ticket', 'error');
        }
    } catch (error) {
        console.error('Delete ticket error:', error);
        showNotification('Failed to delete ticket. Please try again.', 'error');
    }
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
document.addEventListener('DOMContentLoaded', async () => {
    handleSearch('ticketSearch', 'ticketsTable');
    await loadTickets();
});

// Load real tickets from database
async function loadTickets() {
    const tbody = document.getElementById('ticketsTableBody');
    if (!tbody) return;

    tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 20px;"><i class="fas fa-spinner fa-spin"></i> Loading tickets...</td></tr>';

    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/.netlify/functions/tickets', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();
        
        if (data.tickets && data.tickets.length > 0) {
            tbody.innerHTML = '';
            
            data.tickets.forEach(ticket => {
                const createdDate = new Date(ticket.created_at).toLocaleString();
                const updatedDate = ticket.updated_at ? new Date(ticket.updated_at).toLocaleString() : createdDate;
                const isUnread = ticket.status === 'open' || ticket.status === 'pending';
                
                const categoryClass = ticket.category === 'orders' ? 'orders' :
                                    ticket.category === 'payment' ? 'payment' :
                                    ticket.category === 'technical' ? 'technical' : 'other';
                
                const row = `
                    <tr ${isUnread ? 'class="unread-ticket"' : ''}>
                        <td><input type="checkbox" class="ticket-checkbox"></td>
                        <td>${ticket.id}</td>
                        <td>${ticket.users?.username || 'Unknown'}</td>
                        <td>
                            <div class="ticket-subject">
                                <span class="category-badge ${categoryClass}">${ticket.category || 'General'}</span>
                                <a href="#" onclick="viewTicket('${ticket.id}')">${ticket.subject}</a>
                            </div>
                        </td>
                        <td>
                            <select class="inline-select status-select" onchange="updateTicketStatus('${ticket.id}', this.value)">
                                <option ${ticket.status === 'open' ? 'selected' : ''}>open</option>
                                <option ${ticket.status === 'pending' ? 'selected' : ''}>pending</option>
                                <option ${ticket.status === 'answered' ? 'selected' : ''}>answered</option>
                                <option ${ticket.status === 'closed' ? 'selected' : ''}>closed</option>
                            </select>
                        </td>
                        <td>
                            <select class="inline-select assignee-select" onchange="assignTicket('${ticket.id}', this.value)">
                                <option ${!ticket.assigned_to ? 'selected' : ''}>Unassigned</option>
                                <option ${ticket.assigned_to === 'admin' ? 'selected' : ''}>Admin</option>
                                <option ${ticket.assigned_to === 'support1' ? 'selected' : ''}>Support 1</option>
                                <option ${ticket.assigned_to === 'support2' ? 'selected' : ''}>Support 2</option>
                            </select>
                        </td>
                        <td>${createdDate}</td>
                        <td>${updatedDate}</td>
                        <td>
                            <div class="actions-dropdown">
                                <button class="btn-icon"><i class="fas fa-ellipsis-v"></i></button>
                                <div class="dropdown-menu">
                                    <a href="#" onclick="viewTicket('${ticket.id}')">View</a>
                                    <a href="#" onclick="replyTicket('${ticket.id}')">Reply</a>
                                    <a href="#" onclick="closeTicket('${ticket.id}')">Close</a>
                                    <a href="#" onclick="deleteTicket('${ticket.id}')">Delete</a>
                                </div>
                            </div>
                        </td>
                    </tr>
                `;
                tbody.insertAdjacentHTML('beforeend', row);
            });
            
            // Update pagination
            const paginationInfo = document.getElementById('paginationInfo');
            if (paginationInfo) {
                paginationInfo.textContent = `Showing 1-${Math.min(data.tickets.length, 50)} of ${data.tickets.length}`;
            }
        } else {
            tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 20px; color: #888;">No tickets found</td></tr>';
        }
    } catch (error) {
        console.error('Load tickets error:', error);
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 20px; color: #ef4444;">Failed to load tickets. Please refresh the page.</td></tr>';
    }
}
