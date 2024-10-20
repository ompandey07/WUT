document.addEventListener('DOMContentLoaded', function() {
    const preloader = document.getElementById('preloader');
    const mainContent = document.getElementById('mainContent');
    const fileInput = document.querySelector('input[type="file"]');
    const form = document.getElementById('registrationForm');
    const previewImg = document.getElementById('previewImage');
    const userIcon = document.getElementById('userIcon');
    const registerButton = document.getElementById('registerButton');
    const registerText = document.getElementById('registerText');
    const registerSpinner = document.getElementById('registerSpinner');

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
    }, 2000);

    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImg.src = e.target.result;
                previewImg.classList.remove('hidden');
                userIcon.classList.add('hidden');
            }
            reader.readAsDataURL(file);
        }
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);

        // Show spinner and hide text
        registerText.classList.add('hidden');
        registerSpinner.classList.remove('hidden');
        registerButton.disabled = true;

        // Get the current CSRF token
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.text())
        .then(text => {
            let data;
            try {
                data = JSON.parse(text);
            } catch (error) {
                console.error('Error parsing JSON:', error);
                console.log('Received text:', text);
                throw new Error('Invalid JSON response from server');
            }

            if (data.status === 'success') {
                // Update CSRF token
                if (data.csrfToken) {
                    document.querySelector('[name=csrfmiddlewaretoken]').value = data.csrfToken;
                }
                showModal('success', data.message);
                clearForm();
            } else {
                showModal('error', data.message || 'An error occurred');
                resetButton();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showModal('error', 'An error occurred. Please try again.');
            resetButton();
        });
    });

    function resetButton() {
        registerText.classList.remove('hidden');
        registerSpinner.classList.add('hidden');
        registerButton.disabled = false;
    }

    function clearForm() {
        form.reset();
        previewImg.classList.add('hidden');
        userIcon.classList.remove('hidden');
        resetButton();
    }

    function showModal(type, message) {
        const modal = document.getElementById('messageModal');
        const modalIcon = document.getElementById('modalIcon');
        const modalMessage = document.getElementById('modalMessage');
        const modalCloseButton = document.getElementById('modalCloseButton');

        if (type === 'error') {
            modalIcon.innerHTML = '❌';
            modalIcon.className = 'text-6xl mb-4 text-red-500';
        } else {
            modalIcon.innerHTML = `
                <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                    <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
                    <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                </svg>
            `;
        }

        modalMessage.textContent = message;
        modal.classList.remove('hidden');
        setTimeout(() => modal.classList.add('show'), 10);

        // Automatically hide success modal after 2 seconds
        if (type === 'success') {
            setTimeout(() => {
                hideModal();
            }, 2000);
        }

        modalCloseButton.onclick = hideModal;
    }

    function hideModal() {
        const modal = document.getElementById('messageModal');
        modal.classList.remove('show');
        setTimeout(() => modal.classList.add('hidden'), 500);
    }
});