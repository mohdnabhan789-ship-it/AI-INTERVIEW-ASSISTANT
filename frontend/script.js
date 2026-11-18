
const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const status = document.getElementById("status");
const audioPlayer = document.getElementById("audioPlayer");

const API_URL = "https://ai-interview-assistant-5-zee7.onrender.com/voice-interview";

let mediaRecorder;
let audioChunks = [];
let stream;

recordBtn.addEventListener("click", async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        let mimeType = "";

        if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) {
            mimeType = "audio/webm;codecs=opus";
        } else if (MediaRecorder.isTypeSupported("audio/webm")) {
            mimeType = "audio/webm";
        } else if (MediaRecorder.isTypeSupported("audio/ogg;codecs=opus")) {
            mimeType = "audio/ogg;codecs=opus";
        }

        mediaRecorder = mimeType
            ? new MediaRecorder(stream, { mimeType })
            : new MediaRecorder(stream);

        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data && event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {
            try {
                const audioBlob = new Blob(audioChunks, {
                    type: mediaRecorder.mimeType
                });

                console.log("Audio type:", audioBlob.type);
                console.log("Audio size:", audioBlob.size);

                if (audioBlob.size === 0) {
                    throw new Error("Recording is empty. Please record again.");
                }

                const extension = audioBlob.type.includes("ogg")
                    ? "ogg"
                    : "webm";

                const formData = new FormData();

                formData.append(
                    "file",
                    audioBlob,
                    `recording.${extension}`
                );

                status.innerText = "Processing your interview...";

                const response = await fetch(API_URL, {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(errorText);
                }

                const aiAudio = await response.blob();

                if (aiAudio.size === 0) {
                    throw new Error("AI audio response is empty.");
                }

                const audioURL = URL.createObjectURL(aiAudio);

                audioPlayer.src = audioURL;
                await audioPlayer.play();

                status.innerText = "AI replied! Click Start for next answer.";

            } catch (error) {
                console.error("Upload error:", error);
                status.innerText = "Error: " + error.message;
            }
        };

        mediaRecorder.start();

        status.innerText = "Listening... Speak now";

        recordBtn.disabled = true;
        stopBtn.disabled = false;

    } catch (error) {
        console.error(error);
        status.innerText = "Microphone error: " + error.message;
    }
});

stopBtn.addEventListener("click", () => {
    if (!mediaRecorder || mediaRecorder.state !== "recording") {
        return;
    }

    mediaRecorder.stop();

    stream.getTracks().forEach(track => track.stop());

    recordBtn.disabled = false;
    stopBtn.disabled = true;

    status.innerText = "Recording completed. Processing...";
});
