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
    const chatBubble = document.getElementById('chat-bubble');
    const chatContent = document.getElementById('chat-content');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const predefinedOptions = document.getElementById('predefined-options');
    const homepageUrl = "/";
    const meditationID = 7;
    const meditationPage = document.getElementById('meditation-page');
    const meditationAudio = document.getElementById(`meditation-audio-${meditationID}`);
    const skipFeedbackModal = document.getElementById('skipFeedbackModal');
    const feedbackFormModal = document.getElementById('feedbackFormModal');
    const thankYouModal = document.getElementById('thankYouModal');
    const yesButton = document.getElementById('yes-button');
    const noButton = document.getElementById('no-button');
    const closeFeedbackButton = document.getElementById('close-feedback');
    const closeThankYouButton = document.getElementById('close-thank-you');
    const feedbackForm = document.getElementById('feedback-form');
    const stars = document.querySelectorAll('.star');
    const ratingValue = document.getElementById('rating-value');
    const loginNote = document.getElementById('login-note');

    let isAudioPausedByUser = false;

    console.log('Meditation page:', meditationPage);
    console.log('Skip feedback modal:', skipFeedbackModal);

    function showModal(modal) {
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('show');
        } else {
            console.warn('Modal element not found to show:', modal);
        }
    }

    function hideModal(modal) {
        if (modal) {
            modal.classList.remove('show');
            modal.classList.add('hidden');
        } else {
            console.warn('Modal element not found to hide:', modal);
        }
    }

    // Attach event listener to the whole page to trigger the modal
    if (meditationPage) {
        meditationPage.addEventListener('click', function(event) {
            console.log('Meditation page clicked');
            if (meditationAudio && !meditationAudio.paused) {
                meditationAudio.pause();
                isAudioPausedByUser = true;
                console.log('Audio paused');
            }
            if (skipFeedbackModal) {
                showModal(skipFeedbackModal);
            } else {
                console.warn('Skip feedback modal not found');
            }
        });
    }

    if (yesButton) {
        yesButton.addEventListener('click', function() {
            console.log('Yes button clicked');
            hideModal(skipFeedbackModal);
            showModal(feedbackFormModal);
        });
    }

    if (noButton) {
        noButton.addEventListener('click', function() {
            console.log('No button clicked');
            hideModal(skipFeedbackModal);
            // Refresh the page to restart audio
            location.reload();
        });
    }

    if (closeFeedbackButton) {
        closeFeedbackButton.addEventListener('click', function() {
            console.log('Close feedback button clicked');
            hideModal(feedbackFormModal);
            window.location.href = homepageUrl; // Redirect to homepage on close
        });
    }

    if (closeThankYouButton) {
        closeThankYouButton.addEventListener('click', function() {
            console.log('Close thank you button clicked');
            hideModal(thankYouModal);
            window.location.href = homepageUrl;
        });
    }

    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log("Feedback submitted:", {
                rating: feedbackForm.rating.value,
                comments: feedbackForm.comments.value
            });

            fetch("/submit_feedback", {
                method: 'POST',
                body: new FormData(feedbackForm)
            }).then(response => response.json())
              .then(data => {
                  if (data.message) {
                      console.log('Feedback successfully submitted:', data);
                      hideModal(feedbackFormModal);
                      showModal(thankYouModal);
                  } else if (data.error) {
                      console.error('Error submitting feedback:', data.error);
                      alert(data.error);
                  }
              })
              .catch(error => console.error('Error submitting feedback:', error));
        });
    }

    // Toggle chat bubble expansion
    if (chatBubble && chatContent) {
        chatBubble.addEventListener('click', function(event) {
            event.stopPropagation(); // Prevent event from bubbling up
            chatContent.style.display = chatContent.style.display === 'none' || chatContent.style.display === '' ? 'block' : 'none';
        });

        // Close chat when clicking outside
        document.addEventListener('click', function(event) {
            if (chatContent.style.display === 'block' && !chatContent.contains(event.target) && event.target !== chatBubble) {
                chatContent.style.display = 'none';
            }
        });
    }

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

    // Handle predefined options click
    if (predefinedOptions) {
        predefinedOptions.addEventListener('click', function(event) {
            if (event.target.classList.contains('option-button')) {
                const action = event.target.dataset.action;
                switch (action) {
                    case 'helpline':
                        sendMessage("Please provide me with the NZ helpline number.");
                        break;
                    case 'therapist':
                        sendMessage("Can you help me find a therapist near me?");
                        break;
                    case 'chat':
                        sendMessage("I'd like to chat about how I'm feeling.");
                        break;
                }
            }
        });
    }

    // Handle chat form submission
    if (chatForm && chatInput && chatMessages) {
        chatForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const message = chatInput.value.trim();
            if (message !== '') {
                sendMessage(message);
                chatInput.value = '';
            }
        });
    }

    // Handle menu interactions
    if (menuIcon && menuContent && closeMenu) {
        menuIcon.addEventListener('click', function() {
            menuContent.classList.toggle('show');
        });

        closeMenu.addEventListener('click', function() {
            menuContent.classList.remove('show');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!menuIcon.contains(event.target) && !menuContent.contains(event.target)) {
                menuContent.classList.remove('show');
            }
        });
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

    function sendMessage(message) {
        if (!chatMessages) return; // Guard clause

        const userMessage = document.createElement('div');
        userMessage.textContent = message;
        userMessage.classList.add('user-message');
        chatMessages.appendChild(userMessage);

        // Send message to server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            const botMessage = document.createElement('div');
            botMessage.textContent = data.response;
            botMessage.classList.add('bot-message');
            chatMessages.appendChild(botMessage);

            // Update predefined options
            updatePredefinedOptions(data.suggestions);
        })
        .catch(error => {
            console.error('Error:', error);
            const errorMessage = document.createElement('div');
            errorMessage.textContent = 'Sorry, there was an error processing your request.';
            errorMessage.classList.add('bot-message', 'error-message');
            chatMessages.appendChild(errorMessage);
        });

        // Scroll to bottom of chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    function updatePredefinedOptions(suggestions) {
        if (!predefinedOptions) return; // Guard clause

        // Keep the original buttons
        const originalButtons = predefinedOptions.innerHTML;
        
        // Add new suggestions
        suggestions.forEach(suggestion => {
            const button = document.createElement('button');
            button.classList.add('option-button');
            button.textContent = suggestion;
            button.addEventListener('click', () => sendMessage(suggestion));
            predefinedOptions.appendChild(button);
        });
        
        // Remove suggestions after a delay
        setTimeout(() => {
            predefinedOptions.innerHTML = originalButtons;
        }, 30000); // Remove after 30 seconds
    }

    document.addEventListener('DOMContentLoaded', function() {
        const chatHeader = document.getElementById('chat-header');

        chatBubble.addEventListener('click', toggleChat);
        chatHeader.querySelector('.close-chat').addEventListener('click', toggleChat);

        function toggleChat() {
            chatContent.style.display = chatContent.style.display === 'none' || chatContent.style.display === '' ? 'block' : 'none';
        }

        predefinedOptions.addEventListener('click', function(event) {
            if (event.target.classList.contains('option-button')) {
                const message = event.target.textContent;
                sendMessage(message);
            }
        });

        chatForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const message = chatInput.value.trim();
            if (message) {
                sendMessage(message);
                chatInput.value = '';
            }
        });

        // Make the chat box draggable
        let isDragging = false;
        let startX, startY, startWidth, startHeight;

        chatHeader.addEventListener('mousedown', function(e) {
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            startWidth = parseInt(document.defaultView.getComputedStyle(chatContent).width, 10);
            startHeight = parseInt(document.defaultView.getComputedStyle(chatContent).height, 10);
            document.documentElement.addEventListener('mousemove', doDrag, false);
            document.documentElement.addEventListener('mouseup', stopDrag, false);
        });

        function doDrag(e) {
            if (isDragging) {
                chatContent.style.width = (startWidth + e.clientX - startX) + 'px';
                chatContent.style.height = (startHeight + e.clientY - startY) + 'px';
            }
        }

        function stopDrag(e) {
            isDragging = false;
            document.documentElement.removeEventListener('mousemove', doDrag, false);
            document.documentElement.removeEventListener('mouseup', stopDrag, false);
        }
    });
});