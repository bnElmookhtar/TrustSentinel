// static/js/robocalls.js
async function checkRobocall() {
    const fileInput = document.getElementById('fileInput');
    const resultElement = document.getElementById('result');
    const awarenessMessage = document.getElementById('awareness-message');
    const awarenessImage = document.getElementById('awareness-image');
    const progressBarContainer = document.querySelector('.progress-bar-container');
    const snackbar = document.getElementById('snackbar');
    const resultContainer = document.querySelector('.result-container');

    // Reset previous results
    resultElement.textContent = '';
    awarenessMessage.textContent = '';
    awarenessImage.style.display = 'none';
    awarenessImage.style.animation = 'none'; // Reset animation
    progressBarContainer.style.display = 'none';
    resultContainer.setAttribute('data-result', '');

    // Check if file is selected
    if (!fileInput.files || fileInput.files.length === 0) {
        snackbar.textContent = 'Please upload an audio file.';
        snackbar.className = 'show';
        setTimeout(() => { snackbar.className = ''; }, 3000);
        return;
    }

    // Show progress bar
    progressBarContainer.style.display = 'block';

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();

        // Hide progress bar
        progressBarContainer.style.display = 'none';

        if (result.error) {
            resultElement.textContent = `Error: ${result.error}`;
            snackbar.textContent = result.error;
            snackbar.className = 'show';
            setTimeout(() => { snackbar.className = ''; }, 3000);
        } else {
            resultElement.textContent = result.result;
            resultContainer.setAttribute('data-result', result.result === 'Robocall' ? 'robocall' : 'safe');
            if (result.result === 'Robocall') {
                awarenessMessage.textContent = 'Warning: This call may be a robocall! Avoid sharing personal information.';
                awarenessImage.src = '../static/images/robocall_warning.jpg';
            } else {
                awarenessMessage.textContent = 'This call seems safe, but always stay cautious!';
                awarenessImage.src = '../static/images/safe_call.jpg';
            }
            awarenessImage.style.display = 'block';
            // Re-trigger animation
            setTimeout(() => {
                awarenessImage.style.animation = 'popIn 0.5s ease-out forwards';
            }, 10);
        }
    } catch (error) {
        progressBarContainer.style.display = 'none';
        resultElement.textContent = `Error: ${error.message}`;
        snackbar.textContent = 'An error occurred. Please try again.';
        snackbar.className = 'show';
        setTimeout(() => { snackbar.className = ''; }, 3000);
    }
}