function checkSpam() {
    let messageText = document.getElementById("smsInput").value;

    if (messageText.trim() === "") {
        showSnackbar("Please enter a message.");
        return;
    }

    document.querySelector(".progress-bar-container").style.display = "block";
    document.querySelector(".progress-bar").style.width = "0%";
    document.querySelector(".result-container").style.display = "none";

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: messageText })
    })
    .then(response => response.json())
    .then(data => {
        setTimeout(() => {
            document.querySelector(".progress-bar-container").style.display = "none";
            document.querySelector(".result-container").style.display = "flex";
        }, 5000);

        const resultText = document.getElementById("result");
        const awarenessImage = document.getElementById("awareness-image");
        const awarenessMessage = document.getElementById("awareness-message");

        if (data.prediction === 'ham') {
            resultText.innerText = "Prediction: Not Spam";
            awarenessImage.src = "../static/images/ham.gif";
            awarenessMessage.innerText = "This message seems safe. Still, verify the sender.";
            awarenessMessage.style.color = "green";
        } else {
            resultText.innerText = "Prediction: Spam";
            awarenessImage.src = "../static/images/spamWarning.gif";
            awarenessMessage.innerText = "Warning! This looks suspicious and might be a phishing attempt.";
            awarenessMessage.style.color = "red";
        }

        document.getElementById("smsInput").value = "";
    })
    .catch(error => {
        console.error("Error:", error);
        document.querySelector(".progress-bar-container").style.display = "none";
    });
}

function showSnackbar(message) {
    var snackbar = document.getElementById("snackbar");
    snackbar.innerText = message;
    snackbar.className = "show";
    setTimeout(() => {
        snackbar.className = snackbar.className.replace("show", "");
    }, 3000);
}



// Function to show the snackbar
function showSnackbar(message) {
    var snackbar = document.getElementById("snackbar");
    snackbar.innerText = message; // Set the message
    snackbar.className = "show"; // Add the "show" class to make it visible

    // After 3 seconds, remove the "show" class to hide the snackbar
    setTimeout(function() {
        snackbar.className = snackbar.className.replace("show", ""); 
    }, 3000);
}
