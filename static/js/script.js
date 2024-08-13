// Optimize transition effects and event handling
window.addEventListener('load', function() {
    // Transition from intro to landing page after 1.5 seconds
    setTimeout(() => {
        const introSection = document.getElementById('intro-section');
        const landingPage = document.getElementById('landing-page');

        if (introSection && landingPage) {
            introSection.style.display = 'none';
            landingPage.classList.add('show');
        }
    }, 1500);

    // Transition from landing page to input page
    const startButton = document.getElementById('start-button');
    if (startButton) {
        startButton.addEventListener('click', function(event) {
            event.preventDefault();
            const landingPage = document.getElementById('landing-page');
            const inputPage = document.getElementById('input-page');

            if (landingPage && inputPage) {
                landingPage.style.display = 'none';
                inputPage.classList.add('show');
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const menuIcon = document.getElementById('menu-icon');
    const menuContent = document.getElementById('menu-content');
    const closeMenu = document.getElementById('close-menu');

    // Handle menu icon interactions
    if (menuIcon && menuContent && closeMenu) {
        menuIcon.addEventListener('click', () => menuContent.classList.add('show'));
        closeMenu.addEventListener('click', () => menuContent.classList.remove('show'));
    }

    const userInput = document.getElementById('user-input');
    const submitButton = document.getElementById('submit-button');

    if (userInput && submitButton) {
        submitButton.disabled = true; // Initially disable the submit button

        // Function to count words efficiently
        const countWords = str => str.trim().split(/\s+/).filter(Boolean).length;

        // Enable or disable the submit button based on input
        userInput.addEventListener('input', () => {
            const wordCount = countWords(userInput.value);
            submitButton.disabled = wordCount === 0;
            submitButton.classList.toggle('disabled', wordCount === 0);
        });

        const verifyUserInput = userInput => {
            const wordCount = countWords(userInput);
            return wordCount >= 3
                ? { isValid: true, message: "Thank you for sharing! Your input looks great." }
                : { isValid: false, message: "Could you add a few more words to share your thoughts?" };
        };

        const modal = document.getElementById('error-modal');
        const modalMessage = document.getElementById('modal-message');
        const modalClose = document.getElementById('modal-close');

        if (modal && modalMessage && modalClose) {
            submitButton.addEventListener('click', function(event) {
                const userInputText = userInput.value;
                const validationResult = verifyUserInput(userInputText);

                if (!validationResult.isValid) {
                    event.preventDefault();

                    // Position the modal under the submit button
                    const submitButtonRect = submitButton.getBoundingClientRect();
                    modal.style.top = `${submitButtonRect.bottom + window.scrollY}px`;
                    modalMessage.textContent = validationResult.message;

                    modal.classList.remove('hidden');
                    setTimeout(() => modal.classList.add('show'), 10);

                    submitButton.disabled = true;
                    submitButton.classList.add('disabled');
                }
            });

            modalClose.addEventListener('click', () => {
                modal.classList.remove('show');
                setTimeout(() => modal.classList.add('hidden'), 400); // Match the transition duration
            });
        }
    }
});
