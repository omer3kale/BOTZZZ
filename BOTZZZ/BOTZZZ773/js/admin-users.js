// Admin Users Management with Real Modals

// Populate users table
function populateUsersTable() {
    const tbody = document.getElementById('usersTableBody');
    if (!tbody) return;
    
    const users = [
        { id: 11009, username: 'sherry5286', email: 'bmchbzoswr@mailna.co', balance: 0.00, spent: 0.00, status: 'Active', created: '2025-11-01 23:49:58', lastAuth: '2025-11-01 23:49:58', discount: '0%', rates: 'Default' },
        { id: 11008, username: 'azenarky', email: 'azenarky@gmail.com', balance: 0.10, spent: 5.20, status: 'Active', created: '2025-11-01 22:26:37', lastAuth: '2025-11-01 22:26:37', discount: '0%', rates: 'Default' },
        { id: 11007, username: 'ami7456727779', email: 'ami7456727779@gmail.com', balance: 0.00, spent: 0.00, status: 'Active', created: '2025-11-01 21:26:00', lastAuth: '2025-11-01 21:26:00', discount: '0%', rates: 'Default' },
        { id: 11006, username: 'yamh48378', email: 'yamh48378@gmail.com', balance: 0.00, spent: 0.00, status: 'Active', created: '2025-11-01 21:23:59', lastAuth: '2025-11-01 22:24:50', discount: '0%', rates: 'Default' },
        { id: 11005, username: 'jj1302524', email: 'jj1302524@gmail.com', balance: 5.00, spent: 0.00, status: 'Active', created: '2025-11-01 20:06:23', lastAuth: '2025-11-01 20:06:23', discount: '0%', rates: 'Default' },
        { id: 11004, username: 'codedsmm', email: 'coded@smm.com', balance: 125.50, spent: 458.20, status: 'Active', created: '2025-10-28 15:30:00', lastAuth: '2025-11-02 00:40:48', discount: '5%', rates: 'VIP' },
        { id: 11003, username: 'pritampargarbabu123', email: 'pritam@gmail.com', balance: 250.00, spent: 892.35, status: 'Active', created: '2025-10-25 10:20:00', lastAuth: '2025-11-02 00:40:20', discount: '10%', rates: 'Premium' },
        { id: 11002, username: 'vanak', email: 'vanak@test.com', balance: 75.80, spent: 124.15, status: 'Active', created: '2025-10-20 08:15:00', lastAuth: '2025-11-02 00:40:09', discount: '0%', rates: 'Default' }
    ];
    
    tbody.innerHTML = users.map(user => `
        <tr>
            <td><input type="checkbox" class="user-checkbox"></td>
            <td>${user.id}</td>
            <td>${user.username}</td>
            <td>${user.email}</td>
            <td>$${user.balance.toFixed(2)}</td>
            <td>$${user.spent.toFixed(2)}</td>
            <td>
                <span class="status-badge ${user.status === 'Active' ? 'completed' : 'fail'}">
                    ${user.status}
                </span>
            </td>
            <td>${user.created}</td>
            <td>${user.lastAuth}</td>
            <td>${user.discount}</td>
            <td>${user.rates}</td>
            <td>
                <div class="actions-dropdown">
                    <button class="btn-icon"><i class="fas fa-ellipsis-v"></i></button>
                    <div class="dropdown-menu">
                        <a href="#" onclick="viewUser(${user.id})">View</a>
                        <a href="#" onclick="editUser(${user.id})">Edit</a>
                        <a href="#" onclick="loginAsUser(${user.id})">Login as User</a>
                        <a href="#" onclick="deleteUser(${user.id})">Delete</a>
                    </div>
                </div>
            </td>
        </tr>
    `).join('');
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
                    <label>Discount %</label>
                    <input type="number" name="discount" value="0" min="0" max="100" placeholder="0">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Rate Type</label>
                    <select name="rateType">
                        <option value="Default">Default</option>
                        <option value="VIP">VIP</option>
                        <option value="Premium">Premium</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Status</label>
                    <select name="status">
                        <option value="Active">Active</option>
                        <option value="Inactive">Inactive</option>
                        <option value="Banned">Banned</option>
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
    const content = `
        <div class="user-details">
            <div class="user-detail-section">
                <h4><i class="fas fa-user"></i> Profile Information</h4>
                <div class="detail-row">
                    <span class="detail-label">User ID:</span>
                    <span class="detail-value">#${userId}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Username:</span>
                    <span class="detail-value">user_${userId}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Email:</span>
                    <span class="detail-value">user${userId}@example.com</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Status:</span>
                    <span class="status-badge completed">Active</span>
                </div>
            </div>
            <div class="user-detail-section">
                <h4><i class="fas fa-wallet"></i> Financial Summary</h4>
                <div class="detail-row">
                    <span class="detail-label">Current Balance:</span>
                    <span class="detail-value">$0.00</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Total Spent:</span>
                    <span class="detail-value">$0.00</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Discount:</span>
                    <span class="detail-value">0%</span>
                </div>
            </div>
            <div class="user-detail-section">
                <h4><i class="fas fa-chart-line"></i> Activity</h4>
                <div class="detail-row">
                    <span class="detail-label">Total Orders:</span>
                    <span class="detail-value">0</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Total Tickets:</span>
                    <span class="detail-value">0</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Created:</span>
                    <span class="detail-value">2025-11-01 20:06:23</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Last Login:</span>
                    <span class="detail-value">2025-11-01 20:06:23</span>
                </div>
            </div>
        </div>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="editUser(${userId})">
            <i class="fas fa-edit"></i> Edit User
        </button>
        <button type="button" class="btn-primary" onclick="closeModal()">Close</button>
    `;
    
    createModal(`User #${userId} Details`, content, actions);
}

// Edit user
function editUser(userId) {
    const content = `
        <form id="editUserForm" onsubmit="submitEditUser(event, ${userId})" class="admin-form">
            <div class="form-group">
                <label>Username *</label>
                <input type="text" name="username" value="user_${userId}" required>
            </div>
            <div class="form-group">
                <label>Email *</label>
                <input type="email" name="email" value="user${userId}@example.com" required>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Balance</label>
                    <input type="number" name="balance" value="0.00" step="0.01">
                </div>
                <div class="form-group">
                    <label>Discount %</label>
                    <input type="number" name="discount" value="0" min="0" max="100">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Rate Type</label>
                    <select name="rateType">
                        <option value="Default">Default</option>
                        <option value="VIP">VIP</option>
                        <option value="Premium">Premium</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Status</label>
                    <select name="status">
                        <option value="Active" selected>Active</option>
                        <option value="Inactive">Inactive</option>
                        <option value="Banned">Banned</option>
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
    
    createModal(`Edit User #${userId}`, content, actions);
}

function submitEditUser(event, userId) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const userData = Object.fromEntries(formData);
    
    console.log('Updating user #' + userId + ':', userData);
    showNotification(`User #${userId} updated successfully!`, 'success');
    closeModal();
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
