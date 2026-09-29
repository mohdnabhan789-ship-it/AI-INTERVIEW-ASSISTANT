const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const status = document.getElementById("status");
const audioPlayer = document.getElementById("audioPlayer");

const API_URL = "http://127.0.0.1:8000/voice-interview";

let mediaRecorder;
let audioChunks = [];
let stream;

// Start Recording
recordBtn.addEventListener("click", async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.start();

        status.innerText = "🎤 Listening... Speak now";

        recordBtn.disabled = true;
        stopBtn.disabled = false;

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

    } catch (error) {
        console.error(error);
        status.innerText = "Microphone permission denied";
    }
});

// Stop Recording
stopBtn.addEventListener("click", () => {

    mediaRecorder.stop();

    status.innerText = "Processing your interview...";

    recordBtn.disabled = false;
    stopBtn.disabled = true;

    // Stop microphone
    stream.getTracks().forEach(track => track.stop());

    mediaRecorder.onstop = async () => {

        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });

        const formData = new FormData();
        formData.append("file", audioBlob, "recording.webm");

        try {

            const response = await fetch(API_URL, {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error("Server Error");
            }

            const aiAudio = await response.blob();

            const audioURL = URL.createObjectURL(aiAudio);

            audioPlayer.src = audioURL;

            audioPlayer.play();

            status.innerText = "✅ AI replied. Click Start for next answer.";

        } catch (error) {

            console.error(error);

            status.innerText = "❌ Failed to connect to FastAPI";

        }

    };

});