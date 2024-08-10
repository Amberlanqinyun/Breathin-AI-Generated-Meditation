window.addEventListener('load', function() {
    // Wait for 2 seconds before transitioning from the intro to the landing page
    setTimeout(function() {
        const introSection = document.getElementById('intro-section');
        const landingPage = document.getElementById('landing-page');

        // Hide the intro section
        introSection.style.display = 'none';

        // Show the landing page content with a fade-in effect
        landingPage.classList.add('show');
    }, 1500); // Adjust the timing based on the length of your GIF

    // Add event listener to the "Get Started" button
    const startButton = document.getElementById('start-button');
    startButton.addEventListener('click', function(event) {
        event.preventDefault();
        const landingPage = document.getElementById('landing-page');
        const inputPage = document.getElementById('input-page');

        // Transition from landing page to input page
        landingPage.style.display = 'none';
        inputPage.classList.add('show');
    });

    // Add event listener to the "Submit" button (Optional functionality)
    const submitButton = document.getElementById('submit-button');
    submitButton.addEventListener('click', function(event) {
        event.preventDefault();
        const userInput = document.getElementById('user-input').value;
        console.log("User Input:", userInput);
        // Add your code here to handle the submitted input, e.g., send to a server or display on another page.
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
});
// Get references to the textarea and the submit button
const userInput = document.getElementById('user-input');
const submitButton = document.getElementById('submit-button');

// Add an event listener to monitor input changes
userInput.addEventListener('input', function() {
    // Check if there is any input
    if (userInput.value.trim().length > 0) {
        // Show the submit button
        submitButton.classList.remove('hidden');
    } else {
        // Hide the submit button if the textarea is empty
        submitButton.classList.add('hidden');
    }
});
