// Fast Page Navigation - Prefetch links on hover
document.addEventListener('DOMContentLoaded', function() {
    // Prefetch pages when user hovers over links
    const links = document.querySelectorAll('a[href^="/"]');
    
    links.forEach(link => {
        link.addEventListener('mouseenter', function() {
            const href = this.getAttribute('href');
            if (href && !href.startsWith('#')) {
                prefetchPage(href);
            }
        });
    });
    
    function prefetchPage(url) {
        // Check if already prefetched
        if (document.querySelector(`link[rel="prefetch"][href="${url}"]`)) {
            return;
        }
        
        const prefetchLink = document.createElement('link');
        prefetchLink.rel = 'prefetch';
        prefetchLink.href = url;
        document.head.appendChild(prefetchLink);
    }
    
    // Smooth page transitions
    document.body.style.opacity = '1';
    document.body.style.transition = 'opacity 0.2s ease-in-out';
});

// Lazy load images for faster initial load
if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[data-src]');
    images.forEach(img => {
        img.src = img.dataset.src;
    });
} else {
    // Fallback for older browsers
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.3.2/lazysizes.min.js';
    document.body.appendChild(script);
}
