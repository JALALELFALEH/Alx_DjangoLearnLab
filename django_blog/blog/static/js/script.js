// Blog JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Django Blog loaded successfully!');
    
    // Add any interactive functionality here
    const readMoreLinks = document.querySelectorAll('.read-more');
    
    readMoreLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            alert('This feature is coming soon!');
        });
    });
    
    // Navigation active state
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav ul li a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.color = '#007bff';
            link.style.fontWeight = 'bold';
        }
    });
});