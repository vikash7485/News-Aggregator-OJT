// Premium News Aggregator JavaScript
// Modern interactive features and animations

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all features
    initSmoothScrolling();
    // initLazyLoading(); // Disabled - using native lazy loading instead
    initCardAnimations();
    initSearchEnhancements();
    initScrollToTop();
    initAutoHideAlerts();
    initReadingTime();
    // initImageFallback(); // Disabled - using template onerror handler instead
    initTooltips();
});

/**
 * Smooth scrolling for anchor links
 */
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Lazy loading for images with fade-in effect
 * Only works with images that have data-src attribute
 */
function initLazyLoading() {
    const images = document.querySelectorAll('.card-img-top[data-src]');

    // Only process images with data-src (native lazy loading handles others)
    if (images.length === 0) {
        return; // No lazy-load images, skip
    }

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;

                // Only process if image has data-src
                if (img.dataset.src) {
                    // Add loading state
                    img.style.opacity = '0';
                    img.style.transition = 'opacity 0.5s ease-in';

                    // Load image
                    img.src = img.dataset.src;

                    img.addEventListener('load', function () {
                        img.style.opacity = '1';
                    });

                    observer.unobserve(img);
                }
            }
        });
    }, {
        rootMargin: '50px'
    });

    images.forEach(img => imageObserver.observe(img));
}

/**
 * Stagger animation for news cards on page load
 */
function initCardAnimations() {
    const cards = document.querySelectorAll('.news-card');

    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';

        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100); // Stagger delay
    });
}

/**
 * Enhanced search with live character count and suggestions
 */
function initSearchEnhancements() {
    const searchInput = document.querySelector('input[name="q"]');

    if (searchInput) {
        // Add search icon animation on focus
        searchInput.addEventListener('focus', function () {
            this.parentElement.style.transform = 'scale(1.02)';
        });

        searchInput.addEventListener('blur', function () {
            this.parentElement.style.transform = 'scale(1)';
        });

        // Add typing indicator
        let typingTimer;
        searchInput.addEventListener('input', function () {
            clearTimeout(typingTimer);

            if (this.value.length > 0) {
                this.style.borderColor = 'var(--accent-purple)';
            } else {
                this.style.borderColor = '';
            }

            typingTimer = setTimeout(() => {
                // Could add AJAX search suggestions here
            }, 500);
        });
    }
}

/**
 * Scroll to top button with smooth animation
 */
function initScrollToTop() {
    // Create scroll-to-top button
    const scrollBtn = document.createElement('button');
    scrollBtn.id = 'scrollToTop';
    scrollBtn.innerHTML = '↑';
    scrollBtn.setAttribute('aria-label', 'Scroll to top');
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        font-size: 24px;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        z-index: 1000;
    `;

    document.body.appendChild(scrollBtn);

    // Show/hide based on scroll position
    window.addEventListener('scroll', function () {
        if (window.pageYOffset > 300) {
            scrollBtn.style.opacity = '1';
            scrollBtn.style.visibility = 'visible';
        } else {
            scrollBtn.style.opacity = '0';
            scrollBtn.style.visibility = 'hidden';
        }
    });

    // Scroll to top on click
    scrollBtn.addEventListener('click', function () {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Hover effect
    scrollBtn.addEventListener('mouseenter', function () {
        this.style.transform = 'scale(1.1) translateY(-5px)';
        this.style.boxShadow = '0 8px 24px rgba(102, 126, 234, 0.4)';
    });

    scrollBtn.addEventListener('mouseleave', function () {
        this.style.transform = 'scale(1) translateY(0)';
        this.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.2)';
    });
}

/**
 * Auto-hide alerts after 5 seconds
 */
function initAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';

            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
}

/**
 * Calculate and display reading time for articles
 */
function initReadingTime() {
    const cards = document.querySelectorAll('.news-card');

    cards.forEach(card => {
        // Check if reading time already exists
        if (card.querySelector('.reading-time')) {
            return; // Skip if already added
        }

        const cardBody = card.querySelector('.card-body');
        if (!cardBody) return;

        // Get all text content from the card
        const allText = cardBody.textContent || '';
        const wordCount = allText.trim().split(/\s+/).length;
        const readingTimeMinutes = Math.ceil(wordCount / 200); // Average reading speed

        if (readingTimeMinutes > 0) {
            const readingTimeBadge = document.createElement('small');
            readingTimeBadge.className = 'text-muted reading-time';
            readingTimeBadge.innerHTML = `${readingTimeMinutes} min read`;
            readingTimeBadge.style.display = 'block';
            readingTimeBadge.style.marginTop = '0.5rem';

            cardBody.appendChild(readingTimeBadge);
        }
    });
}

/**
 * Image fallback for broken images
 */
function initImageFallback() {
    const images = document.querySelectorAll('.card-img-top');

    images.forEach(img => {
        img.addEventListener('error', function () {
            // Create a gradient placeholder
            this.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="200"%3E%3Cdefs%3E%3ClinearGradient id="grad" x1="0%25" y1="0%25" x2="100%25" y2="100%25"%3E%3Cstop offset="0%25" style="stop-color:%23667eea;stop-opacity:1" /%3E%3Cstop offset="100%25" style="stop-color:%23764ba2;stop-opacity:1" /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width="400" height="200" fill="url(%23grad)" /%3E%3Ctext x="50%25" y="50%25" font-family="Arial" font-size="20" fill="white" text-anchor="middle" dominant-baseline="middle"%3ENews Image%3C/text%3E%3C/svg%3E';
            this.style.objectFit = 'cover';
        });
    });
}

/**
 * Initialize Bootstrap tooltips if available
 */
function initTooltips() {
    // Check if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

/**
 * Add copy link functionality to share buttons
 */
function addShareFunctionality() {
    const shareButtons = document.querySelectorAll('.btn-share');

    shareButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.dataset.url || window.location.href;

            // Copy to clipboard
            navigator.clipboard.writeText(url).then(() => {
                showToast('Link copied to clipboard!', 'success');
            }).catch(err => {
                console.error('Failed to copy:', err);
            });
        });
    });
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 100px;
        right: 30px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        font-weight: 600;
        animation: slideInRight 0.3s ease;
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Add CSS animations for toasts
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    #scrollToTop:active {
        transform: scale(0.95) !important;
    }
`;
document.head.appendChild(style);

/**
 * Add keyboard shortcuts
 */
document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[name="q"]');
        if (searchInput) {
            searchInput.focus();
        }
    }

    // ESC to clear search
    if (e.key === 'Escape') {
        const searchInput = document.querySelector('input[name="q"]');
        if (searchInput && document.activeElement === searchInput) {
            searchInput.value = '';
            searchInput.blur();
        }
    }
});

/**
 * Add loading state to forms
 */
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', function () {
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
        }
    });
});

/**
 * Console greeting message
 */
console.log(
    '%c🚀 News Aggregator ',
    'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 8px 16px; border-radius: 8px; font-size: 16px; font-weight: bold;'
);
console.log(
    '%cWelcome to the News Aggregator! Built with Django + Modern JS',
    'color: #667eea; font-size: 12px;'
);
