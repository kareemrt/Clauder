// Auto-dismiss flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', () => {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(el => {
        setTimeout(() => {
            el.style.transition = 'opacity .4s ease';
            el.style.opacity = '0';
            setTimeout(() => el.remove(), 400);
        }, 5000);
    });

    // Animate category bars on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.style.width = e.target.dataset.width + '%';
            }
        });
    }, { threshold: 0.2 });
    document.querySelectorAll('.category-bar-fill').forEach(bar => {
        const w = bar.style.width;
        bar.dataset.width = parseInt(w);
        bar.style.width = '0';
        observer.observe(bar);
    });
});
