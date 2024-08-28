document.addEventListener('DOMContentLoaded', function() {
    const audioPlayer = document.getElementById('audioPlayer');
    const statusMessages = document.getElementById('statusMessages'); // Zorg ervoor dat dit element bestaat in je HTML
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    
    // Verberg de stop-knop bij het laden
    stopBtn.style.display = 'none';

    startBtn.addEventListener('click', function() {
        fetch('/start', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                // Verberg startknop en toon stopknop
                startBtn.style.display = 'none';
                stopBtn.style.display = 'inline-block';

                // Voeg tekst toe aan het statusMessages element om opname te bevestigen
                statusMessages.textContent = 'Opname gestart...';
            })
            .catch(error => console.error('Error:', error));
    });

    stopBtn.addEventListener('click', function() {
        // Verberg beide knoppen en toon "Wachten op reactie..."
        startBtn.style.display = 'none';
        stopBtn.style.display = 'none';
        statusMessages.textContent = 'Wachten op reactie...';

        fetch('/stop', { method: 'POST' })
            .then(response => response.blob())
            .then(blob => {
                const audioUrl = URL.createObjectURL(blob);
                audioPlayer.src = audioUrl;
                audioPlayer.style.display = 'block';
                audioPlayer.play();

                // Zodra de reactie is ontvangen, toon "Reactie ontvangen!" en toon de 'Start Recording'-knop
                statusMessages.textContent = 'Reactie ontvangen!';
                startBtn.style.display = 'inline-block';
            })
            .catch(error => {
                console.error('Error:', error);
                // Als er een fout optreedt, toon dan een foutmelding en de 'Start Recording'-knop
                statusMessages.textContent = 'Er is een fout opgetreden. Probeer het opnieuw.';
                startBtn.style.display = 'inline-block';
            });
    });

    document.getElementById('messageForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const messageInput = document.getElementById('messageInput');
        
        fetch('/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: messageInput.value })
        })
        .then(response => response.json())
        .then(data => {
            const userMessageDiv = document.createElement('div');
            userMessageDiv.textContent = 'Jij: ' + messageInput.value;
            userMessageDiv.classList.add('message');
            chatWindow.appendChild(userMessageDiv);

            const serverMessageDiv = document.createElement('div');
            serverMessageDiv.textContent = 'Server: ' + data.response;
            serverMessageDiv.classList.add('message');
            chatWindow.appendChild(serverMessageDiv);

            chatWindow.scrollTop = chatWindow.scrollHeight;
            messageInput.value = '';
        })
        .catch(error => console.error('Error:', error));
    });
});
