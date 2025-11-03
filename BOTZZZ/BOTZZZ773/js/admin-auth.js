// Admin Authentication Protection
// This script must be loaded FIRST on all admin pages

(function() {
    'use strict';

    // Check authentication
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    
    // No token or user - redirect to login
    if (!token || !userStr) {
        console.warn('Admin access denied: No authentication token');
        alert('Please sign in to access the admin panel');
        window.location.href = '../signin.html';
        return;
    }

    // Parse user data
    let user;
    try {
        user = JSON.parse(userStr);
    } catch (error) {
        console.error('Admin access denied: Invalid user data', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '../signin.html';
        return;
    }

    // Check if user has admin role
    if (user.role !== 'admin') {
        console.warn('Admin access denied: User is not an admin', user);
        alert('Access denied. Admin privileges required.');
        window.location.href = '../index.html';
        return;
    }

    // Verify token is still valid by checking if it's expired
    // JWT tokens have expiration, but we can do a basic check
    try {
        const tokenParts = token.split('.');
        if (tokenParts.length !== 3) {
            throw new Error('Invalid token format');
        }
        
        // Decode payload (middle part)
        const payload = JSON.parse(atob(tokenParts[1]));
        
        // Check expiration
        if (payload.exp && payload.exp * 1000 < Date.now()) {
            console.warn('Admin access denied: Token expired');
            alert('Your session has expired. Please sign in again.');
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '../signin.html';
            return;
        }
    } catch (error) {
        console.error('Admin access denied: Token validation failed', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '../signin.html';
        return;
    }

    console.log('✅ Admin authentication verified:', user.username);

    // Add logout handler when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        // Find logout button and add handler
        const logoutBtn = document.querySelector('[onclick*="logout"]');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', function(e) {
                e.preventDefault();
                if (confirm('Are you sure you want to logout?')) {
                    localStorage.removeItem('token');
                    localStorage.removeItem('user');
                    window.location.href = '../signin.html';
                }
            });
        }
    });
})();
