document.addEventListener('DOMContentLoaded', function() {
    const captureBtn = document.getElementById('captureBtn'); // Zorg ervoor dat dit element bestaat in je HTML
    const statusMessages = document.getElementById('statusMessages'); // Zorg ervoor dat dit element bestaat in je HTML

    captureBtn.addEventListener('click', function() {
        captureImage(); // Roep de bestaande captureImage functie aan

        // Verberg de capture-knop en toon een statusbericht
        captureBtn.style.display = 'none';
        statusMessages.textContent = 'Foto maken...';
    });

    function captureImage() {
        fetch('/capture')
            .then(response => response.json())
            .then(data => {
                if(data.status === "success") {
                    const imageElement = document.getElementById('capturedImage');
                    imageElement.src = `${data.image_url}?${new Date().getTime()}`;
                    imageElement.style.display = 'block';

                    const analysisTextElement = document.getElementById('analysisText');
                    analysisTextElement.textContent = data.analysis_text;

                    statusMessages.textContent = 'Foto succesvol vastgelegd!'; // Update statusbericht

                    if(data.audio_url) {
                        const audioElement = document.getElementById('analysisAudio');
                        audioElement.src = data.audio_url;
                        audioElement.style.display = 'block';
                        audioElement.play(); // Speel audio automatisch af
                    }

                    captureBtn.style.display = 'inline-block'; // Toon de capture-knop weer
                } else {
                    alert(data.message);
                    statusMessages.textContent = ''; // Wis statusbericht
                    captureBtn.style.display = 'inline-block'; // Toon de capture-knop weer
                }
            })
            .catch(error => {
                console.error('Error:', error);
                statusMessages.textContent = 'Er is een fout opgetreden. Probeer het opnieuw.';
                captureBtn.style.display = 'inline-block'; // Toon de capture-knop weer bij een fout
            });
            fetch('/capture', { method: 'POST' })
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
    }
});

if(data.audio_url) {
    const audioElement = document.getElementById('analysisAudio');
    audioElement.src = data.audio_url;
    audioElement.style.display = 'block';
    audioElement.load(); // Zorg ervoor dat het audio-element opnieuw geladen wordt na het instellen van de src.
    audioElement.play(); // Probeer de audio af te spelen.
}
