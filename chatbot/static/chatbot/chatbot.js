document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const inputField = document.getElementById("chat-input");
    const sendButton = document.getElementById("send-button");
    const csrfToken = document.getElementById("csrf-token").value;  // Get CSRF token

    sendButton.addEventListener("click", function () {
        const userMessage = inputField.value.trim();
        if (userMessage === "") return;

        // Display user message
        chatBox.innerHTML += `<div class="text-end p-2 m-2 bg-secondary text-white "><strong>You:</strong> ${userMessage}</div>`;
        inputField.value = "";

        // Send message to Django API
        fetch("/chatbot/api/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken  // Use CSRF token from hidden input
            },
            body: JSON.stringify({ message: userMessage }),
        })
        .then(response => response.json())
        .then(data => {
            // Display bot response
            chatBox.innerHTML += `<div class="p-2 m-2 bg-dark text-white"><strong>Bot:</strong> ${data.response}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the latest message
        })
        .catch(error => console.error("Error:", error));
    });
});
