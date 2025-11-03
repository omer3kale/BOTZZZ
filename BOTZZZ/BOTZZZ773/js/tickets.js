// Tickets System
let currentTicket = null;

// Category subcategories mapping
const categorySubcategories = {
    orders: ['Refill', 'Cancel', 'Speed'],
    payment: [],
    other: []
};

// Sample tickets data (in production, this would come from backend)
let tickets = [
    {
        id: 'TKT-12345',
        subject: 'Need refill for order #54321',
        category: 'Orders',
        subcategory: 'Refill',
        status: 'open',
        orderId: '54321',
        createdAt: '2024-11-01 14:30',
        updatedAt: '2024-11-01 14:30',
        messages: [
            {
                id: 1,
                author: 'You',
                role: 'user',
                content: 'My order #54321 for 1000 Instagram followers has dropped to 800. I need a refill please.',
                date: '2024-11-01 14:30'
            }
        ]
    },
    {
        id: 'TKT-12344',
        subject: 'Payment not reflected in balance',
        category: 'Payment',
        subcategory: null,
        status: 'pending',
        orderId: null,
        createdAt: '2024-10-31 09:15',
        updatedAt: '2024-10-31 16:45',
        messages: [
            {
                id: 1,
                author: 'You',
                role: 'user',
                content: 'I made a payment of $50 via Payeer but it\'s not showing in my balance. Transaction ID: PYR123456789',
                date: '2024-10-31 09:15'
            },
            {
                id: 2,
                author: 'Admin',
                role: 'admin',
                content: 'Thank you for contacting us. We are currently investigating your payment. We will update you within 24 hours.',
                date: '2024-10-31 16:45'
            }
        ]
    },
    {
        id: 'TKT-12343',
        subject: 'How to use API?',
        category: 'Other',
        subcategory: null,
        status: 'closed',
        orderId: null,
        createdAt: '2024-10-30 11:20',
        updatedAt: '2024-10-30 13:00',
        messages: [
            {
                id: 1,
                author: 'You',
                role: 'user',
                content: 'I want to integrate your API into my website. Can you provide documentation?',
                date: '2024-10-30 11:20'
            },
            {
                id: 2,
                author: 'Admin',
                role: 'admin',
                content: 'Sure! Please visit our API documentation page at https://botzzz773.com/api. You can also generate your API key from the API dashboard.',
                date: '2024-10-30 12:30'
            },
            {
                id: 3,
                author: 'You',
                role: 'user',
                content: 'Perfect! Thank you!',
                date: '2024-10-30 13:00'
            }
        ]
    }
];

// Load tickets from backend
async function loadTickets() {
    try {
        const token = localStorage.getItem('authToken');
        if (!token) return;
        
        const response = await fetch('/.netlify/functions/tickets', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        if (data.success && data.tickets) {
            tickets = data.tickets;
        }
    } catch (error) {
        console.error('Failed to load tickets:', error);
        // Keep sample tickets on error
    }
}

// Save new ticket to backend
async function saveTicket(ticketData) {
    try {
        const token = localStorage.getItem('authToken');
        if (!token) {
            alert('Please login to submit tickets');
            window.location.href = '/signin.html';
            return false;
        }
        
        const response = await fetch('/.netlify/functions/tickets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                action: 'create',
                ...ticketData
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Add new ticket to local array
            tickets.unshift(data.ticket);
            return true;
        } else {
            alert(data.error || 'Failed to create ticket');
            return false;
        }
    } catch (error) {
        console.error('Failed to save ticket:', error);
        alert('Failed to create ticket. Please try again.');
        return false;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTickets();
    renderTickets();
    setupCategoryChange();
    setupFilterButtons();
    setupNewTicketForm();
});

// Render tickets list
function renderTickets(filter = 'all') {
    const ticketsList = document.getElementById('ticketsList');
    
    let filteredTickets = tickets;
    if (filter !== 'all') {
        filteredTickets = tickets.filter(t => t.status === filter);
    }

    if (filteredTickets.length === 0) {
        ticketsList.innerHTML = `
            <div style="text-align: center; padding: 40px 20px; color: rgba(255, 255, 255, 0.5);">
                <p>No ${filter === 'all' ? '' : filter} tickets found</p>
            </div>
        `;
        return;
    }

    ticketsList.innerHTML = filteredTickets.map(ticket => `
        <div class="ticket-item ${currentTicket?.id === ticket.id ? 'active' : ''}" onclick="selectTicket('${ticket.id}')">
            <div class="ticket-item-header">
                <span class="ticket-id">${ticket.id}</span>
                <span class="ticket-status ${ticket.status}">${ticket.status}</span>
            </div>
            <div class="ticket-subject">${ticket.subject}</div>
            <div class="ticket-meta">
                <span class="ticket-category">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M20 7h-9M14 17H5M3 12h18"/>
                    </svg>
                    ${ticket.category}
                </span>
                <span class="ticket-date">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <polyline points="12 6 12 12 16 14"/>
                    </svg>
                    ${formatDate(ticket.updatedAt)}
                </span>
            </div>
        </div>
    `).join('');
}

// Select ticket
function selectTicket(ticketId) {
    currentTicket = tickets.find(t => t.id === ticketId);
    renderTicketDetails();
    renderTickets(); // Re-render to update active state
}

// Render ticket details
function renderTicketDetails() {
    const emptyState = document.getElementById('emptyState');
    const ticketDetails = document.getElementById('ticketDetails');

    if (!currentTicket) {
        emptyState.style.display = 'flex';
        ticketDetails.style.display = 'none';
        return;
    }

    emptyState.style.display = 'none';
    ticketDetails.style.display = 'block';

    ticketDetails.innerHTML = `
        <div class="ticket-details-header">
            <div class="ticket-details-info">
                <div class="ticket-details-id">${currentTicket.id}</div>
                <h2 class="ticket-details-subject">${currentTicket.subject}</h2>
                <div class="ticket-details-meta">
                    <div class="ticket-details-meta-item">
                        <span class="category-badge">
                            ${currentTicket.category}
                            ${currentTicket.subcategory ? ` → ${currentTicket.subcategory}` : ''}
                        </span>
                    </div>
                    <div class="ticket-details-meta-item">
                        <strong>Status:</strong>
                        <span class="ticket-status ${currentTicket.status}">${currentTicket.status}</span>
                    </div>
                    ${currentTicket.orderId ? `
                        <div class="ticket-details-meta-item">
                            <strong>Order ID:</strong> ${currentTicket.orderId}
                        </div>
                    ` : ''}
                    <div class="ticket-details-meta-item">
                        <strong>Created:</strong> ${currentTicket.createdAt}
                    </div>
                </div>
            </div>
        </div>

        <div class="ticket-messages">
            ${currentTicket.messages.map(message => `
                <div class="message ${message.role === 'admin' ? 'admin' : ''}">
                    <div class="message-header">
                        <div class="message-author">
                            <div class="message-avatar">
                                ${message.author.charAt(0).toUpperCase()}
                            </div>
                            <div class="message-author-info">
                                <div class="message-author-name">${message.author}</div>
                                ${message.role === 'admin' ? '<div class="message-author-role">Support Team</div>' : ''}
                            </div>
                        </div>
                        <div class="message-date">${message.date}</div>
                    </div>
                    <div class="message-content">${message.content}</div>
                </div>
            `).join('')}
        </div>

        ${currentTicket.status !== 'closed' ? `
            <div class="reply-form">
                <h3>Reply to Ticket</h3>
                <textarea id="replyMessage" placeholder="Type your message here..."></textarea>
                <div class="reply-form-actions">
                    <button type="button" class="btn-secondary" onclick="closeTicket()">Close Ticket</button>
                    <button type="button" class="btn-primary" onclick="sendReply()">Send Reply</button>
                </div>
            </div>
        ` : `
            <div class="reply-form">
                <p style="color: rgba(255, 255, 255, 0.6); text-align: center;">This ticket is closed.</p>
            </div>
        `}
    `;
}

// Send reply to backend
async function sendReply() {
    const replyMessage = document.getElementById('replyMessage');
    const message = replyMessage.value.trim();

    if (!message) {
        alert('Please enter a message');
        return;
    }

    try {
        const token = localStorage.getItem('authToken');
        if (!token) {
            alert('Please login to reply to tickets');
            return;
        }
        
        const response = await fetch('/.netlify/functions/tickets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                action: 'reply',
                ticketId: currentTicket.id,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const newMessage = {
                id: currentTicket.messages.length + 1,
                author: 'You',
                role: 'user',
                content: message,
                date: new Date().toLocaleString('en-US', {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit'
                })
            };
            
            currentTicket.messages.push(newMessage);
            currentTicket.updatedAt = newMessage.date;
            renderTicketDetails();
            replyMessage.value = '';
        } else {
            alert(data.error || 'Failed to send reply');
        }
    } catch (error) {
        console.error('Failed to send reply:', error);
        alert('Failed to send reply. Please try again.');
    }
}

// Close ticket via backend
async function closeTicket() {
    if (!confirm('Are you sure you want to close this ticket?')) return;
    
    try {
        const token = localStorage.getItem('authToken');
        if (!token) {
            alert('Please login to close tickets');
            return;
        }
        
        const response = await fetch('/.netlify/functions/tickets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                action: 'close',
                ticketId: currentTicket.id
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentTicket.status = 'closed';
            currentTicket.updatedAt = new Date().toLocaleString('en-US', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
            renderTickets();
            renderTicketDetails();
        } else {
            alert(data.error || 'Failed to close ticket');
        }
    } catch (error) {
        console.error('Failed to close ticket:', error);
        alert('Failed to close ticket. Please try again.');
    }
}

// Setup filter buttons
function setupFilterButtons() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const status = btn.dataset.status;
            renderTickets(status);
        });
    });
}

// Modal functions
function openNewTicketModal() {
    document.getElementById('newTicketModal').classList.add('active');
}

function closeNewTicketModal() {
    document.getElementById('newTicketModal').classList.remove('active');
    document.getElementById('newTicketForm').reset();
    document.getElementById('subcategoryGroup').style.display = 'none';
    document.getElementById('orderIdGroup').style.display = 'none';
}

// Setup category change
function setupCategoryChange() {
    const categorySelect = document.getElementById('ticketCategory');
    const subcategoryGroup = document.getElementById('subcategoryGroup');
    const subcategorySelect = document.getElementById('ticketSubcategory');
    const orderIdGroup = document.getElementById('orderIdGroup');

    categorySelect.addEventListener('change', (e) => {
        const category = e.target.value;
        
        if (category === 'orders') {
            // Show subcategory for orders
            subcategoryGroup.style.display = 'block';
            subcategorySelect.innerHTML = '<option value="">Select Subcategory</option>' +
                categorySubcategories.orders.map(sub => `<option value="${sub}">${sub}</option>`).join('');
            subcategorySelect.required = true;
            
            // Show order ID field
            orderIdGroup.style.display = 'block';
        } else {
            // Hide subcategory for payment and other
            subcategoryGroup.style.display = 'none';
            subcategorySelect.required = false;
            
            // Hide order ID field for non-order categories
            if (category !== 'orders') {
                orderIdGroup.style.display = 'none';
            }
        }
    });
}

// Setup new ticket form
function setupNewTicketForm() {
    const form = document.getElementById('newTicketForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const category = document.getElementById('ticketCategory').value;
        const subcategory = document.getElementById('ticketSubcategory').value;
        const subject = document.getElementById('ticketSubject').value;
        const message = document.getElementById('ticketMessage').value;
        const orderId = document.getElementById('ticketOrderId').value;

        const ticketData = {
            subject: subject,
            category: category.charAt(0).toUpperCase() + category.slice(1),
            subcategory: subcategory || null,
            orderId: orderId || null,
            message: message
        };

        const success = await saveTicket(ticketData);
        
        if (success) {
            closeNewTicketModal();
            renderTickets();
            if (tickets.length > 0) {
                selectTicket(tickets[0].id);
            }
            alert('Ticket created successfully!');
        }
    });
}

// Format date
function formatDate(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 60) {
        return `${diffMins}m ago`;
    } else if (diffHours < 24) {
        return `${diffHours}h ago`;
    } else if (diffDays < 7) {
        return `${diffDays}d ago`;
    } else {
        return dateStr.split(' ')[0];
    }
}
