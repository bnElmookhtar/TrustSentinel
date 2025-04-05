function checkSpam() {
    let smsText = document.getElementById("smsInput").value;

    if (smsText.trim() === "") {
        alert("Please enter a message.");
        return;
    }

    // Show progress bar while checking
    document.querySelector(".progress-bar-container").style.display = "block";
    document.querySelector(".progress-bar").style.width = "0%"; // Reset the width of progress bar
    document.querySelector(".result-container").style.display = "none"; // Hide result container during processing

    // Make API call to backend (Assuming you have a Flask API)
    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: smsText })
    })
    .then(response => response.json())
    .then(data => {
        // Hide progress bar after 5 seconds
        setTimeout(() => {
            document.querySelector(".progress-bar-container").style.display = "none";
            
            // Reset everything to default state
            document.getElementById("result").innerText = "";
            document.getElementById("awareness-image").src = "../static/images/default-image.png"; // Reset image to default
            document.getElementById("awareness-message").innerText = "";
            document.getElementById("smsInput").value = ""; // Clear the input field
            
            // Show result container
            document.querySelector(".result-container").style.display = "flex";
        }, 5000); // Hide the progress bar after 5 seconds

        const resultText = document.getElementById("result");
        const awarenessImage = document.getElementById("awareness-image");
        const awarenessMessage = document.getElementById("awareness-message");

        if (data.prediction === 'ham') {
            // If prediction is not spam
            resultText.innerText = "Prediction: Not Spam";
            awarenessImage.src = "../static/images/ham.gif"; // Image for ham
            awarenessMessage.innerText = "This message seems safe. Stay cautious and verify the sender.";
            awarenessMessage.style.color = "green"; // Highlight safe message
        } else {
            // If prediction is spam
            resultText.innerText = "Prediction: Spam";
            awarenessImage.src = "../static/images/spamWarning.gif"; // Image for spam
            awarenessMessage.innerText = "Warning! This message looks suspicious and might be a phishing attempt.";
            awarenessMessage.style.color = "red"; // Highlight warning
        }

        // Show the result container with centered result and images
        document.querySelector(".result-container").style.display = "flex";

        // Clear the textarea after checking
        document.getElementById("smsInput").value = "";
    })
    .catch(error => {
        console.error("Error:", error);
        // Hide progress bar if there's an error
        document.querySelector(".progress-bar-container").style.display = "none";
    });
}
