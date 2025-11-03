// API Dashboard JavaScript with Encryption

// Security Constants
const ENCRYPTION_KEY = 'BOTZZZ773_SECURE_KEY_2025'; // In production, use user-specific key

// Security Helper: Encrypt API key
function encryptApiKey(apiKey) {
    try {
        const encrypted = CryptoJS.AES.encrypt(apiKey, ENCRYPTION_KEY).toString();
        return encrypted;
    } catch (error) {
        console.error('Encryption error:', error);
        return apiKey; // Fallback to plain text if encryption fails
    }
}

// Security Helper: Decrypt API key
function decryptApiKey(encryptedKey) {
    try {
        const decrypted = CryptoJS.AES.decrypt(encryptedKey, ENCRYPTION_KEY).toString(CryptoJS.enc.Utf8);
        return decrypted || encryptedKey; // Fallback if decryption fails
    } catch (error) {
        console.error('Decryption error:', error);
        return encryptedKey; // Fallback to encrypted text if decryption fails
    }
}

// Modal functions
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
    }
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
    }
}

// Generate random API key with secure format
function generateRandomKey() {
    // Generate a secure random API key
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const specialChars = '!@#$%^&*';
    let key = '';
    
    // Generate 48 random characters for maximum security
    for (let i = 0; i < 48; i++) {
        if (i > 0 && i % 12 === 0) {
            // Add dash separator every 12 characters for readability
            key += '-';
        }
        // Mix in special characters occasionally for added security
        if (i % 15 === 7) {
            key += specialChars.charAt(Math.floor(Math.random() * specialChars.length));
        } else {
            key += chars.charAt(Math.floor(Math.random() * chars.length));
        }
    }
    
    // SECURITY: Encrypt the key before storing
    return encryptApiKey(key);
}

// Copy API key function
function copyApiKey() {
    const apiKeyElement = document.getElementById('generatedApiKey');
    const apiKey = apiKeyElement.textContent;
    
    navigator.clipboard.writeText(apiKey).then(() => {
        showMessage('API key copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showMessage('Failed to copy API key', 'error');
    });
}

// Update dashboard stats from backend
async function updateDashboardStats() {
    try {
        const token = localStorage.getItem('token');
        if (!token) return;
        
        const response = await fetch('/.netlify/functions/dashboard', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('totalRequests').textContent = (data.totalRequests || 0).toLocaleString();
            document.getElementById('totalOrders').textContent = (data.totalOrders || 0).toLocaleString();
            document.getElementById('activeProviders').textContent = (data.activeProviders || 0);
            document.getElementById('totalSpent').textContent = '$' + (data.totalSpent || 0).toFixed(2);
        }
    } catch (error) {
        console.error('Failed to load dashboard stats:', error);
        // Set default values on error
        document.getElementById('totalRequests').textContent = '0';
        document.getElementById('totalOrders').textContent = '0';
        document.getElementById('activeProviders').textContent = '0';
        document.getElementById('totalSpent').textContent = '$0.00';
    }
}

// Render API keys list from backend
async function renderApiKeys() {
    const container = document.getElementById('apiKeysList');
    
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            container.innerHTML = '<div class="empty-state"><p>Please login to view API keys</p></div>';
            return;
        }
        
        const response = await fetch('/.netlify/functions/api-keys', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        const apiKeys = data.keys || data.apiKeys || [];
        
        if (apiKeys.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                        <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    </svg>
                    <h3>No API Keys Yet</h3>
                    <p>Generate your first API key to start integrating our services</p>
                    <button class="btn-primary" onclick="document.getElementById('generateKeyBtn').click()">Generate API Key</button>
                </div>
            `;
            return;
        }
        
        container.innerHTML = apiKeys.map(key => {
            // SECURITY: Decrypt key for display (masked)
            const decryptedKey = decryptApiKey(key.key);
            const maskedKey = decryptedKey.substring(0, 20) + '••••••••••••';
            
            return `
            <div class="api-key-card">
                <div class="api-key-header">
                    <div class="api-key-info">
                        <h3>${key.name}</h3>
                        <span class="api-key-date">Created ${new Date(key.created).toLocaleDateString()}</span>
                    </div>
                    <div class="api-key-actions">
                        <button class="btn-icon" onclick="copyKeyToClipboard('${key.key}')" title="Copy API Key">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                            </svg>
                        </button>
                        <button class="btn-icon danger" onclick="deleteApiKey('${key.id}')" title="Delete API Key">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="3 6 5 6 21 6"/>
                                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                            </svg>
                        </button>
                    </div>
                </div>
                <div class="api-key-display-hidden">
                    <code>${maskedKey}</code>
                </div>
                <div class="api-key-stats">
                    <div class="key-stat">
                        <span class="key-stat-label">Requests</span>
                        <span class="key-stat-value">${key.requests || 0}</span>
                    </div>
                    <div class="key-stat">
                        <span class="key-stat-label">Last Used</span>
                        <span class="key-stat-value">${key.lastUsed ? new Date(key.lastUsed).toLocaleDateString() : 'Never'}</span>
                    </div>
                </div>
                <div class="api-key-permissions">
                    ${key.permissions.map(p => `<span class="permission-badge">${p}</span>`).join('')}
                </div>
            </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Failed to load API keys:', error);
        container.innerHTML = '<div class="empty-state"><p>Failed to load API keys</p></div>';
    }
}

// Copy key to clipboard with decryption
function copyKeyToClipboard(encryptedKey) {
    // SECURITY: Decrypt key before copying
    const decryptedKey = decryptApiKey(encryptedKey);
    
    navigator.clipboard.writeText(decryptedKey).then(() => {
        showMessage('API key copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showMessage('Failed to copy API key', 'error');
    });
}

// Delete API key from backend
async function deleteApiKey(keyId) {
    if (!confirm('Are you sure you want to delete this API key? This action cannot be undone.')) {
        return;
    }
    
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            alert('Please login to delete API keys');
            return;
        }
        
        const response = await fetch('/.netlify/functions/api-keys', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ keyId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('API key deleted successfully', 'success');
            renderApiKeys();
        } else {
            showMessage(data.error || 'Failed to delete API key', 'error');
        }
    } catch (error) {
        console.error('Delete API key error:', error);
        showMessage('Failed to delete API key', 'error');
    }
}

// Render providers list from backend
async function renderProviders() {
    const container = document.getElementById('providersList');
    
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            container.innerHTML = '<div class="empty-state"><p>Please login to view providers</p></div>';
            return;
        }
        
        const response = await fetch('/.netlify/functions/providers', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        const providers = data.providers || [];
        
        if (providers.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                        <circle cx="9" cy="7" r="4"/>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                    </svg>
                    <h3>No Providers Connected</h3>
                    <p>Add your first provider to import services and automate order fulfillment</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = providers.map(provider => `
            <div class="provider-card">
                <div class="provider-header">
                    <div class="provider-info">
                        <h3>${provider.name}</h3>
                        <span class="provider-url">${provider.api_url || provider.apiUrl}</span>
                    </div>
                    <span class="provider-status ${provider.status}">
                        ${provider.status === 'active' ? '● Active' : '● Inactive'}
                    </span>
                </div>
                <div class="provider-stats-grid">
                    <div class="provider-stat">
                        <span class="provider-stat-label">Services</span>
                        <span class="provider-stat-value">${provider.services_count || provider.servicesCount || 0}</span>
                    </div>
                    <div class="provider-stat">
                        <span class="provider-stat-label">Orders</span>
                        <span class="provider-stat-value">${provider.orders_count || provider.ordersCount || 0}</span>
                    </div>
                    <div class="provider-stat">
                        <span class="provider-stat-label">Markup</span>
                        <span class="provider-stat-value">${provider.markup}%</span>
                    </div>
                    <div class="provider-stat">
                        <span class="provider-stat-label">Added</span>
                        <span class="provider-stat-value">${new Date(provider.created_at || provider.created).toLocaleDateString()}</span>
                    </div>
                </div>
                <div class="provider-actions">
                    <button class="btn-secondary btn-sm" onclick="syncProvider('${provider.id}')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="23 4 23 10 17 10"/>
                            <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                        </svg>
                        Sync Services
                    </button>
                    <button class="btn-secondary btn-sm" onclick="editProvider('${provider.id}')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                        Edit
                    </button>
                    <button class="btn-icon danger" onclick="deleteProvider('${provider.id}')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"/>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                        </svg>
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load providers:', error);
        container.innerHTML = '<div class="empty-state"><p>Failed to load providers</p></div>';
    }
}

// Sync provider services with backend
async function syncProvider(providerId) {
    try {
        showMessage('Syncing services...', 'info');
        
        const token = localStorage.getItem('token');
        if (!token) {
            alert('Please login to sync providers');
            return;
        }
        
        const response = await fetch('/.netlify/functions/providers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                action: 'sync',
                providerId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(`Successfully synced ${data.servicesCount || 0} services`, 'success');
            renderProviders();
            updateDashboardStats();
        } else {
            showMessage(data.error || 'Failed to sync provider', 'error');
        }
    } catch (error) {
        console.error('Sync provider error:', error);
        showMessage('Failed to sync provider', 'error');
    }
}

// Edit provider
function editProvider(providerId) {
    showMessage('Edit provider functionality coming soon', 'info');
}

// Delete provider from backend
async function deleteProvider(providerId) {
    if (!confirm('Are you sure you want to delete this provider? All imported services will be removed.')) {
        return;
    }
    
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            alert('Please login to delete providers');
            return;
        }
        
        const response = await fetch('/.netlify/functions/providers', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ providerId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('Provider deleted successfully', 'success');
            renderProviders();
            updateDashboardStats();
        } else {
            showMessage(data.error || 'Failed to delete provider', 'error');
        }
    } catch (error) {
        console.error('Delete provider error:', error);
        showMessage('Failed to delete provider', 'error');
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    updateDashboardStats();
    renderApiKeys();
    renderProviders();
    
    // Generate API Key button
    document.getElementById('generateKeyBtn').addEventListener('click', function() {
        openModal('generateKeyModal');
    });
    
    // Generate API Key form
    document.getElementById('generateKeyForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const keyName = document.getElementById('keyName').value;
        const permissions = Array.from(document.querySelectorAll('#generateKeyForm input[type="checkbox"]:checked'))
            .map(cb => cb.value);
        
        if (permissions.length === 0) {
            showMessage('Please select at least one permission', 'error');
            return;
        }
        
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                alert('Please login to generate API keys');
                window.location.href = '/signin.html';
                return;
            }
            
            const response = await fetch('/.netlify/functions/api-keys', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    action: 'create',
                    name: keyName,
                    permissions: permissions
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Show the key in modal
                document.getElementById('generatedApiKey').textContent = data.key;
                
                closeModal('generateKeyModal');
                openModal('apiKeyModal');
                
                // Reset form
                document.getElementById('generateKeyForm').reset();
                
                // Re-render keys
                renderApiKeys();
            } else {
                showMessage(data.error || 'Failed to generate API key', 'error');
            }
        } catch (error) {
            console.error('Generate API key error:', error);
            showMessage('Failed to generate API key', 'error');
        }
    });
    
    // Add Provider button
    document.getElementById('addProviderBtn').addEventListener('click', function() {
        openModal('addProviderModal');
    });
    
    // Add Provider form
    document.getElementById('addProviderForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const providerName = document.getElementById('providerName').value;
        const providerApiKey = document.getElementById('providerApiKey').value;
        
        // Show loading
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>Adding Provider...</span>';
        
        try {
            // Get auth token
            const token = localStorage.getItem('token');
            if (!token) {
                alert('Please login to add providers');
                window.location.href = '/signin.html';
                return;
            }

            // Call backend to create provider
            const response = await fetch('/.netlify/functions/providers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    action: 'create',
                    name: providerName,
                    apiKey: providerApiKey,
                    status: 'active'
                })
            });

            const data = await response.json();

            if (data.success) {
                // Success - show modal
                document.getElementById('providerSuccessTitle').textContent = `${providerName} Added!`;
                document.getElementById('importedServicesCount').textContent = '0';
                document.getElementById('importedCategoriesCount').textContent = '0';
                
                closeModal('addProviderModal');
                openModal('providerSuccessModal');
                
                // Reset form
                document.getElementById('addProviderForm').reset();
                
                // Re-render providers
                renderProviders();
                updateDashboardStats();
            } else {
                alert(data.error || 'Failed to add provider');
            }
        } catch (error) {
            console.error('Add provider error:', error);
            alert('Failed to add provider. Please try again.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
    
    // Close modals when clicking outside
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal(this.id);
            }
        });
    });
});

