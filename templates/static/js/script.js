document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.getElementById('submitButton');
    const inputField = document.getElementById('inputField');
    const responseDiv = document.getElementById('response');

    // FastAPI backend URL - adjust this to your actual FastAPI endpoint
    const apiUrl = 'http://localhost:8000/api/process';

    submitButton.addEventListener('click', async function() {
        const inputText = inputField.value.trim();

        if (!inputText) {
            responseDiv.textContent = 'Please enter some text';
            responseDiv.className = 'error';
            return;
        }

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: inputText }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            responseDiv.textContent = `Server response: ${data.result}`;
            responseDiv.className = '';
        } catch (error) {
            responseDiv.textContent = `Error: ${error.message}`;
            responseDiv.className = 'error';
            console.error('Error:', error);
        }
    });
});