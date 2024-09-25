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
        const chatBubble = document.getElementById('chat-bubble');
        const chatHeader = document.getElementById('chat-header');
        const chatContent = document.getElementById('chat-content');
        const chatForm = document.getElementById('chat-form');
        const chatInput = document.getElementById('chat-input');
        const chatMessages = document.getElementById('chat-messages');
        const predefinedOptions = document.getElementById('predefined-options');

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