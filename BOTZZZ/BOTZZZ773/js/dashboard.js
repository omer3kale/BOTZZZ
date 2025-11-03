// Dashboard Functionality - Authentication Required
(function() {
    'use strict';

    // ==========================================
    // AUTHENTICATION CHECK
    // ==========================================
    function checkAuth() {
        const token = localStorage.getItem('token');
        const user = localStorage.getItem('user');

        // If no token or user, redirect to sign in
        if (!token || !user) {
            window.location.href = 'signin.html';
            return null;
        }

        try {
            const userData = JSON.parse(user);
            return { token, user: userData };
        } catch (error) {
            console.error('Invalid user data:', error);
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = 'signin.html';
            return null;
        }
    }

    // ==========================================
    // INITIALIZE DASHBOARD
    // ==========================================
    const auth = checkAuth();
    if (!auth) return;

    const { token, user } = auth;

    // Update UI with user data
    function updateUserDisplay() {
        const userNameEl = document.getElementById('userName');
        const balanceAmountEl = document.getElementById('balanceAmount');

        if (userNameEl && user.username) {
            userNameEl.textContent = user.username;
        }

        if (balanceAmountEl && user.balance !== undefined) {
            balanceAmountEl.textContent = `$${parseFloat(user.balance).toFixed(2)}`;
        }
    }

    // ==========================================
    // MOBILE MENU TOGGLE
    // ==========================================
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const sidebar = document.querySelector('.dashboard-sidebar');

    if (mobileMenuToggle && sidebar) {
        mobileMenuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('show');
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 1024) {
                if (!sidebar.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
                    sidebar.classList.remove('show');
                }
            }
        });
    }

    // ==========================================
    // USER MENU DROPDOWN
    // ==========================================
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');

    if (userMenuBtn && userDropdown) {
        userMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            userDropdown.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            userDropdown.classList.remove('show');
        });
    }

    // ==========================================
    // LOGOUT FUNCTIONALITY
    // ==========================================
    function handleLogout() {
        // Clear all auth data
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        sessionStorage.clear();

        // Show notification
        showToast('Logged out successfully', 'success');

        // Redirect to home page
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1000);
    }

    const logoutBtn = document.getElementById('logoutBtn');
    const logoutLink = document.getElementById('logoutLink');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            handleLogout();
        });
    }

    // ==========================================
    // TOAST NOTIFICATION
    // ==========================================
    function showToast(message, type = 'success') {
        const toast = document.getElementById('toast');
        if (!toast) return;

        const messageEl = toast.querySelector('.toast-message');
        const closeBtn = toast.querySelector('.toast-close');

        // Remove existing classes
        toast.classList.remove('success', 'error', 'show');

        // Set message and type
        if (messageEl) messageEl.textContent = message;
        toast.classList.add(type);

        // Show toast
        setTimeout(() => toast.classList.add('show'), 10);

        // Auto hide after 5 seconds
        const hideTimeout = setTimeout(() => {
            toast.classList.remove('show');
        }, 5000);

        // Close button
        if (closeBtn) {
            closeBtn.onclick = () => {
                clearTimeout(hideTimeout);
                toast.classList.remove('show');
            };
        }
    }

    // ==========================================
    // SERVICES DATA
    // ==========================================
    const servicesData = {
        instagram: [
            { 
                id: '4404', 
                name: '😊 Instagram Followers | Global Users | NR | Instant Start | Very Fast | Cheapest', 
                price: 1.0105,
                min: 100,
                max: 30000,
                avgTime: '34 minutes'
            },
            { 
                id: '2717', 
                name: '😊 Instagram Followers | Flag Off | NR | 50K Per Day', 
                price: 0.736,
                min: 100,
                max: 50000,
                avgTime: '2 hours'
            },
            { 
                id: '1199', 
                name: '😊 Instagram Followers | Cancel Button ❌ | 30 Days Refill | Per Day 50K', 
                price: 1.287,
                min: 100,
                max: 50000,
                avgTime: '1 hour'
            },
            { 
                id: '3001', 
                name: '😊 Instagram Likes | Real | Instant | 5K Per Day', 
                price: 0.45,
                min: 50,
                max: 5000,
                avgTime: '15 minutes'
            }
        ],
        tiktok: [
            { 
                id: '3694', 
                name: '🎵 TikTok Followers | Global Users | NR | Instant Start | 30K Per Day', 
                price: 0.89,
                min: 100,
                max: 30000,
                avgTime: '45 minutes'
            },
            { 
                id: '3695', 
                name: '🎵 TikTok Likes | Real | Fast | 10K Per Hour', 
                price: 0.35,
                min: 100,
                max: 10000,
                avgTime: '20 minutes'
            }
        ],
        youtube: [
            { 
                id: '4403', 
                name: '▶️ YouTube Subscribe | R30 | Instant Start | Per Day 20-50 | No Drop | %100 Working', 
                price: 0.65,
                min: 50,
                max: 5000,
                avgTime: '1 hour'
            },
            { 
                id: '4448', 
                name: '▶️ YouTube Views | Lifetime Refill | Start in 0-4 Hours | No Drop | Per Day 5K', 
                price: 5.20,
                min: 100,
                max: 5000,
                avgTime: '4 hours'
            }
        ],
        twitter: [
            { 
                id: '3584', 
                name: '🐦 Twitter Tweet Views | Global Users | Instant Starts | 500K per Hour', 
                price: 0.093,
                min: 1000,
                max: 500000,
                avgTime: '30 minutes'
            },
            { 
                id: '3605', 
                name: '🐦 Twitter Followers | Real | Instant | 10K Per Day', 
                price: 1.50,
                min: 100,
                max: 10000,
                avgTime: '1 hour'
            }
        ],
        facebook: [
            { 
                id: '2001', 
                name: '👍 Facebook Page Likes | Real | 5K Per Day', 
                price: 0.85,
                min: 100,
                max: 5000,
                avgTime: '2 hours'
            }
        ],
        telegram: [
            { 
                id: '4449', 
                name: '✈️ Telegram Channel - Group Members | Real | Fast Service | Instant Start | 100K Per Day', 
                price: 0.806,
                min: 100,
                max: 100000,
                avgTime: '1 hour'
            }
        ]
    };

    // ==========================================
    // ORDER FORM FUNCTIONALITY
    // ==========================================
    const categorySelect = document.getElementById('category');
    const serviceSelect = document.getElementById('service');
    const serviceInfo = document.getElementById('serviceInfo');
    const quantityInput = document.getElementById('quantity');
    const chargeAmount = document.getElementById('chargeAmount');
    const averageTimeEl = document.getElementById('averageTime');
    const orderForm = document.getElementById('orderForm');
    const searchInput = document.getElementById('searchServices');

    let selectedService = null;

    // Populate services based on category
    if (categorySelect && serviceSelect) {
        categorySelect.addEventListener('change', (e) => {
            const category = e.target.value;
            serviceSelect.innerHTML = '<option value="" disabled selected>Select a service</option>';
            
            if (category && servicesData[category]) {
                servicesData[category].forEach(service => {
                    const option = document.createElement('option');
                    option.value = service.id;
                    option.textContent = service.name;
                    option.dataset.price = service.price;
                    option.dataset.min = service.min;
                    option.dataset.max = service.max;
                    option.dataset.avgTime = service.avgTime;
                    serviceSelect.appendChild(option);
                });
            }
            
            resetOrderCalculation();
        });

        // Update service info and limits
        serviceSelect.addEventListener('change', (e) => {
            const option = e.target.options[e.target.selectedIndex];
            
            if (option.value) {
                selectedService = {
                    id: option.value,
                    name: option.textContent,
                    price: parseFloat(option.dataset.price),
                    min: parseInt(option.dataset.min),
                    max: parseInt(option.dataset.max),
                    avgTime: option.dataset.avgTime
                };

                // Update quantity limits
                if (quantityInput) {
                    quantityInput.min = selectedService.min;
                    quantityInput.max = selectedService.max;
                    quantityInput.placeholder = `Min: ${selectedService.min} - Max: ${selectedService.max}`;
                    
                    // Update quantity info display
                    const quantityInfo = quantityInput.parentElement.querySelector('.quantity-info');
                    if (quantityInfo) {
                        quantityInfo.innerHTML = `
                            <span>Min: <strong>${selectedService.min}</strong></span>
                            <span>Max: <strong>${selectedService.max.toLocaleString()}</strong></span>
                        `;
                    }
                }

                // Update average time
                if (averageTimeEl) {
                    averageTimeEl.textContent = selectedService.avgTime;
                }

                // Show service info
                if (serviceInfo) {
                    serviceInfo.innerHTML = `
                        <strong>Service ID:</strong> ${selectedService.id} | 
                        <strong>Price:</strong> $${selectedService.price.toFixed(4)} per 1000 | 
                        <strong>Range:</strong> ${selectedService.min} - ${selectedService.max.toLocaleString()}
                    `;
                    serviceInfo.classList.add('show');
                }

                calculateCharge();
            } else {
                resetOrderCalculation();
            }
        });
    }

    // Calculate charge based on quantity
    if (quantityInput) {
        quantityInput.addEventListener('input', calculateCharge);
    }

    function calculateCharge() {
        if (!selectedService || !quantityInput) return;
        
        const quantity = parseInt(quantityInput.value) || 0;
        
        if (quantity >= selectedService.min && quantity <= selectedService.max) {
            const charge = (quantity / 1000) * selectedService.price;
            if (chargeAmount) {
                chargeAmount.textContent = `$${charge.toFixed(2)}`;
            }
        } else if (chargeAmount) {
            chargeAmount.textContent = '$0.00';
        }
    }

    function resetOrderCalculation() {
        selectedService = null;
        if (chargeAmount) chargeAmount.textContent = '$0.00';
        if (averageTimeEl) averageTimeEl.textContent = '34 minutes';
        if (serviceInfo) {
            serviceInfo.classList.remove('show');
            serviceInfo.innerHTML = '';
        }
        if (quantityInput) {
            quantityInput.min = 100;
            quantityInput.max = 30000;
            quantityInput.placeholder = 'Min: 100 - Max: 30,000';
        }
    }

    // ==========================================
    // SEARCH FUNCTIONALITY
    // ==========================================
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            
            if (searchTerm.length < 2) {
                categorySelect.value = '';
                serviceSelect.innerHTML = '<option value="" disabled selected>Select a service</option>';
                return;
            }

            // Search across all services
            let results = [];
            Object.entries(servicesData).forEach(([category, services]) => {
                services.forEach(service => {
                    if (service.name.toLowerCase().includes(searchTerm) || 
                        service.id.includes(searchTerm)) {
                        results.push({ ...service, category });
                    }
                });
            });

            // Populate service select with results
            serviceSelect.innerHTML = '<option value="" disabled selected>Search results...</option>';
            results.forEach(service => {
                const option = document.createElement('option');
                option.value = service.id;
                option.textContent = `[${service.category.toUpperCase()}] ${service.name}`;
                option.dataset.price = service.price;
                option.dataset.min = service.min;
                option.dataset.max = service.max;
                option.dataset.avgTime = service.avgTime;
                serviceSelect.appendChild(option);
            });

            if (results.length === 0) {
                serviceSelect.innerHTML = '<option value="" disabled selected>No services found</option>';
            }
        });
    }

    // ==========================================
    // FORM SUBMISSION
    // ==========================================
    if (orderForm) {
        orderForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (!selectedService) {
                showToast('Please select a service', 'error');
                return;
            }

            const orderLink = document.getElementById('orderLink').value;
            const quantity = parseInt(quantityInput.value);

            // Validate quantity
            if (quantity < selectedService.min || quantity > selectedService.max) {
                showToast(`Quantity must be between ${selectedService.min} and ${selectedService.max}`, 'error');
                return;
            }

            // Calculate charge
            const charge = (quantity / 1000) * selectedService.price;

            // Check if user has sufficient balance
            if (parseFloat(user.balance) < charge) {
                showToast('Insufficient balance. Please add funds.', 'error');
                return;
            }

            const orderData = {
                service_id: selectedService.id,
                service_name: selectedService.name,
                link: orderLink,
                quantity: quantity,
                charge: charge
            };

            try {
                const response = await fetch('/.netlify/functions/orders', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(orderData)
                });

                const result = await response.json();

                if (response.ok) {
                    showToast('Order placed successfully!', 'success');
                    
                    // Update user balance
                    user.balance = (parseFloat(user.balance) - charge).toFixed(2);
                    localStorage.setItem('user', JSON.stringify(user));
                    updateUserDisplay();

                    // Reset form
                    orderForm.reset();
                    resetOrderCalculation();

                    // Switch to orders view after 2 seconds
                    setTimeout(() => {
                        showOrdersView();
                        loadOrders();
                    }, 2000);
                } else {
                    showToast(result.error || 'Failed to place order', 'error');
                }
            } catch (error) {
                console.error('Order submission error:', error);
                showToast('Network error. Please try again.', 'error');
            }
        });
    }

    // ==========================================
    // ORDERS VIEW
    // ==========================================
    const ordersLink = document.getElementById('ordersLink');
    const dashboardContent = document.getElementById('dashboardContent');
    const ordersView = document.getElementById('ordersView');

    function showOrdersView() {
        if (dashboardContent) dashboardContent.classList.add('hidden');
        if (ordersView) ordersView.classList.remove('hidden');
        
        // Update sidebar active state
        document.querySelectorAll('.sidebar-link').forEach(link => {
            link.classList.remove('active');
        });
        if (ordersLink) ordersLink.classList.add('active');
    }

    function showDashboardView() {
        if (ordersView) ordersView.classList.add('hidden');
        if (dashboardContent) dashboardContent.classList.remove('hidden');
        
        // Update sidebar active state
        document.querySelectorAll('.sidebar-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector('.sidebar-link[href="dashboard.html"]')?.classList.add('active');
    }

    if (ordersLink) {
        ordersLink.addEventListener('click', (e) => {
            e.preventDefault();
            showOrdersView();
            loadOrders();
        });
    }

    // Load orders from backend
    async function loadOrders() {
        const ordersTableBody = document.getElementById('ordersTableBody');
        if (!ordersTableBody) return;

        try {
            const response = await fetch('/.netlify/functions/orders', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            const result = await response.json();

            if (response.ok && result.orders) {
                displayOrders(result.orders);
            } else {
                ordersTableBody.innerHTML = `
                    <tr>
                        <td colspan="9" class="no-orders">
                            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <circle cx="12" cy="12" r="10"/>
                                <line x1="12" y1="8" x2="12" y2="12"/>
                                <line x1="12" y1="16" x2="12.01" y2="16"/>
                            </svg>
                            <p>No orders found</p>
                        </td>
                    </tr>
                `;
            }
        } catch (error) {
            console.error('Error loading orders:', error);
        }
    }

    function displayOrders(orders) {
        const ordersTableBody = document.getElementById('ordersTableBody');
        if (!ordersTableBody) return;

        if (orders.length === 0) {
            ordersTableBody.innerHTML = `
                <tr>
                    <td colspan="9" class="no-orders">
                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <circle cx="12" cy="12" r="10"/>
                            <line x1="12" y1="8" x2="12" y2="12"/>
                            <line x1="12" y1="16" x2="12.01" y2="16"/>
                        </svg>
                        <p>No orders found</p>
                    </td>
                </tr>
            `;
            return;
        }

        ordersTableBody.innerHTML = orders.map(order => `
            <tr>
                <td><strong>${order.order_number || order.id}</strong></td>
                <td>${new Date(order.created_at).toLocaleDateString()}</td>
                <td><a href="${order.link}" target="_blank" style="color: var(--primary-pink);">${order.link.substring(0, 30)}...</a></td>
                <td>$${parseFloat(order.charge).toFixed(2)}</td>
                <td>${order.start_count || 0}</td>
                <td>${order.quantity}</td>
                <td>${order.service_name.substring(0, 40)}...</td>
                <td><span class="status-badge status-${order.status}">${order.status}</span></td>
                <td>${order.remains || 0}</td>
            </tr>
        `).join('');
    }

    // Order filters
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            filterBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            const filter = e.target.dataset.filter;
            // Implement filter logic here
            console.log('Filter by:', filter);
        });
    });

    // Initialize
    updateUserDisplay();

})();
