/**
 * Main Application Scripts
 * Handles hamburger menu, image modals, and other interactive elements
 */

document.addEventListener('DOMContentLoaded', function() {
    // Page visibility - fade in when ready
    document.body.style.opacity = '1';
    document.body.style.transition = 'opacity 0.3s ease-in-out';

    // ===== HAMBURGER MENU =====
    const hamburgerBtn = document.getElementById("hamburger-btn");
    const overlay = document.getElementById("mobile-menu-overlay");
    const closeBtn = document.getElementById("close-menu-btn");
    
    if (hamburgerBtn && overlay) {
        hamburgerBtn.addEventListener("click", (e) => {
            e.preventDefault();
            overlay.classList.add("active");
            document.body.style.overflow = 'hidden';
        });
    }
    
    if (closeBtn && overlay) {
        closeBtn.addEventListener("click", () => {
            overlay.classList.remove("active");
            document.body.style.overflow = '';
        });
    }
    
    if (overlay) {
        overlay.addEventListener("click", (e) => {
            if(e.target === overlay){
                overlay.classList.remove("active");
                document.body.style.overflow = '';
            }
        });
    }

    // ===== IMAGE MODAL (Home Page) =====
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const closeModalBtn = document.querySelector('.modal-close');
    const issueImages = document.querySelectorAll('.issue-image');

    if (modal && modalImage) {
        // Open modal on image click
        issueImages.forEach(container => {
            container.addEventListener('click', function() {
                const img = this.querySelector('img');
                if (img) {
                    modalImage.src = img.src;
                    modal.style.display = 'flex';
                    document.body.style.overflow = 'hidden';
                }
            });
        });

        // Close modal functions
        const closeModal = function() {
            modal.style.display = 'none';
            document.body.style.overflow = '';
        };

        if (closeModalBtn) {
            closeModalBtn.addEventListener('click', closeModal);
        }

        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && modal.style.display === 'flex') {
                closeModal();
            }
        });
    }

    // ===== PASSWORD VISIBILITY TOGGLE =====
    const toggleButtons = document.querySelectorAll('.toggle-password, .password-toggle');
    toggleButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const inputId = this.getAttribute('onclick') ? 
                this.getAttribute('onclick').match(/'([^']+)'/)[1] : 
                this.previousElementSibling?.id;
            
            if (inputId) {
                const input = document.getElementById(inputId);
                if (input) {
                    if (input.type === 'password') {
                        input.type = 'text';
                        this.title = 'Hide password';
                    } else {
                        input.type = 'password';
                        this.title = 'Show password';
                    }
                }
            }
        });
    });

    // ===== PASSWORD RESET VALIDATION =====
    const newPasswordInput = document.getElementById('new_password') || document.getElementById('id_new_password1');
    const confirmPasswordInput = document.getElementById('confirm_password') || document.getElementById('id_new_password2');
    const passwordMatchStatus = document.getElementById('passwordMatchStatus');
    const submitBtn = document.querySelector('button[type="submit"]');

    if (newPasswordInput) {
        newPasswordInput.addEventListener('input', function() {
            const pwd = this.value;
            
            // Update requirement indicators
            const requirements = [
                { id: 'req-length', test: pwd.length >= 8 },
                { id: 'req-upper', test: /[A-Z]/.test(pwd) },
                { id: 'req-lower', test: /[a-z]/.test(pwd) },
                { id: 'req-number', test: /[0-9]/.test(pwd) }
            ];

            requirements.forEach(req => {
                const element = document.getElementById(req.id);
                if (element) {
                    if (req.test) {
                        element.classList.add('met');
                        element.classList.remove('unmet');
                    } else {
                        element.classList.add('unmet');
                        element.classList.remove('met');
                    }
                }
            });

            // Check password match
            checkPasswordMatch();
        });
    }

    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', checkPasswordMatch);
    }

    function checkPasswordMatch() {
        if (!newPasswordInput || !confirmPasswordInput || !passwordMatchStatus) return;

        if (newPasswordInput.value && confirmPasswordInput.value) {
            if (newPasswordInput.value === confirmPasswordInput.value) {
                passwordMatchStatus.innerHTML = '<span style="color: #10b981; font-size: 0.9rem;">✓ Passwords match</span>';
                if (submitBtn) submitBtn.disabled = false;
            } else {
                passwordMatchStatus.innerHTML = '<span style="color: #ef4444; font-size: 0.9rem;">✗ Passwords do not match</span>';
                if (submitBtn) submitBtn.disabled = true;
            }
        } else {
            passwordMatchStatus.innerHTML = '';
        }
    }
});
