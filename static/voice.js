// static/js/voice.js

document.addEventListener('DOMContentLoaded', function () {
    const micBtn = document.getElementById('mic-btn');
    const urgencyInputs = document.getElementsByName('urgency');

    if (micBtn) {
        micBtn.addEventListener('click', () => {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-US';
            recognition.start();

            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript.toLowerCase();
                console.log("Heard:", transcript);
                if (transcript.includes('low')) urgencyInputs[0].checked = true;
                else if (transcript.includes('medium')) urgencyInputs[1].checked = true;
                else if (transcript.includes('high')) urgencyInputs[2].checked = true;
            };
        });
    }
});