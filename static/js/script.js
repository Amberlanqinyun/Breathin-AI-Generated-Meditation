window.addEventListener('load', function() {
    const chatBubble = document.getElementById('chat-bubble');
    const chatContent = document.getElementById('chat-content');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const predefinedOptions = document.getElementById('predefined-options');

    // Toggle chat bubble expansion
    chatBubble.addEventListener('click', function(event) {
        chatContent.style.display = chatContent.style.display === 'none' ? 'block' : 'none';
        chatBubble.style.pointerEvents = 'none'; // Disable hover effect after click
    });

    // Handle predefined options click
    if (predefinedOptions) {
        predefinedOptions.addEventListener('click', function(event) {
            if (event.target.classList.contains('option-button')) {
                const message = event.target.getAttribute('data-message');
                sendMessage(message);
            }
        });
    }

    // Handle chat form submission
    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const message = chatInput.value;
        if (message.trim() !== '') {
            sendMessage(message);
            chatInput.value = '';
        }
    });

    function sendMessage(message) {
        const userMessage = document.createElement('div');
        userMessage.textContent = message;
        userMessage.classList.add('user-message');
        chatMessages.appendChild(userMessage);

        // Simulate a response from the chatbot
        setTimeout(() => {
            const botMessage = document.createElement('div');
            botMessage.textContent = 'This is a response from the chatbot.';
            botMessage.classList.add('bot-message');
            chatMessages.appendChild(botMessage);

            // Add response rating
            const responseRating = document.createElement('div');
            responseRating.classList.add('response-rating');
            responseRating.innerHTML = 'Was this helpful? <i class="fas fa-thumbs-up"></i> <i class="fas fa-thumbs-down"></i>';
            chatMessages.appendChild(responseRating);

            // Update predefined options based on response
            updatePredefinedOptions(['Option 1', 'Option 2', 'Option 3']);
        }, 1000);
    }

    function updatePredefinedOptions(suggestions) {
        predefinedOptions.innerHTML = '';
        suggestions.forEach(suggestion => {
            const button = document.createElement('button');
            button.classList.add('option-button');
            button.setAttribute('data-message', suggestion);
            button.textContent = suggestion;
            predefinedOptions.appendChild(button);
        });
    }
});