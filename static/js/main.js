// Calendario Italiano - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for anchor links
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

    // Add animation on scroll for cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';

                setTimeout(() => {
                    entry.target.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards for animation
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });

    // Highlight current day in calendar
    const today = new Date();
    const currentDay = today.getDate();
    const currentMonth = today.getMonth() + 1;
    const currentYear = today.getFullYear();

    document.querySelectorAll('.calendar-day .day-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href && href.includes(`/${currentYear}/${String(currentMonth).padStart(2, '0')}/${String(currentDay).padStart(2, '0')}`)) {
            link.parentElement.classList.add('today');
            link.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            link.style.color = 'white';
            link.querySelector('.day-number').style.color = 'white';
        }
    });

    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        // Left arrow - previous day/month/year
        if (e.key === 'ArrowLeft') {
            const prevLink = document.querySelector('.navigation a[href*="precedente"], .navigation a:first-child');
            if (prevLink) {
                prevLink.click();
            }
        }

        // Right arrow - next day/month/year
        if (e.key === 'ArrowRight') {
            const nextLink = document.querySelector('.navigation a[href*="successivo"], .navigation a:last-child');
            if (nextLink) {
                nextLink.click();
            }
        }

        // H key - go to home/today
        if (e.key === 'h' || e.key === 'H') {
            window.location.href = '/oggi';
        }
    });

    // Print functionality
    if (document.querySelector('.print-button')) {
        document.querySelector('.print-button').addEventListener('click', function() {
            window.print();
        });
    }

    // Share functionality (if Web Share API is available)
    if (navigator.share && document.querySelector('.share-button')) {
        document.querySelector('.share-button').addEventListener('click', async function() {
            try {
                await navigator.share({
                    title: document.title,
                    text: document.querySelector('meta[name="description"]')?.content,
                    url: window.location.href
                });
            } catch (err) {
                console.log('Error sharing:', err);
            }
        });
    }

    // Add tooltips
    document.querySelectorAll('[title]').forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('title');
            tooltip.style.cssText = `
                position: absolute;
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 4px;
                font-size: 0.875rem;
                z-index: 1000;
                pointer-events: none;
            `;
            document.body.appendChild(tooltip);

            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + window.scrollY + 'px';

            this._tooltip = tooltip;
        });

        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                delete this._tooltip;
            }
        });
    });

    // Console Easter Egg
    console.log('%c📅 Calendario Italiano', 'font-size: 24px; font-weight: bold; color: #2563eb;');
    console.log('%cBenvenuto nel calendario più completo d\'Italia! 🇮🇹', 'font-size: 14px; color: #7c3aed;');
    console.log('%cScopri santi, feste, fasi lunari e molto altro...', 'font-size: 12px; color: #6b7280;');
});

// Service Worker registration for PWA (optional, can be expanded)
if ('serviceWorker' in navigator) {
    // Uncomment to enable service worker
    // navigator.serviceWorker.register('/sw.js').catch(err => console.log('SW registration failed'));
}
