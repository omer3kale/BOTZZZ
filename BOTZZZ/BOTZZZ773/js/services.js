// ==========================================
// Services Page JavaScript
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
    // Service Filter
    const filterButtons = document.querySelectorAll('.filter-btn');
    const serviceCategories = document.querySelectorAll('.service-category');
    const searchInput = document.getElementById('serviceSearch');
    
    // Filter by category
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.dataset.filter;
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filter categories
            serviceCategories.forEach(category => {
                if (filter === 'all') {
                    category.style.display = 'block';
                } else {
                    if (category.dataset.category === filter) {
                        category.style.display = 'block';
                    } else {
                        category.style.display = 'none';
                    }
                }
            });
            
            // Animate appearance
            setTimeout(() => {
                const visibleCategories = Array.from(serviceCategories)
                    .filter(cat => cat.style.display !== 'none');
                visibleCategories.forEach((cat, index) => {
                    cat.style.animation = 'none';
                    setTimeout(() => {
                        cat.style.animation = 'fadeInUp 0.5s ease';
                    }, index * 100);
                });
            }, 100);
        });
    });
    
    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            serviceCategories.forEach(category => {
                const categoryTitle = category.querySelector('.category-title').textContent.toLowerCase();
                const subcategories = category.querySelectorAll('.service-subcategory');
                let hasVisibleSubcategory = false;
                
                subcategories.forEach(subcategory => {
                    const subcategoryTitle = subcategory.querySelector('.subcategory-title').textContent.toLowerCase();
                    const rows = subcategory.querySelectorAll('.service-row:not(.service-row-header)');
                    let hasVisibleRow = false;
                    
                    rows.forEach(row => {
                        const serviceName = row.querySelector('strong')?.textContent.toLowerCase() || '';
                        const serviceDetails = row.querySelector('.service-details')?.textContent.toLowerCase() || '';
                        
                        if (serviceName.includes(searchTerm) || 
                            serviceDetails.includes(searchTerm) ||
                            categoryTitle.includes(searchTerm) ||
                            subcategoryTitle.includes(searchTerm)) {
                            row.style.display = 'grid';
                            hasVisibleRow = true;
                        } else {
                            row.style.display = 'none';
                        }
                    });
                    
                    if (hasVisibleRow || subcategoryTitle.includes(searchTerm)) {
                        subcategory.style.display = 'block';
                        hasVisibleSubcategory = true;
                    } else {
                        subcategory.style.display = 'none';
                    }
                });
                
                if (hasVisibleSubcategory || categoryTitle.includes(searchTerm)) {
                    category.style.display = 'block';
                } else {
                    category.style.display = 'none';
                }
            });
        });
    }
    
    // Smooth scroll to category from hash
    if (window.location.hash) {
        setTimeout(() => {
            const target = document.querySelector(window.location.hash);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }, 100);
    }
    
    // Highlight matching text in search
    function highlightText(text, search) {
        if (!search) return text;
        const regex = new RegExp(`(${search})`, 'gi');
        return text.replace(regex, '<mark style="background: rgba(255,20,148,0.3); color: #FF1494;">$1</mark>');
    }
});

// Add fade in animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

console.log('📱 Services page loaded!');
