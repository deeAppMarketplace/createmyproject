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
            const sessionId = result.name.split('/').pop();
            document.getElementById('session-id').textContent = sessionId;
            document.getElementById('session-id-input').value = sessionId;
            document.getElementById('activities-section').style.display = 'block';
        } else {
            responseDiv.textContent = `Error: ${result.error}`;
        }
    } catch (error) {
        responseDiv.textContent = `An error occurred: ${error.message}`;
    }
});

document.getElementById('activities-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const sessionId = formData.get('session_id');

    const responseDiv = document.getElementById('activities-response');
    responseDiv.textContent = 'Loading...';

    try {
        const response = await fetch(`/api/jules/${sessionId}/activities`);
        const result = await response.json();

        if (response.ok) {
            let activitiesHtml = '<h3>Activities:</h3><ul>';
            if (result.activities && result.activities.length > 0) {
                result.activities.forEach(activity => {
                    activitiesHtml += `<li>${activity.description}</li>`;
                });
            } else {
                activitiesHtml += '<li>No activities found.</li>';
            }
            activitiesHtml += '</ul>';
            responseDiv.innerHTML = activitiesHtml;
        } else {
            responseDiv.textContent = `Error: ${result.error}`;
        }
    } catch (error) {
        responseDiv.textContent = `An error occurred: ${error.message}`;
    }
});