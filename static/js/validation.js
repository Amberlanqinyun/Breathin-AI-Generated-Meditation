document.addEventListener('DOMContentLoaded', function() {

    // Function to validate email fields
    function validateEmail(email) {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email.trim());
    }

    // Function to validate password fields
    function validatePassword(password, confirmPassword) {
        const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,20}$/;
        if (!passwordRegex.test(password)) {
            return { isValid: false, message: "Password must contain at least 1 letter, 1 number, and be 6-20 characters long." };
        }
        if (password !== confirmPassword) {
            return { isValid: false, message: "Passwords do not match." };
        }
        return { isValid: true, message: "" };
    }

    // Universal function to validate all fields and enable/disable the submit button
    function validateForm(fields) {
        let isFormValid = true;

        fields.forEach(field => {
            const { element, validator, errorField } = field;
            const value = element.value.trim();

            const validationResult = validator(value);
            if (!validationResult.isValid) {
                element.classList.add('is-invalid');
                errorField.textContent = validationResult.message;
                isFormValid = false;
            } else {
                element.classList.remove('is-invalid');
                element.classList.add('is-valid');
                errorField.textContent = "";
            }
        });

        return isFormValid;
    }

    const forms = document.querySelectorAll('form.needs-validation');
    forms.forEach(form => {
        const submitButton = form.querySelector('button[type="submit"]');
        const emailField = form.querySelector('#email');
        const passwordField = form.querySelector('#new_password');
        const confirmPasswordField = form.querySelector('#new_password_confirm');
        const emailError = form.querySelector('#email-invalid-feedback');
        const passwordError = form.querySelector('#password-feedback');
        const confirmPasswordError = form.querySelector('#confirm_password_feedback');

        if (emailField && passwordField && confirmPasswordField && submitButton) {
            submitButton.disabled = true; // Initially disable the submit button

            const fieldsToValidate = [
                { element: emailField, validator: validateEmail, errorField: emailError },
                { element: passwordField, validator: password => validatePassword(password, confirmPasswordField.value).isValid, errorField: passwordError },
                { element: confirmPasswordField, validator: confirmPassword => validatePassword(passwordField.value, confirmPassword).isValid, errorField: confirmPasswordError }
            ];

            form.addEventListener('input', () => {
                const isFormValid = validateForm(fieldsToValidate);
                submitButton.disabled = !isFormValid;
                submitButton.classList.toggle('disabled', !isFormValid);
            });
        }
    });

});
