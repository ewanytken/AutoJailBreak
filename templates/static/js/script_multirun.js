    const URI_MULTIRUN = 'http://localhost:8800/multirun';
//
    const path = document.getElementById('path');
    const handler = document.getElementById('handler');
    const runButton = document.getElementById('runButton');
    const serviceResponse = document.getElementById('serviceResponse');

document.addEventListener('DOMContentLoaded', function() {

    runButton.addEventListener('click', async function() {

        const path_value = path.value.trim();
        const handler_value = handler.value.trim();

        if (!path_value || !handler_value) {
            path_value.textContent = 'Enter path to JSON files';
            path_value.className = 'error';

            handler_value.textContent = 'Enter path to service handler';
            handler_value.className = 'error';
            return;
        }

        let multirun_parameters = {};

        multirun_parameters.handler = handler_value ?? "None";
        multirun_parameters.direction = path_value ?? "None";

        try {
            const response = await fetch(URI_MULTIRUN, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(multirun_parameters),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            serviceResponse.innerHTML = data.result;
            serviceResponse.className = '';

        } catch (error) {
            serviceResponse.textContent = `Error: ${error.message}`;
            serviceResponse.className = 'error';
            console.error('Error:', error);
        }
    });
});

