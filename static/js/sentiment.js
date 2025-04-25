function checkSentiment() {
    let smsText = document.getElementById("smsInput").value;

    if (smsText.trim() === "") {
        showSnackbar("Please enter a message.");
        return;
    }
    // Show progress bar while checking
    document.querySelector(".progress-bar-container").style.display = "block";
    document.querySelector(".progress-bar").style.width = "0%"; // Reset the width of progress bar
    document.querySelector(".result-container").style.display = "none"; // Hide result container during processing

    // Make API call to backend (Assuming you have a Flask API)
    fetch("/predict_sentiment", {
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
//Number	Emotion Description
//1	Joy
//2	Fear
//3	Anger
//4	Sadness
//5	Disgust
//6	Shame, Embarrassment, or Guilt
//7	Embarrassment or Guilt
if (data.prediction === '0' || data.prediction === '1') {
               
    resultText.innerText = "Prediction: Positive";
    awarenessImage.src = "../static/images/Positive.jpg"; // Image for ham
    awarenessMessage.innerText = "This message seems as Positive.";
}
else{      
    
            resultText.innerText = "Prediction: Negative";
            awarenessImage.src = "../static/images/Negative.jpg"; // Image for ham
            awarenessMessage.innerText = "This message seems as Negative.";
       
        
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

