// Auto-dismiss messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.error-alert, .success-message');
    
    messages.forEach(function(message) {
        // Add dismiss button
        const dismissBtn = document.createElement('button');
        dismissBtn.type = 'button';
        dismissBtn.className = 'dismiss-btn';
        dismissBtn.innerHTML = '&times;';
        dismissBtn.onclick = function() {
            message.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(function() {
                message.remove();
            }, 300);
        };
        message.appendChild(dismissBtn);
        
        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            if (message && message.parentNode) {
                message.style.animation = 'fadeOut 0.3s ease-out';
                setTimeout(function() {
                    if (message && message.parentNode) {
                        message.remove();
                    }
                }, 300);
            }
        }, 5000);
    });
});

// Password toggle visibility - compatible with old and new implementation
function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    // Find the button (works with both onclick and data-toggle)
    let toggleBtn = document.querySelector(`[onclick*="${inputId}"]`);
    if (!toggleBtn) {
        toggleBtn = document.querySelector(`[data-toggle="${inputId}"]`);
    }
    
    if (input.type === 'password') {
        input.type = 'text';
        if (toggleBtn) {
            toggleBtn.title = 'Hide password';
            toggleBtn.classList.add('password-visible');
        }
    } else {
        input.type = 'password';
        if (toggleBtn) {
            toggleBtn.title = 'Show password';
            toggleBtn.classList.remove('password-visible');
        }
    }
}

