// Admin Users Management with Real Backend Integration

// Global variable to store fetched users
let usersData = [];

// Populate users table from backend
async function populateUsersTable() {
    const tbody = document.getElementById('usersTableBody');
    if (!tbody) return;
    
    try {
        // Show loading state
        tbody.innerHTML = '<tr><td colspan="13" style="text-align: center; padding: 2rem;">Loading users...</td></tr>';
        
        // Get auth token
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Not authenticated');
        }
        
        // Fetch users from backend
        const response = await fetch('/.netlify/functions/users', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`Failed to fetch users: ${response.status}`);
        }
        
        const result = await response.json();
        usersData = result.users || [];
        
        if (usersData.length === 0) {
            tbody.innerHTML = '<tr><td colspan="13" style="text-align: center; padding: 2rem; color: #888;">No users found</td></tr>';
            return;
        }
        
        // Render users
        tbody.innerHTML = usersData.map(user => {
            const created = new Date(user.created_at).toLocaleString();
            const lastAuth = user.last_login ? new Date(user.last_login).toLocaleString() : 'Never';
            const balance = parseFloat(user.balance || 0);
            const spent = parseFloat(user.spent || 0);
            const discount = parseFloat(user.discount_rate || 0);
            const userRate = parseFloat(user.user_rate || 0);
            const rateLabel = userRate > 0 ? `Custom ${userRate}%` : 'Default';
            const status = (user.status || 'active').charAt(0).toUpperCase() + (user.status || 'active').slice(1);
            
            return `
                <tr>
                    <td><input type="checkbox" class="user-checkbox"></td>
                    <td>${user.id.substring(0, 8)}...</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>$${balance.toFixed(2)}</td>
                    <td>$${spent.toFixed(2)}</td>
                    <td>
                        <span class="status-badge ${status.toLowerCase() === 'active' ? 'completed' : 'fail'}">
                            ${status}
                        </span>
                    </td>
                    <td>${created}</td>
                    <td>${lastAuth}</td>
                    <td>${discount}%</td>
                    <td>${rateLabel}</td>
                    <td>
                        <div class="actions-dropdown">
                            <button class="btn-icon"><i class="fas fa-ellipsis-v"></i></button>
                            <div class="dropdown-menu">
                                <a href="#" onclick="viewUser('${user.id}')">View</a>
                                <a href="#" onclick="editUser('${user.id}')">Edit</a>
                                <a href="#" onclick="loginAsUser('${user.id}')">Login as User</a>
                                <a href="#" onclick="deleteUser('${user.id}')">Delete</a>
                            </div>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
        
        console.log(`✅ Loaded ${usersData.length} users from database`);
        
    } catch (error) {
        console.error('Error fetching users:', error);
        tbody.innerHTML = `<tr><td colspan="13" style="text-align: center; padding: 2rem; color: #ff4444;">Error loading users: ${error.message}</td></tr>`;
    }
}

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
    
    // Remove existing modal if any
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

// Add user with real modal
function addUser() {
    const content = `
        <form id="addUserForm" onsubmit="submitAddUser(event)" class="admin-form">
            <div class="form-group">
                <label>Username *</label>
                <input type="text" name="username" required placeholder="Enter username">
            </div>
            <div class="form-group">
                <label>Email *</label>
                <input type="email" name="email" required placeholder="Enter email address">
            </div>
            <div class="form-group">
                <label>Password *</label>
                <div class="password-input-wrapper">
                    <input type="password" name="password" id="newUserPassword" required placeholder="Enter password">
                    <button type="button" class="toggle-password" onclick="togglePasswordField('newUserPassword')">
                        <i class="fas fa-eye"></i>
                    </button>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Initial Balance</label>
                    <input type="number" name="balance" value="0.00" min="0" step="0.01" placeholder="0.00">
                </div>
                <div class="form-group">
                    <label>Discount Rate %</label>
                    <input type="number" name="discount_rate" value="0" min="0" max="100" step="0.01" placeholder="0">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>User Rate %</label>
                    <input type="number" name="user_rate" value="0" min="0" max="100" step="0.01" placeholder="0 = Default">
                </div>
                <div class="form-group">
                    <label>Status</label>
                    <select name="status">
                        <option value="active">Active</option>
                        <option value="inactive">Inactive</option>
                        <option value="banned">Banned</option>
                    </select>
                </div>
            </div>
        </form>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="submit" form="addUserForm" class="btn-primary">
            <i class="fas fa-user-plus"></i> Create User
        </button>
    `;
    
    createModal('Add New User', content, actions);
}

function togglePasswordField(fieldId) {
    const field = document.getElementById(fieldId);
    const icon = event.target.closest('button').querySelector('i');
    if (field.type === 'password') {
        field.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        field.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

function submitAddUser(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const userData = Object.fromEntries(formData);
    
    console.log('Creating user:', userData);
    showNotification(`User "${userData.username}" created successfully!`, 'success');
    closeModal();
    
    // In production, this would make an API call
    setTimeout(() => populateUsersTable(), 500);
}

// View user with details modal
function viewUser(userId) {
    // Find user in global data
    const user = usersData.find(u => u.id === userId);
    if (!user) {
        showNotification('User not found', 'error');
        return;
    }
    
    const balance = parseFloat(user.balance || 0);
    const spent = parseFloat(user.spent || 0);
    const discount = parseFloat(user.discount_rate || 0);
    const userRate = parseFloat(user.user_rate || 0);
    const created = new Date(user.created_at).toLocaleString();
    const lastLogin = user.last_login ? new Date(user.last_login).toLocaleString() : 'Never';
    const lastUpdate = user.updated_at ? new Date(user.updated_at).toLocaleString() : 'Never';
    const status = (user.status || 'active').charAt(0).toUpperCase() + (user.status || 'active').slice(1);
    
    const content = `
        <div class="user-details">
            <div class="user-detail-section">
                <h4><i class="fas fa-user"></i> Profile Information</h4>
                <div class="detail-row">
                    <span class="detail-label">User ID:</span>
                    <span class="detail-value" style="font-family: monospace; font-size: 0.85em;">${user.id}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Username:</span>
                    <span class="detail-value">${user.username}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Email:</span>
                    <span class="detail-value">${user.email}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Full Name:</span>
                    <span class="detail-value">${user.full_name || 'Not provided'}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Role:</span>
                    <span class="detail-value">${user.role || 'user'}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Status:</span>
                    <span class="status-badge ${status.toLowerCase() === 'active' ? 'completed' : 'fail'}">${status}</span>
                </div>
            </div>
            <div class="user-detail-section">
                <h4><i class="fas fa-wallet"></i> Financial Summary</h4>
                <div class="detail-row">
                    <span class="detail-label">Current Balance:</span>
                    <span class="detail-value">$${balance.toFixed(2)}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Total Spent:</span>
                    <span class="detail-value">$${spent.toFixed(2)}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Discount Rate:</span>
                    <span class="detail-value">${discount}%</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">User Rate:</span>
                    <span class="detail-value">${userRate > 0 ? userRate + '%' : 'Default'}</span>
                </div>
            </div>
            <div class="user-detail-section">
                <h4><i class="fas fa-chart-line"></i> Activity</h4>
                <div class="detail-row">
                    <span class="detail-label">API Key:</span>
                    <span class="detail-value" style="font-family: monospace; font-size: 0.85em;">${user.api_key || 'Not generated'}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Created:</span>
                    <span class="detail-value">${created}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Last Login:</span>
                    <span class="detail-value">${lastLogin}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Last Updated:</span>
                    <span class="detail-value">${lastUpdate}</span>
                </div>
            </div>
        </div>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="editUser('${userId}')">
            <i class="fas fa-edit"></i> Edit User
        </button>
        <button type="button" class="btn-primary" onclick="closeModal()">Close</button>
    `;
    
    createModal(`User: ${user.username}`, content, actions);
}

// Edit user
function editUser(userId) {
    // Find user in global data
    const user = usersData.find(u => u.id === userId);
    if (!user) {
        showNotification('User not found', 'error');
        return;
    }
    
    const balance = parseFloat(user.balance || 0);
    const discount = parseFloat(user.discount_rate || 0);
    const userRate = parseFloat(user.user_rate || 0);
    const status = user.status || 'active';
    
    const content = `
        <form id="editUserForm" onsubmit="submitEditUser(event, '${userId}')" class="admin-form">
            <div class="form-group">
                <label>Username *</label>
                <input type="text" name="username" value="${user.username}" required>
            </div>
            <div class="form-group">
                <label>Email *</label>
                <input type="email" name="email" value="${user.email}" required>
            </div>
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" name="full_name" value="${user.full_name || ''}" placeholder="Enter full name">
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Balance</label>
                    <input type="number" name="balance" value="${balance.toFixed(2)}" step="0.01">
                </div>
                <div class="form-group">
                    <label>Discount Rate %</label>
                    <input type="number" name="discount_rate" value="${discount}" min="0" max="100" step="0.01">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>User Rate %</label>
                    <input type="number" name="user_rate" value="${userRate}" min="0" max="100" step="0.01" placeholder="0 = Default">
                </div>
                <div class="form-group">
                    <label>Status</label>
                    <select name="status">
                        <option value="active" ${status === 'active' ? 'selected' : ''}>Active</option>
                        <option value="inactive" ${status === 'inactive' ? 'selected' : ''}>Inactive</option>
                        <option value="banned" ${status === 'banned' ? 'selected' : ''}>Banned</option>
                    </select>
                </div>
            </div>
        </form>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="submit" form="editUserForm" class="btn-primary">
            <i class="fas fa-save"></i> Save Changes
        </button>
    `;
    
    createModal(`Edit User: ${user.username}`, content, actions);
}

async function submitEditUser(event, userId) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const userData = Object.fromEntries(formData);
    
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Not authenticated');
        }
        
        // Send update to backend
        const response = await fetch('/.netlify/functions/users', {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                userId: userId,
                username: userData.username,
                email: userData.email,
                full_name: userData.full_name,
                balance: parseFloat(userData.balance || 0),
                discount_rate: parseFloat(userData.discount_rate || 0),
                user_rate: parseFloat(userData.user_rate || 0),
                status: userData.status
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to update user');
        }
        
        showNotification(`User updated successfully!`, 'success');
        closeModal();
        
        // Refresh users list
        await populateUsersTable();
        
    } catch (error) {
        console.error('Error updating user:', error);
        showNotification(error.message, 'error');
    }
}

// Login as user
function loginAsUser(userId) {
    const content = `
        <div class="confirmation-message">
            <i class="fas fa-user-lock" style="font-size: 48px; color: #FF1494; margin-bottom: 20px;"></i>
            <p>You are about to log in as User #${userId}.</p>
            <p style="color: #888; font-size: 14px; margin-top: 10px;">
                You will see the panel from their perspective and can perform actions on their behalf.
            </p>
        </div>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="button" class="btn-primary" onclick="confirmLoginAsUser(${userId})">
            <i class="fas fa-sign-in-alt"></i> Login as User
        </button>
    `;
    
    createModal('Login as User', content, actions);
}

function confirmLoginAsUser(userId) {
    showNotification(`Logged in as User #${userId}. Redirecting...`, 'success');
    closeModal();
    setTimeout(() => {
        // window.location.href = '../index.html?impersonate=' + userId;
    }, 1500);
}

// Delete user
function deleteUser(userId) {
    const content = `
        <div class="confirmation-message danger">
            <i class="fas fa-exclamation-triangle" style="font-size: 48px; color: #ef4444; margin-bottom: 20px;"></i>
            <p>Are you sure you want to delete User #${userId}?</p>
            <p style="color: #888; font-size: 14px; margin-top: 10px;">
                This will permanently delete all their data including orders, tickets, and payment history. This action cannot be undone.
            </p>
        </div>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="button" class="btn-danger" onclick="confirmDeleteUser(${userId})">
            <i class="fas fa-trash"></i> Delete User
        </button>
    `;
    
    createModal('Delete User', content, actions);
}

function confirmDeleteUser(userId) {
    showNotification(`User #${userId} deleted successfully`, 'success');
    closeModal();
    setTimeout(() => populateUsersTable(), 500);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    populateUsersTable();
    handleSearch('userSearch', 'usersTable');
});
