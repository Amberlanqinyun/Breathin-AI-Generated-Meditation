window.addEventListener('load', function() {
    // Transition from intro to landing page after 1.5 seconds
    setTimeout(function() {
        const introSection = document.getElementById('intro-section');
        const landingPage = document.getElementById('landing-page');

        // Hide the intro section
        introSection.style.display = 'none';

        // Show the landing page content with a fade-in effect
        landingPage.classList.add('show');
    }, 1500); // Adjust the timing based on the length of your GIF

    // Transition from landing page to input page
    const startButton = document.getElementById('start-button');
    startButton.addEventListener('click', function(event) {
        event.preventDefault();
        const landingPage = document.getElementById('landing-page');
        const inputPage = document.getElementById('input-page');

        landingPage.style.display = 'none';
        inputPage.classList.add('show');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const menuIcon = document.getElementById('menu-icon');
    const menuContent = document.getElementById('menu-content');
    const closeMenu = document.getElementById('close-menu');

    menuIcon.addEventListener('click', function() {
        menuContent.classList.add('show');
    });

    closeMenu.addEventListener('click', function() {
        menuContent.classList.remove('show');
    });

    // Get references to the textarea and the submit button
    const userInput = document.getElementById('user-input');
    const submitButton = document.getElementById('submit-button');
    const feedbackMessage = document.getElementById('feedback-message');

    // Initially hide the submit button
    submitButton.classList.add('hidden');

    // Add an event listener to monitor input changes
    userInput.addEventListener('input', function() {
        const inputLength = userInput.value.trim().length;
        if (inputLength > 0) {
            submitButton.classList.remove('hidden');
        } else {
            submitButton.classList.add('hidden');
        }
    });

    // Simplified validation function
    function verifyUserInput(userInput) {
        const minLength = 10;
        const maxLength = 300;

        if (userInput.length < minLength) {
            return {
                isValid: false,
                message: "Could you add a few more words to share your thoughts?"
            };
        } else if (userInput.length > maxLength) {
            return {
                isValid: false,
                message: `Your input is quite detailed! Could you try summarizing it to under ${maxLength} characters?`
            };
        }

        return {
            isValid: true,
            message: "Thank you for sharing! Your input looks great."
        };
    }

    // Event listener for the submit button
    submitButton.addEventListener('click', function(event) {
        const userInputText = userInput.value;
        const validationResult = verifyUserInput(userInputText);

        if (!validationResult.isValid) {
            event.preventDefault();
            feedbackMessage.textContent = validationResult.message;
            feedbackMessage.classList.remove('hidden');
            submitButton.classList.add('disabled');
            submitButton.setAttribute('disabled', 'true');
        } else {
            feedbackMessage.textContent = '';
            feedbackMessage.classList.add('hidden');
            submitButton.classList.remove('disabled');
            submitButton.removeAttribute('disabled');
            // Proceed with form submission or additional logic
        }
    });

    // Re-enable the button if the user changes the input to a valid state
    userInput.addEventListener('input', function() {
        const userInputText = userInput.value;
        const validationResult = verifyUserInput(userInputText);

        if (validationResult.isValid) {
            feedbackMessage.textContent = '';
            feedbackMessage.classList.add('hidden');
            submitButton.classList.remove('disabled');
            submitButton.removeAttribute('disabled');
        } else {
            submitButton.classList.add('disabled');
            submitButton.setAttribute('disabled', 'true');
        }
    });
});
