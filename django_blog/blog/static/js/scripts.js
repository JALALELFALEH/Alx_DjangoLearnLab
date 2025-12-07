// static/js/scripts.js OR blog/static/js/scripts.js

/**
 * Django Blog - Main JavaScript File
 * Contains all client-side functionality for the blog
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Django Blog - Scripts loaded successfully');
    
    // Initialize all modules
    initializeNavigation();
    initializeMessages();
    initializeForms();
    initializeResponsiveMenu();
    
    // Performance monitoring
    logPageLoadTime();
});

// ========== MODULE: NAVIGATION ==========
function initializeNavigation() {
    console.log('Initializing navigation...');
    
    // Add active class to current page link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath && currentPath.includes(linkPath) && linkPath !== '/') {
            link.classList.add('active');
            link.style.fontWeight = 'bold';
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ========== MODULE: MESSAGE HANDLING ==========
function initializeMessages() {
    const messages = document.querySelectorAll('.alert');
    
    if (messages.length > 0) {
        console.log(`Found ${messages.length} message(s)`);
        
        // Auto-dismiss messages after 5 seconds
        messages.forEach(message => {
            setTimeout(() => {
                fadeOut(message);
            }, 5000);
            
            // Add dismiss button
            const dismissBtn = document.createElement('button');
            dismissBtn.innerHTML = '&times;';
            dismissBtn.className = 'message-dismiss';
            dismissBtn.style.cssText = `
                background: none;
                border: none;
                font-size: 1.2rem;
                cursor: pointer;
                position: absolute;
                right: 10px;
                top: 5px;
                color: inherit;
            `;
            
            message.style.position = 'relative';
            message.appendChild(dismissBtn);
            
            dismissBtn.addEventListener('click', () => {
                fadeOut(message);
            });
        });
    }
}

// ========== MODULE: FORM ENHANCEMENTS ==========
function initializeForms() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Add form validation feedback
        const inputs = form.querySelectorAll('input[required], textarea[required]');
        
        inputs.forEach(input => {
            // Add validation styling
            input.addEventListener('invalid', function(e) {
                e.preventDefault();
                this.style.borderColor = '#ef4444';
                showValidationError(this, 'This field is required');
            });
            
            input.addEventListener('input', function() {
                this.style.borderColor = '';
                removeValidationError(this);
            });
        });
        
        // Form submission loading state
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = 'Processing...';
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.7';
            }
        });
    });
}

// ========== MODULE: RESPONSIVE MENU ==========
function initializeResponsiveMenu() {
    // Create mobile menu toggle for smaller screens
    if (window.innerWidth <= 768) {
        const navbar = document.querySelector('.navbar');
        const navMenu = document.querySelector('.nav-menu');
        
        if (navbar && navMenu) {
            // Create mobile menu button
            const menuToggle = document.createElement('button');
            menuToggle.innerHTML = '☰';
            menuToggle.className = 'mobile-menu-toggle';
            menuToggle.style.cssText = `
                background: none;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                color: var(--primary-color);
                display: none;
            `;
            
            navbar.insertBefore(menuToggle, navMenu);
            
            // Toggle menu visibility
            menuToggle.addEventListener('click', () => {
                navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
            });
            
            // Show/hide based on screen size
            window.addEventListener('resize', () => {
                if (window.innerWidth > 768) {
                    navMenu.style.display = 'flex';
                    menuToggle.style.display = 'none';
                } else {
                    menuToggle.style.display = 'block';
                    navMenu.style.display = 'none';
                }
            });
            
            // Initial state
            if (window.innerWidth <= 768) {
                menuToggle.style.display = 'block';
                navMenu.style.display = 'none';
                navMenu.style.flexDirection = 'column';
                navMenu.style.gap = '1rem';
                navMenu.style.marginTop = '1rem';
            }
        }
    }
}

// ========== UTILITY FUNCTIONS ==========
function fadeOut(element) {
    element.style.transition = 'opacity 0.5s ease';
    element.style.opacity = '0';
    
    setTimeout(() => {
        element.style.display = 'none';
    }, 500);
}

function showValidationError(input, message) {
    // Remove existing error
    removeValidationError(input);
    
    // Create error element
    const error = document.createElement('div');
    error.className = 'validation-error';
    error.textContent = message;
    error.style.cssText = `
        color: #ef4444;
        font-size: 0.875rem;
        margin-top: 0.25rem;
    `;
    
    input.parentNode.appendChild(error);
}

function removeValidationError(input) {
    const existingError = input.parentNode.querySelector('.validation-error');
    if (existingError) {
        existingError.remove();
    }
}

function logPageLoadTime() {
    if (window.performance) {
        const timing = performance.getEntriesByType('navigation')[0];
        if (timing) {
            const loadTime = timing.loadEventEnd - timing.loadEventStart;
            console.log(`Page loaded in ${loadTime}ms`);
        }
    }
}

// ========== EXPORT FUNCTIONS FOR REUSE ==========
window.DjangoBlog = {
    utils: {
        fadeOut,
        showValidationError,
        removeValidationError
    },
    modules: {
        navigation: initializeNavigation,
        messages: initializeMessages,
        forms: initializeForms
    }
};