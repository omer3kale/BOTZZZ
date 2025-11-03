// Admin Services Management with Real Modals

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

// Add new service
function addService() {
    const content = `
        <form id="addServiceForm" onsubmit="submitAddService(event)" class="admin-form">
            <div class="form-group">
                <label>Service Name *</label>
                <input type="text" name="serviceName" placeholder="Instagram Followers - High Quality" required>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Category *</label>
                    <select name="category" required>
                        <option value="">Select Category</option>
                        <option value="instagram">Instagram</option>
                        <option value="tiktok">TikTok</option>
                        <option value="youtube">YouTube</option>
                        <option value="twitter">Twitter</option>
                        <option value="facebook">Facebook</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Type *</label>
                    <select name="type" required>
                        <option value="default">Default</option>
                        <option value="subscription">Subscription</option>
                        <option value="custom">Custom</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label>Provider *</label>
                <select name="provider" required>
                    <option value="">Select Provider</option>
                    <option value="1">SMM Provider 1</option>
                    <option value="2">SMM Provider 2</option>
                    <option value="3">SMM Provider 3</option>
                </select>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Rate per 1000 *</label>
                    <input type="number" name="rate" placeholder="5.00" min="0" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Min Quantity *</label>
                    <input type="number" name="min" placeholder="100" min="1" required>
                </div>
                <div class="form-group">
                    <label>Max Quantity *</label>
                    <input type="number" name="max" placeholder="10000" min="1" required>
                </div>
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea name="description" rows="3" placeholder="Service description..."></textarea>
            </div>
            <div class="form-group">
                <label>Status</label>
                <select name="status">
                    <option value="Active" selected>Active</option>
                    <option value="Inactive">Inactive</option>
                </select>
            </div>
        </form>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="submit" form="addServiceForm" class="btn-primary">
            <i class="fas fa-plus"></i> Create Service
        </button>
    `;
    
    createModal('Add New Service', content, actions);
}

function submitAddService(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const serviceData = Object.fromEntries(formData);
    
    console.log('Creating service:', serviceData);
    showNotification('Service created successfully!', 'success');
    closeModal();
}

// Import services from provider
function importServices() {
    const content = `
        <form id="importServicesForm" onsubmit="submitImportServices(event)" class="admin-form">
            <div class="form-group">
                <label>Select Provider *</label>
                <select name="provider" id="importProvider" required onchange="loadProviderServices(this.value)">
                    <option value="">Choose a provider...</option>
                    <option value="1">SMM Provider 1 (87 services)</option>
                    <option value="2">SMM Provider 2 (124 services)</option>
                    <option value="3">SMM Provider 3 (56 services)</option>
                </select>
            </div>
            <div class="form-group">
                <label>Markup Percentage *</label>
                <input type="number" name="markup" value="15" min="0" max="100" step="1" required>
                <small style="color: #888;">Add this percentage to provider rates</small>
            </div>
            <div class="form-group">
                <label>Category Mapping</label>
                <select name="categoryMapping">
                    <option value="auto">Auto-detect from provider</option>
                    <option value="instagram">Map all to Instagram</option>
                    <option value="tiktok">Map all to TikTok</option>
                    <option value="youtube">Map all to YouTube</option>
                </select>
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" name="activeOnly" checked>
                    Import only active services
                </label>
            </div>
            <div id="providerServicesPreview" style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 16px; margin-top: 16px; display: none;">
                <h4 style="margin-bottom: 12px; color: #FF1494;">Services Preview</h4>
                <div id="servicesPreviewList"></div>
            </div>
        </form>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="submit" form="importServicesForm" class="btn-primary">
            <i class="fas fa-file-import"></i> Import Services
        </button>
    `;
    
    createModal('Import Services from Provider', content, actions);
}

function loadProviderServices(providerId) {
    if (!providerId) return;
    
    const preview = document.getElementById('providerServicesPreview');
    const list = document.getElementById('servicesPreviewList');
    
    const services = [
        'Instagram Followers - Real',
        'Instagram Likes - Fast',
        'TikTok Views - HQ',
        'YouTube Subscribers - Instant'
    ];
    
    list.innerHTML = services.map(s => `<div style="padding: 4px 0; color: #aaa;">• ${s}</div>`).join('');
    preview.style.display = 'block';
}

function submitImportServices(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const importData = Object.fromEntries(formData);
    
    console.log('Importing services:', importData);
    showNotification('Services imported successfully! Syncing...', 'success');
    closeModal();
    
    setTimeout(() => {
        showNotification('87 services added to your panel', 'success');
    }, 2000);
}

// Create category
function createCategory() {
    const content = `
        <form id="createCategoryForm" onsubmit="submitCreateCategory(event)" class="admin-form">
            <div class="form-group">
                <label>Category Name *</label>
                <input type="text" name="categoryName" placeholder="e.g., Instagram" required>
            </div>
            <div class="form-group">
                <label>Category Icon</label>
                <input type="text" name="icon" placeholder="fab fa-instagram" value="fab fa-">
                <small style="color: #888;">Font Awesome icon class</small>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Display Order</label>
                    <input type="number" name="order" value="1" min="1">
                </div>
                <div class="form-group">
                    <label>Status</label>
                    <select name="status">
                        <option value="Active" selected>Active</option>
                        <option value="Inactive">Inactive</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label>Parent Category</label>
                <select name="parent">
                    <option value="">None (Top Level)</option>
                    <option value="social-media">Social Media</option>
                    <option value="video">Video Platforms</option>
                    <option value="music">Music Platforms</option>
                </select>
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea name="description" rows="2" placeholder="Category description..."></textarea>
            </div>
        </form>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="submit" form="createCategoryForm" class="btn-primary">
            <i class="fas fa-folder-plus"></i> Create Category
        </button>
    `;
    
    createModal('Create New Category', content, actions);
}

function submitCreateCategory(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const categoryData = Object.fromEntries(formData);
    
    console.log('Creating category:', categoryData);
    showNotification(`Category "${categoryData.categoryName}" created successfully!`, 'success');
    closeModal();
}

// Add subscription service
function addSubscription() {
    const content = `
        <form id="addSubscriptionForm" onsubmit="submitAddSubscription(event)" class="admin-form">
            <div class="form-group">
                <label>Service Name *</label>
                <input type="text" name="serviceName" placeholder="Instagram Auto Likes" required>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Category *</label>
                    <select name="category" required>
                        <option value="instagram">Instagram</option>
                        <option value="tiktok">TikTok</option>
                        <option value="youtube">YouTube</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Provider *</label>
                    <select name="provider" required>
                        <option value="1">SMM Provider 1</option>
                        <option value="2">SMM Provider 2</option>
                    </select>
                </div>
            </div>
            <h4 style="margin: 20px 0 12px; color: #FF1494;">Subscription Settings</h4>
            <div class="form-row">
                <div class="form-group">
                    <label>Interval (minutes) *</label>
                    <input type="number" name="interval" value="60" min="1" required>
                </div>
                <div class="form-group">
                    <label>Posts Quantity *</label>
                    <input type="number" name="posts" value="10" min="1" required>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Min Quantity per Post *</label>
                    <input type="number" name="minQty" value="100" min="1" required>
                </div>
                <div class="form-group">
                    <label>Max Quantity per Post *</label>
                    <input type="number" name="maxQty" value="1000" min="1" required>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Delay (minutes)</label>
                    <input type="number" name="delay" value="0" min="0">
                </div>
                <div class="form-group">
                    <label>Expiry (days)</label>
                    <input type="number" name="expiry" value="30" min="1">
                </div>
            </div>
            <div class="form-group">
                <label>Rate per 1000 *</label>
                <input type="number" name="rate" placeholder="5.00" min="0" step="0.01" required>
            </div>
        </form>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="submit" form="addSubscriptionForm" class="btn-primary">
            <i class="fas fa-sync-alt"></i> Create Subscription
        </button>
    `;
    
    createModal('Add Subscription Service', content, actions);
}

function submitAddSubscription(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const subscriptionData = Object.fromEntries(formData);
    
    console.log('Creating subscription:', subscriptionData);
    showNotification('Subscription service created successfully!', 'success');
    closeModal();
}

// Edit service
function editService(serviceId) {
    const content = `
        <form id="editServiceForm" onsubmit="submitEditService(event, ${serviceId})" class="admin-form">
            <div class="form-group">
                <label>Service Name *</label>
                <input type="text" name="serviceName" value="Instagram Followers" required>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Rate per 1000 *</label>
                    <input type="number" name="rate" value="5.50" min="0" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Min *</label>
                    <input type="number" name="min" value="100" min="1" required>
                </div>
                <div class="form-group">
                    <label>Max *</label>
                    <input type="number" name="max" value="10000" min="1" required>
                </div>
            </div>
            <div class="form-group">
                <label>Status</label>
                <select name="status">
                    <option value="Active" selected>Active</option>
                    <option value="Inactive">Inactive</option>
                </select>
            </div>
        </form>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="submit" form="editServiceForm" class="btn-primary">
            <i class="fas fa-save"></i> Save Changes
        </button>
    `;
    
    createModal(`Edit Service #${serviceId}`, content, actions);
}

function submitEditService(event, serviceId) {
    event.preventDefault();
    showNotification(`Service #${serviceId} updated successfully!`, 'success');
    closeModal();
}

// Duplicate service
function duplicateService(serviceId) {
    const content = `
        <div class="confirmation-message">
            <i class="fas fa-copy" style="font-size: 48px; color: #FF1494; margin-bottom: 20px;"></i>
            <p>Duplicate service #${serviceId}?</p>
            <p style="color: #888; font-size: 14px; margin-top: 10px;">
                This will create an exact copy of the service. You can edit it after creation.
            </p>
        </div>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="button" class="btn-primary" onclick="confirmDuplicateService(${serviceId})">
            <i class="fas fa-copy"></i> Duplicate Service
        </button>
    `;
    
    createModal('Duplicate Service', content, actions);
}

function confirmDuplicateService(serviceId) {
    showNotification(`Service #${serviceId} duplicated successfully`, 'success');
    closeModal();
}

// Toggle service status
function toggleService(serviceId) {
    const content = `
        <div class="confirmation-message">
            <i class="fas fa-power-off" style="font-size: 48px; color: #FF1494; margin-bottom: 20px;"></i>
            <p>Toggle status for service #${serviceId}?</p>
            <p style="color: #888; font-size: 14px; margin-top: 10px;">
                This will change the service status between Active and Inactive.
            </p>
        </div>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="button" class="btn-primary" onclick="confirmToggleService(${serviceId})">
            <i class="fas fa-power-off"></i> Toggle Status
        </button>
    `;
    
    createModal('Toggle Service Status', content, actions);
}

function confirmToggleService(serviceId) {
    showNotification(`Service #${serviceId} status updated`, 'success');
    closeModal();
}

// Delete service
function deleteService(serviceId) {
    const content = `
        <div class="confirmation-message danger">
            <i class="fas fa-exclamation-triangle" style="font-size: 48px; color: #ef4444; margin-bottom: 20px;"></i>
            <p>Delete service #${serviceId}?</p>
            <p style="color: #888; font-size: 14px; margin-top: 10px;">
                This will permanently delete the service. This action cannot be undone.
            </p>
        </div>
    `;
    
    const actions = `
        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="button" class="btn-danger" onclick="confirmDeleteService(${serviceId})">
            <i class="fas fa-trash"></i> Delete Service
        </button>
    `;
    
    createModal('Delete Service', content, actions);
}

function confirmDeleteService(serviceId) {
    showNotification(`Service #${serviceId} deleted successfully`, 'success');
    closeModal();
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    if (typeof handleSearch === 'function') {
        handleSearch('serviceSearch', 'servicesTable');
    }
});
