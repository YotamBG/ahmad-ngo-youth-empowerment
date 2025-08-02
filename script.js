// ============================
// BULLETPROOF 2025 JAVASCRIPT
// COMPLETE FUNCTIONALITY & ERROR HANDLING
// ============================

(function() {
    'use strict';

    // Global error handler
    window.addEventListener('error', function(event) {
        console.error('JavaScript Error:', event.error);
        showNotification('Something went wrong. Please refresh the page.', 'error');
    });

    // Wait for DOM to be fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeApp);
    } else {
        initializeApp();
    }

    function initializeApp() {
        try {
            // Initialize all functionality with error handling
            initMobileNavigation();
            initScrollEffects();
            initSmoothScrolling();
            initAnimationObserver();
            initCounterAnimations();
            initGlowEffects();
            initFormHandling();
            initLoadingEffects();
            initAccessibility();
            
            console.log('✅ Arab Youth Leaders website initialized successfully!');
        } catch (error) {
            console.error('❌ Initialization error:', error);
            showNotification('Website loading encountered an issue. Please refresh.', 'error');
        }
    }

    // ============================
    // ENHANCED MOBILE NAVIGATION
    // ============================

    function initMobileNavigation() {
        const hamburger = document.getElementById('hamburger');
        const navMenu = document.getElementById('nav-menu');
        const body = document.body;
        
        if (!hamburger || !navMenu) {
            console.warn('Navigation elements not found');
            return;
        }

        // Toggle mobile navigation
        hamburger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleMobileNav();
        });

        // Close on navigation link click
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                closeMobileNav();
            });
        });

        // Close on outside click
        document.addEventListener('click', function(event) {
            if (navMenu.classList.contains('active') && 
                !hamburger.contains(event.target) && 
                !navMenu.contains(event.target)) {
                closeMobileNav();
            }
        });

        // Close on escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && navMenu.classList.contains('active')) {
                closeMobileNav();
            }
        });

        function toggleMobileNav() {
            const isActive = navMenu.classList.contains('active');
            
            if (isActive) {
                closeMobileNav();
            } else {
                openMobileNav();
            }
        }

        function openMobileNav() {
            navMenu.classList.add('active');
            hamburger.classList.add('active');
            body.style.overflow = 'hidden';
            
            // Focus first menu item for accessibility
            const firstLink = navMenu.querySelector('a');
            if (firstLink) {
                setTimeout(() => firstLink.focus(), 100);
            }
        }

        function closeMobileNav() {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
            body.style.overflow = '';
        }
    }

    // ============================
    // ENHANCED SCROLL EFFECTS
    // ============================

    function initScrollEffects() {
        const navbar = document.querySelector('.navbar');
        if (!navbar) return;

        let ticking = false;

        function updateScrollEffects() {
            const scrollY = window.pageYOffset;
            
            // Update navbar appearance
            if (scrollY > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            // Parallax effect for hero
            updateParallax(scrollY);
            
            ticking = false;
        }

        function updateParallax(scrollY) {
            const hero = document.querySelector('.hero');
            const heroContainer = hero?.querySelector('.hero-container');
            
            if (heroContainer && scrollY < window.innerHeight) {
                const speed = scrollY * 0.3;
                heroContainer.style.transform = `translateY(${speed}px)`;
            }
        }

        function requestScrollUpdate() {
            if (!ticking) {
                requestAnimationFrame(updateScrollEffects);
                ticking = true;
            }
        }

        // Throttled scroll listener
        window.addEventListener('scroll', requestScrollUpdate, { passive: true });
    }

    // ============================
    // BULLETPROOF SMOOTH SCROLLING
    // ============================

    function initSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                
                // Skip empty or invalid hrefs
                if (!href || href === '#') return;
                
                e.preventDefault();
                
                const targetElement = document.querySelector(href);
                if (!targetElement) {
                    console.warn(`Target element not found: ${href}`);
                    return;
                }

                // Calculate offset for fixed navbar
                const navbar = document.querySelector('.navbar');
                const navbarHeight = navbar ? navbar.offsetHeight : 80;
                const offsetTop = targetElement.offsetTop - navbarHeight - 20;

                // Smooth scroll with fallback
                smoothScrollTo(offsetTop, 1000);
                
                // Close mobile nav if open
                const navMenu = document.getElementById('nav-menu');
                if (navMenu?.classList.contains('active')) {
                    navMenu.classList.remove('active');
                    document.getElementById('hamburger')?.classList.remove('active');
                    document.body.style.overflow = '';
                }
            });
        });
    }

    function smoothScrollTo(targetPosition, duration) {
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        let startTime = null;

        function animation(currentTime) {
            if (startTime === null) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const run = easeInOutCubic(timeElapsed, startPosition, distance, duration);
            
            window.scrollTo(0, run);
            
            if (timeElapsed < duration) {
                requestAnimationFrame(animation);
            }
        }

        function easeInOutCubic(t, b, c, d) {
            t /= d / 2;
            if (t < 1) return c / 2 * t * t * t + b;
            t -= 2;
            return c / 2 * (t * t * t + 2) + b;
        }

        requestAnimationFrame(animation);
    }

    // ============================
    // ENHANCED ANIMATION OBSERVER
    // ============================

    function initAnimationObserver() {
        if (!('IntersectionObserver' in window)) {
            console.warn('IntersectionObserver not supported');
            return;
        }

        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    // Staggered animation
                    setTimeout(() => {
                        entry.target.classList.add('animate-in');
                    }, index * 100);
                    
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observe multiple element types
        const animateElements = document.querySelectorAll(`
            .overview-item, .team-member-card, .contribution-item, 
            .criteria-item, .city-item, .vision-item, .course-item,
            .semester-card, .cost-breakdown, .budget-table,
            .application-form, h2, h3, .btn-primary, .btn-secondary
        `);

        animateElements.forEach(element => {
            if (element) observer.observe(element);
        });
    }

    // ============================
    // ROBUST COUNTER ANIMATIONS
    // ============================

    function initCounterAnimations() {
        const counters = document.querySelectorAll('.stat-number, .stat-year, [data-counter]');
        
        if (counters.length === 0) return;

        const counterObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }

    function animateCounter(element) {
        const text = element.textContent.trim();
        const numbers = text.match(/\d+/g);
        
        if (!numbers || numbers.length === 0) return;

        const finalNumber = parseInt(numbers[0]);
        if (isNaN(finalNumber) || finalNumber === 0) return;

        const duration = Math.min(2000, Math.max(1000, finalNumber * 50));
        const frameDuration = 1000 / 60;
        const totalFrames = Math.round(duration / frameDuration);
        let frame = 0;

        const counter = setInterval(() => {
            frame++;
            const progress = easeOutCubic(frame / totalFrames);
            const currentNumber = Math.round(finalNumber * progress);
            
            element.textContent = text.replace(numbers[0], currentNumber.toLocaleString());
            
            if (frame >= totalFrames) {
                clearInterval(counter);
                element.textContent = text.replace(numbers[0], finalNumber.toLocaleString());
            }
        }, frameDuration);
    }

    function easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }

    // ============================
    // ENHANCED INTERACTIVE EFFECTS
    // ============================

    function initGlowEffects() {
        const glowElements = document.querySelectorAll('.btn-primary, .btn-apply, .team-member-card, .overview-item');
        
        glowElements.forEach(element => {
            element.addEventListener('mouseenter', function() {
                this.style.animation = 'glow 1.5s ease-in-out infinite alternate';
            });
            
            element.addEventListener('mouseleave', function() {
                this.style.animation = '';
            });
        });

        // Enhanced ripple effect for buttons
        const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-apply, button[type="submit"]');
        
        buttons.forEach(button => {
            button.addEventListener('click', createRipple);
        });
    }

    function createRipple(e) {
        const button = e.currentTarget;
        
        // Remove existing ripples
        const existingRipples = button.querySelectorAll('.ripple');
        existingRipples.forEach(ripple => ripple.remove());
        
        const circle = document.createElement('span');
        const diameter = Math.max(button.clientWidth, button.clientHeight);
        const radius = diameter / 2;
        
        const rect = button.getBoundingClientRect();
        circle.style.width = circle.style.height = `${diameter}px`;
        circle.style.left = `${e.clientX - rect.left - radius}px`;
        circle.style.top = `${e.clientY - rect.top - radius}px`;
        circle.classList.add('ripple');
        
        // Ripple styles
        Object.assign(circle.style, {
            position: 'absolute',
            borderRadius: '50%',
            background: 'rgba(255, 255, 255, 0.6)',
            transform: 'scale(0)',
            animation: 'ripple 600ms linear',
            pointerEvents: 'none'
        });
        
        // Ensure button positioning
        if (getComputedStyle(button).position === 'static') {
            button.style.position = 'relative';
        }
        button.style.overflow = 'hidden';
        
        button.appendChild(circle);
        
        // Auto cleanup
        setTimeout(() => {
            if (circle.parentNode) {
                circle.remove();
            }
        }, 600);
    }

    // ============================
    // BULLETPROOF FORM HANDLING
    // ============================

    function initFormHandling() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', handleFormSubmit);
            
            // Enhanced field validation
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                input.addEventListener('blur', validateField);
                input.addEventListener('input', clearFieldError);
                input.addEventListener('focus', addFocusEffect);
            });
        });
    }

    function handleFormSubmit(event) {
        event.preventDefault();
        
        const form = event.target;
        const submitButton = form.querySelector('button[type="submit"], input[type="submit"], .form-submit');
        
        if (!submitButton) {
            showNotification('Form submission error. Please try again.', 'error');
            return;
        }

        // Comprehensive validation
        if (!validateForm(form)) {
            showNotification('Please correct all errors before submitting.', 'error');
            return;
        }

        // Enhanced loading state
        const originalText = submitButton.textContent;
        const originalHTML = submitButton.innerHTML;
        
        submitButton.innerHTML = '<span>Submitting...</span>';
        submitButton.disabled = true;
        submitButton.style.opacity = '0.7';
        submitButton.style.cursor = 'not-allowed';

        // Simulate form submission with realistic delay
        setTimeout(() => {
            try {
                // Success state
                submitButton.innerHTML = '✅ Submitted Successfully!';
                submitButton.style.background = 'var(--accent-coral)';
                
                showNotification('Thank you! Your application has been received. We\'ll contact you soon.', 'success');
                
                // Reset form
                form.reset();
                clearAllFieldErrors(form);
                
                // Reset button after delay
                setTimeout(() => {
                    submitButton.innerHTML = originalHTML;
                    submitButton.textContent = originalText;
                    submitButton.disabled = false;
                    submitButton.style.opacity = '';
                    submitButton.style.cursor = '';
                    submitButton.style.background = '';
                }, 4000);
                
            } catch (error) {
                console.error('Form submission error:', error);
                showNotification('Submission failed. Please try again.', 'error');
                
                // Reset button on error
                submitButton.innerHTML = originalHTML;
                submitButton.textContent = originalText;
                submitButton.disabled = false;
                submitButton.style.opacity = '';
                submitButton.style.cursor = '';
            }
        }, 1500);
    }

    function validateForm(form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        // Clear previous errors
        clearAllFieldErrors(form);
        
        requiredFields.forEach(field => {
            if (!validateField({ target: field })) {
                isValid = false;
            }
        });
        
        return isValid;
    }

    function validateField(event) {
        const field = event.target;
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Clear previous error
        clearFieldError(event);

        // Required field validation
        if (field.hasAttribute('required') && !value) {
            errorMessage = `${getFieldLabel(field)} is required`;
            isValid = false;
        }
        // Email validation
        else if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                errorMessage = 'Please enter a valid email address';
                isValid = false;
            }
        }
        // Phone validation
        else if (field.type === 'tel' && value) {
            const phoneRegex = /^[\+]?[\s\-\(\)]*([0-9][\s\-\(\)]*){10,}$/;
            if (!phoneRegex.test(value)) {
                errorMessage = 'Please enter a valid phone number';
                isValid = false;
            }
        }
        // Text length validation
        else if (field.type === 'text' && value.length > 0 && value.length < 2) {
            errorMessage = `${getFieldLabel(field)} must be at least 2 characters`;
            isValid = false;
        }
        // Textarea validation
        else if (field.tagName.toLowerCase() === 'textarea' && value.length > 0 && value.length < 10) {
            errorMessage = 'Please provide more details (at least 10 characters)';
            isValid = false;
        }

        if (!isValid) {
            showFieldError(field, errorMessage);
        } else {
            showFieldSuccess(field);
        }

        return isValid;
    }

    function getFieldLabel(field) {
        const label = field.closest('.form-group')?.querySelector('label');
        return label ? label.textContent.replace('*', '').trim() : 'This field';
    }

    function showFieldError(field, message) {
        const formGroup = field.closest('.form-group');
        if (!formGroup) return;

        field.style.borderColor = 'var(--accent-coral)';
        field.style.boxShadow = '0 0 0 3px rgba(255, 127, 80, 0.1)';
        field.setAttribute('aria-invalid', 'true');

        let errorElement = formGroup.querySelector('.field-error');
        if (!errorElement) {
            errorElement = document.createElement('span');
            errorElement.className = 'field-error';
            errorElement.setAttribute('role', 'alert');
            errorElement.style.cssText = `
                color: var(--accent-coral);
                font-size: 0.875rem;
                margin-top: 0.5rem;
                display: block;
                font-weight: 500;
            `;
            formGroup.appendChild(errorElement);
        }
        errorElement.textContent = message;
    }

    function showFieldSuccess(field) {
        field.style.borderColor = 'var(--primary-teal)';
        field.style.boxShadow = '0 0 0 3px rgba(0, 109, 119, 0.1)';
        field.setAttribute('aria-invalid', 'false');
    }

    function clearFieldError(event) {
        const field = event.target;
        const formGroup = field.closest('.form-group');
        
        field.style.borderColor = '';
        field.style.boxShadow = '';
        field.removeAttribute('aria-invalid');
        
        const errorElement = formGroup?.querySelector('.field-error');
        if (errorElement) {
            errorElement.remove();
        }
    }

    function clearAllFieldErrors(form) {
        const errorElements = form.querySelectorAll('.field-error');
        errorElements.forEach(error => error.remove());
        
        const fields = form.querySelectorAll('input, select, textarea');
        fields.forEach(field => {
            field.style.borderColor = '';
            field.style.boxShadow = '';
            field.removeAttribute('aria-invalid');
        });
    }

    function addFocusEffect(event) {
        const field = event.target;
        field.style.transform = 'translateY(-2px)';
        field.style.transition = 'all 0.3s ease';
        
        field.addEventListener('blur', function resetTransform() {
            field.style.transform = '';
            field.removeEventListener('blur', resetTransform);
        });
    }

    // ============================
    // ENHANCED NOTIFICATION SYSTEM
    // ============================

    function showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(notification => {
            notification.remove();
        });

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.setAttribute('role', 'alert');
        notification.setAttribute('aria-live', 'polite');
        
        const colors = {
            success: 'var(--primary-teal)',
            error: 'var(--accent-coral)',
            info: 'var(--future-dusk)',
            warning: 'var(--accent-orange)'
        };

        const icons = {
            success: '✅',
            error: '❌',
            info: 'ℹ️',
            warning: '⚠️'
        };

        notification.innerHTML = `
            <span class="notification-icon">${icons[type] || icons.info}</span>
            <span class="notification-message">${message}</span>
            <button class="notification-close" aria-label="Close notification">×</button>
        `;

        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${colors[type] || colors.info};
            color: white;
            border-radius: 0.75rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            z-index: 10000;
            font-size: 0.875rem;
            font-weight: 600;
            max-width: 400px;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            cursor: pointer;
            backdrop-filter: blur(16px);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        `;

        // Close button styles
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.style.cssText = `
            background: none;
            border: none;
            color: white;
            font-size: 1.2rem;
            cursor: pointer;
            margin-left: auto;
            padding: 0;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Auto remove
        const autoRemoveTimeout = setTimeout(() => {
            removeNotification(notification);
        }, type === 'error' ? 8000 : 5000);

        // Manual close
        const removeNotification = (notif) => {
            notif.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notif.parentNode) {
                    notif.remove();
                }
            }, 300);
            clearTimeout(autoRemoveTimeout);
        };

        // Click handlers
        closeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            removeNotification(notification);
        });

        notification.addEventListener('click', () => {
            removeNotification(notification);
        });
    }

    // ============================
    // LOADING EFFECTS
    // ============================

    function initLoadingEffects() {
        const elementsToAnimate = document.querySelectorAll('h1, h2, h3, p, .btn-primary, .btn-secondary');
        
        elementsToAnimate.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, index * 50);
        });
    }

    // ============================
    // ENHANCED ACCESSIBILITY
    // ============================

    function initAccessibility() {
        // Keyboard navigation enhancement
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', function() {
            document.body.classList.remove('keyboard-navigation');
        });

        // Enhanced focus management
        const focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
        
        // Skip to main content link
        if (!document.querySelector('.skip-link')) {
            const skipLink = document.createElement('a');
            skipLink.className = 'skip-link';
            skipLink.href = '#home';
            skipLink.textContent = 'Skip to main content';
            skipLink.style.cssText = `
                position: absolute;
                top: -40px;
                left: 6px;
                background: var(--primary-teal);
                color: white;
                padding: 8px;
                text-decoration: none;
                border-radius: 4px;
                z-index: 10001;
                transition: top 0.3s;
            `;
            
            skipLink.addEventListener('focus', function() {
                this.style.top = '6px';
            });
            
            skipLink.addEventListener('blur', function() {
                this.style.top = '-40px';
            });
            
            document.body.insertBefore(skipLink, document.body.firstChild);
        }

        // Enhanced ARIA labels
        const buttons = document.querySelectorAll('button:not([aria-label])');
        buttons.forEach(button => {
            if (!button.getAttribute('aria-label') && button.textContent.trim()) {
                button.setAttribute('aria-label', button.textContent.trim());
            }
        });
    }

    // ============================
    // UTILITY FUNCTIONS
    // ============================

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    function getViewportHeight() {
        return Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
    }

    function getViewportWidth() {
        return Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
    }

    function isElementInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= getViewportHeight() &&
            rect.right <= getViewportWidth()
        );
    }

    // ============================
    // ADD MISSING CSS ANIMATIONS
    // ============================

    if (!document.querySelector('#dynamic-styles')) {
        const dynamicStyles = document.createElement('style');
        dynamicStyles.id = 'dynamic-styles';
        dynamicStyles.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
            
            @keyframes glow {
                0%, 100% {
                    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
                }
                50% {
                    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04), 0 0 20px rgba(0, 206, 209, 0.3);
                }
            }
            
            .keyboard-navigation *:focus {
                outline: 3px solid var(--primary-ocean) !important;
                outline-offset: 2px !important;
            }
            
            .animate-in {
                animation: fadeInUp 0.8s ease-out forwards;
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(40px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        `;
        document.head.appendChild(dynamicStyles);
    }

    // ============================
    // PERFORMANCE MONITORING
    // ============================

    // Monitor performance
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                if (perfData) {
                    console.log(`🚀 Page loaded in ${Math.round(perfData.loadEventEnd - perfData.loadEventStart)}ms`);
                }
            }, 0);
        });
    }

    console.log('🌊 Bulletproof Arab Youth Leaders JavaScript initialized!');

})(); 