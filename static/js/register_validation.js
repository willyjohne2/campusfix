// Registration Form Live Validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    if (!form) return;

    const nameField = document.getElementById('id_name');
    const emailField = document.getElementById('id_email');
    const password1Field = document.getElementById('id_password1');
    const password2Field = document.getElementById('id_password2');
    const submitBtn = document.getElementById('submitBtn');

    // Validation patterns
    const patterns = {
        name: {
            regex: /^[a-zA-Z\s]{2,}$/,
            message: 'Name must be at least 2 characters and contain only letters',
            minLength: 2
        },
        email: {
            regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: 'Please enter a valid email address'
        },
        password: {
            minLength: 8,
            minUppercase: 1,
            minLowercase: 1,
            minNumbers: 1,
            message: 'Password must be at least 8 characters with uppercase, lowercase, and numbers'
        }
    };

    // Add password toggle listeners
    setupPasswordToggle();

    // Add real-time validation listeners
    if (nameField) nameField.addEventListener('input', () => validateName());
    if (emailField) emailField.addEventListener('blur', () => validateEmail());
    if (password1Field) {
        password1Field.addEventListener('input', () => validatePassword());
        password1Field.addEventListener('focus', () => showPasswordRequirements());
    }
    if (password2Field) password2Field.addEventListener('input', () => validateConfirmPassword());

    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateAll()) {
            // Show loading state
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
            
            // Allow form to submit after a short delay
            setTimeout(() => {
                form.submit();
            }, 500);
        }
    });

    // Validation functions
    function validateName() {
        const value = nameField.value.trim();
        const group = nameField.closest('.form-group');
        const icon = document.getElementById('name-icon');
        const hint = document.getElementById('name-hint');

        if (value.length === 0) {
            clearFieldValidation(nameField, group, icon, hint);
            return false;
        }

        if (value.length < 2) {
            setFieldInvalid(nameField, group, icon, hint, 'Name is too short');
            return false;
        }

        if (!/^[a-zA-Z\s'-]+$/.test(value)) {
            setFieldInvalid(nameField, group, icon, hint, 'Name can only contain letters, spaces, hyphens and apostrophes');
            return false;
        }

        setFieldValid(nameField, group, icon, hint, 'Name looks good');
        return true;
    }

    function validateEmail() {
        const value = emailField.value.trim();
        const group = emailField.closest('.form-group');
        const icon = document.getElementById('email-icon');
        const hint = document.getElementById('email-hint');

        if (value.length === 0) {
            clearFieldValidation(emailField, group, icon, hint);
            return false;
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            setFieldInvalid(emailField, group, icon, hint, 'Enter a valid email address');
            return false;
        }

        // Check if email already exists (can be enhanced with AJAX)
        setFieldValid(emailField, group, icon, hint, 'Email is valid');
        return true;
    }

    function validatePassword() {
        const value = password1Field.value;
        const group = password1Field.closest('.form-group');
        const icon = document.getElementById('password1-icon');
        const hint = document.getElementById('password1-hint');

        if (value.length === 0) {
            clearFieldValidation(password1Field, group, icon, hint);
            updatePasswordStrength('', group);
            return false;
        }

        const strength = calculatePasswordStrength(value);
        updatePasswordStrength(strength.level, group, strength.text);

        if (value.length < 8) {
            setFieldInvalid(password1Field, group, icon, hint, 'Password must be at least 8 characters');
            return false;
        }

        const hasUppercase = /[A-Z]/.test(value);
        const hasLowercase = /[a-z]/.test(value);
        const hasNumbers = /[0-9]/.test(value);

        if (!hasUppercase || !hasLowercase || !hasNumbers) {
            setFieldInvalid(password1Field, group, icon, hint, 'Include uppercase, lowercase, and numbers');
            return false;
        }

        setFieldValid(password1Field, group, icon, hint, 'Password is strong');
        
        // Also validate confirm password if it has a value
        if (password2Field.value) {
            validateConfirmPassword();
        }
        
        return true;
    }

    function validateConfirmPassword() {
        const value = password2Field.value;
        const group = password2Field.closest('.form-group');
        const icon = document.getElementById('password2-icon');
        const hint = document.getElementById('password2-hint');

        if (value.length === 0) {
            clearFieldValidation(password2Field, group, icon, hint);
            return false;
        }

        if (value !== password1Field.value) {
            setFieldInvalid(password2Field, group, icon, hint, 'Passwords do not match');
            return false;
        }

        setFieldValid(password2Field, group, icon, hint, 'Passwords match');
        return true;
    }

    function calculatePasswordStrength(password) {
        let strength = 0;
        let feedback = [];

        if (password.length >= 8) strength++;
        if (password.length >= 12) strength++;
        if (/[a-z]/.test(password)) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^a-zA-Z0-9]/.test(password)) strength++;

        let level = 'weak';
        let text = 'Weak password';

        if (strength >= 5) {
            level = 'strong';
            text = 'Strong password';
        } else if (strength >= 4) {
            level = 'good';
            text = 'Good password';
        } else if (strength >= 3) {
            level = 'fair';
            text = 'Fair password';
        }

        return { level, text };
    }

    function updatePasswordStrength(level, group, text) {
        const strengthContainer = group.querySelector('.password-strength');
        const strengthBar = group.querySelector('.strength-bar');
        const strengthText = group.querySelector('.strength-text');

        if (level === '') {
            strengthContainer.classList.remove('active');
            if (strengthBar) strengthBar.className = 'strength-bar';
            if (strengthText) strengthText.textContent = '';
            return;
        }

        strengthContainer.classList.add('active');
        if (strengthBar) {
            strengthBar.className = `strength-bar ${level}`;
        }
        if (strengthText) {
            strengthText.classList.remove('weak', 'fair', 'good', 'strong');
            strengthText.classList.add('active', level);
            strengthText.textContent = text;
        }
    }

    function setFieldValid(field, group, icon, hint, message) {
        field.classList.remove('invalid');
        field.classList.add('valid');
        
        if (icon) {
            icon.classList.remove('invalid');
            icon.classList.add('valid');
            icon.textContent = '✓';
        }
        
        if (hint) {
            hint.classList.remove('error');
            hint.classList.add('active', 'success');
            hint.textContent = message;
        }
    }

    function setFieldInvalid(field, group, icon, hint, message) {
        field.classList.remove('valid');
        field.classList.add('invalid');
        
        if (icon) {
            icon.classList.remove('valid');
            icon.classList.add('invalid');
            icon.textContent = '✕';
        }
        
        if (hint) {
            hint.classList.remove('success');
            hint.classList.add('active', 'error');
            hint.textContent = message;
        }
    }

    function clearFieldValidation(field, group, icon, hint) {
        field.classList.remove('valid', 'invalid');
        
        if (icon) {
            icon.classList.remove('valid', 'invalid');
            icon.textContent = '';
        }
        
        if (hint) {
            hint.classList.remove('active', 'success', 'error');
            hint.textContent = '';
        }
    }

    function showPasswordRequirements() {
        const hint = document.getElementById('password1-hint');
        if (hint) {
            hint.classList.add('active');
            hint.textContent = 'Minimum 8 characters • Uppercase and lowercase letters • At least one number';
        }
    }

    function validateAll() {
        const nameValid = validateName();
        const emailValid = validateEmail();
        const passwordValid = validatePassword();
        const confirmPasswordValid = validateConfirmPassword();

        return nameValid && emailValid && passwordValid && confirmPasswordValid;
    }

    function setupPasswordToggle() {
        const toggleButtons = document.querySelectorAll('.toggle-password');
        
        toggleButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const inputId = this.getAttribute('data-toggle');
                const input = document.getElementById(inputId);
                
                if (input.type === 'password') {
                    input.type = 'text';
                    this.title = 'Hide password';
                } else {
                    input.type = 'password';
                    this.title = 'Show password';
                }
            });
        });
    }

    // Update submit button state based on form validity
    const allInputs = [nameField, emailField, password1Field, password2Field];
    allInputs.forEach(input => {
        if (input) {
            input.addEventListener('input', () => {
                const isFormValid = validateAll();
                submitBtn.disabled = !isFormValid;
                submitBtn.style.opacity = isFormValid ? '1' : '0.6';
            });
        }
    });
});
