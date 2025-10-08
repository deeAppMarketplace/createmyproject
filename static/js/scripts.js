document.getElementById('jules-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    const responseDiv = document.getElementById('response');
    responseDiv.textContent = 'Loading...';

    try {
        const response = await fetch('/api/jules', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            responseDiv.textContent = `Success:\n${JSON.stringify(result, null, 2)}`;
        } else {
            responseDiv.textContent = `Error: ${result.error}`;
        }
    } catch (error) {
        responseDiv.textContent = `An error occurred: ${error.message}`;
    }
});