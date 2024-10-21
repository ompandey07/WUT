  // Global function to close the modal
  function closeModal() {
    const errorModal = document.getElementById('errorModal');
    errorModal.classList.remove('show');
}

document.addEventListener('DOMContentLoaded', function() {
    const preloader = document.getElementById('preloader');
    const mainContent = document.getElementById('mainContent');
    const form = document.getElementById('loginForm');
    const loginButton = document.getElementById('loginButton');
    const loginText = document.getElementById('loginText');
    const loginSpinner = document.getElementById('loginSpinner');

    // Show preloader
    preloader.style.display = 'flex';
    mainContent.style.display = 'none';

    // Hide preloader and show main content after 3 seconds
    setTimeout(() => {
        preloader.style.display = 'none';
        mainContent.style.display = 'flex';
        document.body.classList.add('bg-gray-100');
        
        // Trigger the zig-zag animation
        setTimeout(() => {
            mainContent.classList.add('animate-zigzag');
            mainContent.style.opacity = '1';
        }, 100);
    }, 3000);

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);

        // Show spinner and hide text
        loginText.classList.add('hidden');
        loginSpinner.classList.remove('hidden');
        loginButton.disabled = true;

        const startTime = Date.now();

        fetch('', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            const elapsedTime = Date.now() - startTime;
            const remainingTime = Math.max(0, 2000 - elapsedTime);

            setTimeout(() => {
                if (data.status === 'success') {
                    window.location.href = data.redirect;
                } else {
                    showModal(data.message || 'An error occurred');
                    resetButton();
                }
            }, remainingTime);
        })
        .catch(error => {
            console.error('Error:', error);
            setTimeout(() => {
                showModal('An error occurred. Please try again.');
                resetButton();
            }, 2000 - (Date.now() - startTime));
        });
    });

    function resetButton() {
        loginText.classList.remove('hidden');
        loginSpinner.classList.add('hidden');
        loginButton.disabled = false;
    }

    function showModal(message) {
        const errorModal = document.getElementById('errorModal');
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.textContent = message;
        errorModal.classList.add('show');
        setTimeout(() => closeModal(), 5000); // Auto close after 5 seconds
    }

    // Check for Django messages and display them
    const djangoMessages = document.querySelectorAll('.django-message');
    djangoMessages.forEach(message => {
        showModal(message.textContent);
        message.remove(); // Remove the message from the DOM after displaying
    });
});