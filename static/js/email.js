function checkEmail() {
    const emailText = document.getElementById("emailText").value;

    fetch("/predict_email", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: emailText }),
    })
    .then(response => response.json())
    .then(data => {
        const result = document.getElementById("result");
        const resultText = document.getElementById("resultText");
        const resultImage = document.getElementById("resultImage");

        if (data.prediction === "spam") {
            resultText.textContent = "⚠️ This Email is SPAM!";
            resultImage.src = "/static/images/spam.png";
        } else {
            resultText.textContent = "✅ This Email is HAM (Not Spam)";
            resultImage.src = "/static/images/ham.png";
        }

        result.classList.remove("hidden");
    });
}
