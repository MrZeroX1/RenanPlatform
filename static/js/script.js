document.addEventListener("DOMContentLoaded", function () {
  // Get references to the elements
  const createVoiceOverButton = document.getElementById("create-voice-over");
  const createBroadcastButton = document.getElementById("create-boadcast");
  const audioElement = document.getElementById("audio-result");
  const ttsInputTextArea = document.getElementById("tts-input");
  const textGenInput = document.getElementById("text-gen-input");
  const createButton = document.getElementById("create");
  const playButton = document.getElementById("playButton");
  const playIcon = playButton.querySelector(".play-icon");

  function resetCreateButton() {
    createButton.innerHTML = `
      <img src="../static/images/icons/create.png" alt="انشاء" class="btn-icon">
      انـشــاء
    `;
    createButton.disabled = false;
  }

  function resetTextGen() {
    textGenInput.innerHTML = `<textarea id="text-gen-input" class="input-textarea no-scroll" style="height: 80px;"
              placeholder="اكتب فكرتك هنا ليتم انشاء نص إبداعي لها.."></textarea> <br>`;
  }

  // Function to handle the pre-defined button logic
  function handlePredefinedText(buttonType) {
    const predefinedData = {
      "create-voice-over": {
        audioPath: "../audio/samples/RenanSample.wav",
        text: "خَل صُوتِك يَبرِز مَع رِنان سَواء كِنت تِحتَاج تَعليق صَوتِي احترافي،أو تبغَى تحَسّن إنتاجِك، رِسَالتِك مَعْنَا تُسْمَع! هذا هو رِنان.",
      },
      "create-boadcast": {
        audioPath: "../audio/samples/bodcastSample.wav",
        text: "كِلنا عِنْدِنا صُندوقْ أفْكار، فِكرة جَتْنَا فِي، السيارة اوالطَيَّارة، و المَدرسة اوالعَمَل، لَمَّا ضَحَك لِنا الحَظ، أو خَاننا التَّعْبِير. اليوم بِنِتحَدث عَن كيف مُمكِن نعبِّر عَن أفكارنا، ونَسْتَعرِض مَعكُم أشهر الشركات في هذا المجال!",
      },
    };

    const selectedData = predefinedData[buttonType];
    if (selectedData) {
      audioElement.src = selectedData.audioPath;
      audioElement.hidden = false;
      ttsInputTextArea.value = selectedData.text;
    }
  }

  // Event listeners for pre-defined buttons
  createVoiceOverButton.addEventListener("click", function () {
    handlePredefinedText("create-voice-over");
  });

  createBroadcastButton.addEventListener("click", function () {
    handlePredefinedText("create-boadcast");
  });

  // Event listener for the "Create" button to generate audio
  createButton.addEventListener("click", async function () {
    const textInput = textGenInput.value;
    const ttsInput = ttsInputTextArea.value;

    // Ensure only one text area is filled
    if (textInput && ttsInput) {
      alert("الرجاء أملئ فقط واحدة من الخانات فقط");
      return;
    }

    if (textInput) {
      try {
          createButton.innerHTML = "يتم إنتاج النص...";
          createButton.disabled = true;

          const response = await fetch("/generate-text", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ input: textInput }),
          });

          const data = await response.json();
          console.log("Text Generation Response:", data); // Log the response to check if it's received

          const generatedText = data.generated_text;

          // Check if generatedText is populated
          if (generatedText) {
              ttsInputTextArea.value = ""; // Clear previous text

              // Display generated text in `tts-input` with typing effect
              let i = 0;
              const speed = 10; // Typing speed
              function typeWriter() {
                  if (i < generatedText.length) {
                      ttsInputTextArea.value += generatedText.charAt(i);
                      i++;
                      setTimeout(typeWriter, speed);
                  }
              }
              typeWriter();
          } else {
              alert("No text was generated.");
          }

          resetCreateButton();
          resetTextGen();
      } catch (error) {
          console.error("Error:", error);
          resetCreateButton();
      }
  }
    // If the user is converting text to speech
    else if (ttsInput) {
      createButton.innerText = "يتم تحويل النص إلى صوت...";
      createButton.disabled = true;
      const text = ttsInput;
      const speakerId =
        document.getElementById("speaker-select").value || "speaker1"; // Default speaker
      const speed = document.getElementById("speed-select").value || "1.00"; // Default speed
      const bgMusicFilename =
        document.getElementById("music-select").value || "no-music"; // Default to no music

      try {
        const response = await fetch("/generate-audio", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            text: text,
            speaker_id: speakerId,
            speed: speed,
            bg_music_filename: bgMusicFilename,
          }),
        });

        const blob = await response.blob();
        console.log("Text Generation Response:", data); // Add this line
        const audioURL = URL.createObjectURL(blob);
        audioElement.src = audioURL;
        audioElement.play();

        resetCreateButton();
      } catch (error) {
        console.error("Error:", error);
        resetCreateButton();
      }
    }
  });

  // Toggle play and pause functionality for the playButton
  playButton.addEventListener("click", function () {
    if (audioElement.paused) {
      audioElement.play();
      playIcon.classList.remove("play-icon");
      playIcon.classList.add("pause-icon");
    } else {
      audioElement.pause();
      playIcon.classList.remove("pause-icon");
      playIcon.classList.add("play-icon");
    }
  });

  // Automatically reset to the play icon when the audio ends
  audioElement.addEventListener("ended", function () {
    playIcon.classList.remove("pause-icon");
    playIcon.classList.add("play-icon");
  });
});

// Upload pop-up
const speakerSelect = document.getElementById("speaker-select");
const uploadForm = document.getElementById("upload-form");
const overlay = document.getElementById("overlay");
const popup = document.getElementById("popup");
const fileInput = document.getElementById("voice-file");
const uploadButton = uploadForm.querySelector("button[type='button']");
const cancelButton = uploadForm.querySelector("button[type='button']:last-child");

function showPopup() {
  overlay.style.display = "block";
  popup.style.display = "block";
}

function closePopup() {
  overlay.style.display = "none";
  popup.style.display = "none";
  fileInput.value = "";
}

speakerSelect.addEventListener("change", function () {
  if (speakerSelect.value === "new") {
    showPopup();
  }
});

uploadButton.addEventListener("click", function () {
  const file = fileInput.files[0];

  if (file && file.type === "audio/wav") {
    const formData = new FormData();
    formData.append("file", file, "new.wav");

    fetch("/upload-voice", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
        closePopup();
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        alert("File upload failed. Please try again.");
      });
  } else {
    alert("Please select a valid .wav file.");
  }
});

cancelButton.addEventListener("click", closePopup);