// RTD Transit Tracker - Main JavaScript

// Utility functions
function formatTime(timestamp) {
    return new Date(timestamp * 1000).toLocaleTimeString();
}

function formatDistance(meters) {
    const miles = meters * 0.000621371;
    return miles.toFixed(2) + ' mi';
}

function formatSpeed(metersPerSecond) {
    if (!metersPerSecond) return '-';
    const mph = metersPerSecond * 2.23694;
    return mph.toFixed(1) + ' mph';
}

// Highlight current page in navigation
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.color = 'var(--primary-color)';
            link.style.fontWeight = 'bold';
        }
    });
});

// Console info
console.log('%cRTD Transit Tracker', 'font-size: 24px; font-weight: bold; color: #2563eb;');
console.log('Built with ❤️ for the Denver community');
console.log('GitHub: https://github.com/cargarn1/RTD');

