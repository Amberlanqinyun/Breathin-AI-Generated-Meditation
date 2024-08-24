window.addEventListener('load', function() {
    // Declare elements once at the start
    const introSection = document.getElementById('intro-section');
    const landingPage = document.getElementById('landing-page');
    const startButton = document.getElementById('start-button');
    const inputPage = document.getElementById('input-page');
    const breathingOverlay = document.getElementById('breathing-overlay');
    const menuIcon = document.getElementById('hamburger-menu');
    const menuContent = document.getElementById('menu-content');
    const closeMenu = document.getElementById('close-menu');
    const userInput = document.getElementById('user-input');
    const submitButton = document.getElementById('submit-button');
    const categoryContainer = document.querySelector('.category-cards');
    
    // Intro to landing page transition
    setTimeout(() => {
        if (introSection && landingPage) {
            introSection.style.display = 'none';
            landingPage.classList.add('show');
        }
    }, 1500);

    // Landing page to input page transition
    if (startButton) {
        startButton.addEventListener('click', function(event) {
            event.preventDefault();
            if (landingPage && inputPage) {
                landingPage.style.display = 'none';
                inputPage.classList.add('show');
            }
        });
    }

    // Handle form submission and breathing overlay
    if (breathingOverlay) {
        const inputForm = document.getElementById('input-form');
        if (inputForm) {
            inputForm.onsubmit = function(event) {
                event.preventDefault();
                breathingOverlay.classList.remove('hidden');
                breathingOverlay.classList.add('fade-in');

                setTimeout(() => {
                    fetch('{{ url_for("prepare_meditation") }}', {
                        method: 'POST',
                        body: new FormData(inputForm)
                    })
                    .then(response => response.json())
                    .then(data => {
                        breathingOverlay.classList.remove('fade-in');
                        breathingOverlay.classList.add('fade-out');
                        setTimeout(() => {
                            window.location.href = "{{ url_for('start_meditation') }}?audio_file=" + data.audio_file_url;
                        }, 500);
                    })
                    .catch(error => {
                        console.error('Error generating audio:', error);
                    });
                }, 5000);
            };
        }
    }

    // Handle menu interactions
    if (menuIcon && menuContent && closeMenu) {
        menuIcon.addEventListener('click', () => menuContent.classList.add('show'));
        closeMenu.addEventListener('click', () => menuContent.classList.remove('show'));
    }

    // Handle user input validation and modal display
    if (userInput && submitButton) {
        submitButton.disabled = true; // Initially disable the submit button

        const countWords = str => str.trim().split(/\s+/).filter(Boolean).length;

        userInput.addEventListener('input', () => {
            const wordCount = countWords(userInput.value);
            submitButton.disabled = wordCount === 0;
            submitButton.classList.toggle('disabled', wordCount === 0);
        });

        const verifyUserInput = input => {
            const wordCount = countWords(input);
            return wordCount >= 3
                ? { isValid: true, message: "Thank you for sharing! Your input looks great." }
                : { isValid: false, message: "Could you add a few more words to share your thoughts?" };
        };

        const modal = document.getElementById('error-modal');
        const modalMessage = document.getElementById('modal-message');
        const modalClose = document.getElementById('modal-close');

        if (modal && modalMessage && modalClose) {
            submitButton.addEventListener('click', function(event) {
                const validationResult = verifyUserInput(userInput.value);

                if (!validationResult.isValid) {
                    event.preventDefault();
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
                setTimeout(() => modal.classList.add('hidden'), 400);
            });
        }
    }

    // Handle scrollable category cards
    if (categoryContainer) {
        categoryContainer.addEventListener('wheel', (event) => {
            event.preventDefault();
            categoryContainer.scrollBy({
                top: event.deltaY,
                behavior: 'smooth'
            });
        });
    }
});