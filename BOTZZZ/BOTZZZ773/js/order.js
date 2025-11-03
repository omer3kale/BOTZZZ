// ==========================================
// Order Page JavaScript
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
    const orderForm = document.getElementById('orderForm');
    const platformSelect = document.getElementById('platform');
    const quantityInput = document.getElementById('quantity');
    const serviceTypeSelect = document.getElementById('serviceType');
    const estimatedPriceEl = document.getElementById('estimatedPrice');
    
    // Update estimated price on input change
    function updatePrice() {
        const platform = platformSelect.value;
        const service = serviceTypeSelect.value;
        const quantity = parseInt(quantityInput.value) || 0;
        
        if (platform && service && quantity > 0) {
            const price = calculatePrice(platform, service, quantity);
            estimatedPriceEl.textContent = '$' + price;
            estimatedPriceEl.style.animation = 'pulse 0.5s ease';
        } else {
            estimatedPriceEl.textContent = '$0.00';
        }
    }
    
    // Add pulse animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
    `;
    document.head.appendChild(style);
    
    platformSelect?.addEventListener('change', updatePrice);
    serviceTypeSelect?.addEventListener('change', updatePrice);
    quantityInput?.addEventListener('input', updatePrice);
    
    // Handle form submission
    if (orderForm) {
        orderForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(orderForm);
            const data = {
                platform: formData.get('platform'),
                serviceType: formData.get('serviceType'),
                link: formData.get('link'),
                quantity: formData.get('quantity'),
                email: formData.get('email'),
                notes: formData.get('notes')
            };
            
            // Validate
            if (!validateEmail(data.email)) {
                showMessage('Please enter a valid email address', 'error');
                return;
            }
            
            if (!validateURL(data.link)) {
                showMessage('Please enter a valid URL', 'error');
                return;
            }
            
            if (parseInt(data.quantity) < 10) {
                showMessage('Minimum order quantity is 10', 'error');
                return;
            }
            
            // Show loading
            const submitBtn = orderForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span>Processing...</span>';
            
            try {
                // Call Orders API
                const response = await fetch('/.netlify/functions/orders', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    },
                    body: JSON.stringify({
                        service_id: getServiceId(data.platform, data.serviceType),
                        link: data.link,
                        quantity: parseInt(data.quantity),
                        notes: data.notes || ''
                    })
                });

                const result = await response.json();

                if (result.success) {
                    showMessage(`Order #${result.order.id} created successfully!`, 'success');
                    orderForm.reset();
                    updatePrice();
                    
                    // Scroll to top
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                    
                    // Redirect to dashboard after 2 seconds
                    setTimeout(() => {
                        window.location.href = 'dashboard.html';
                    }, 2000);
                } else {
                    throw new Error(result.error || 'Order creation failed');
                }
            } catch (error) {
                console.error('Order error:', error);
                showMessage(error.message || 'Failed to create order. Please try again.', 'error');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        });
    }
    
    // Helper function to get service ID based on platform and type
    function getServiceId(platform, serviceType) {
        // This maps platform and service type to actual service IDs
        // In production, this should query the services API
        // For now, return a placeholder that will be replaced when services are synced
        return 1; // TODO: Get from services API or cache
    }
    
    // Pre-fill service from URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const service = urlParams.get('service');
    
    if (service) {
        // Parse service ID (e.g., "ig-followers-hq" -> platform: instagram, service: followers)
        const parts = service.split('-');
        if (parts.length >= 2) {
            const platformMap = {
                'ig': 'instagram',
                'tt': 'tiktok',
                'yt': 'youtube',
                'tw': 'twitter',
                'fb': 'facebook',
                'tg': 'telegram'
            };
            
            const platform = platformMap[parts[0]] || parts[0];
            const serviceType = parts[1];
            
            if (platformSelect && platform) {
                platformSelect.value = platform;
            }
            if (serviceTypeSelect && serviceType) {
                serviceTypeSelect.value = serviceType;
            }
            
            updatePrice();
        }
    }
    
    // Real-time link validation
    const linkInput = document.getElementById('link');
    if (linkInput) {
        linkInput.addEventListener('blur', function() {
            if (this.value && !validateURL(this.value)) {
                this.style.borderColor = '#ef4444';
                const hint = this.nextElementSibling;
                if (hint) {
                    hint.textContent = '❌ Please enter a valid URL';
                    hint.style.color = '#ef4444';
                }
            } else if (this.value) {
                this.style.borderColor = '#10b981';
                const hint = this.nextElementSibling;
                if (hint) {
                    hint.textContent = '✅ Valid URL';
                    hint.style.color = '#10b981';
                }
            }
        });
    }
    
    // Real-time email validation
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            if (this.value && !validateEmail(this.value)) {
                this.style.borderColor = '#ef4444';
                const hint = this.nextElementSibling;
                if (hint) {
                    hint.textContent = '❌ Please enter a valid email';
                    hint.style.color = '#ef4444';
                }
            } else if (this.value) {
                this.style.borderColor = '#10b981';
                const hint = this.nextElementSibling;
                if (hint) {
                    hint.textContent = '✅ Valid email';
                    hint.style.color = '#10b981';
                }
            }
        });
    }
    
    // Quantity validation
    if (quantityInput) {
        quantityInput.addEventListener('input', function() {
            const value = parseInt(this.value);
            if (value && value < 10) {
                this.style.borderColor = '#ef4444';
                const hint = this.nextElementSibling;
                if (hint) {
                    hint.textContent = '❌ Minimum quantity is 10';
                    hint.style.color = '#ef4444';
                }
            } else if (value) {
                this.style.borderColor = '#10b981';
                const hint = this.nextElementSibling;
                if (hint) {
                    hint.textContent = '✅ Valid quantity';
                    hint.style.color = '#10b981';
                }
            }
        });
    }
});

console.log('💰 Order page loaded!');
