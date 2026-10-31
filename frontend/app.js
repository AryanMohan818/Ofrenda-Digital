document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("memorial-form");
  const nameInput = document.getElementById("name");
  const relationInput = document.getElementById("relation");
  const yearsInput = document.getElementById("years");
  const photoInput = document.getElementById("photo");
  const memoriesInput = document.getElementById("memories");
  const foodsInput = document.getElementById("foods");
  const musicInput = document.getElementById("music");
  const summonBtn = document.getElementById("summon-btn");

  const displayName = document.getElementById("display-name");
  const displayYears = document.getElementById("display-years");
  const altarPhoto = document.getElementById("altar-photo");
  const photoFallbackIcon = document.getElementById("photo-fallback-icon");
  const remembranceText = document.getElementById("remembrance-text");
  const loadingSpinner = document.getElementById("loading-spinner");
  const audioBar = document.getElementById("audio-bar");
  const narrateBtn = document.getElementById("narrate-btn");

  let currentEulogy = "";
  let currentAudioBase64 = null;

  // Handle local photo preview
  photoInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        altarPhoto.src = event.target.result;
        altarPhoto.classList.remove("hidden");
        photoFallbackIcon.classList.add("hidden");
      };
      reader.readAsDataURL(file);
    }
  });

  // Handle Form Submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = nameInput.value.trim();
    const relation = relationInput.value.trim() || "Loved One";
    const years = yearsInput.value.trim();
    const memories = memoriesInput.value.trim();
    const foods = foodsInput.value.trim();
    const music = musicInput.value.trim();

    if (!name || !memories) {
      alert("Please provide at least a Name and Cherished Memories.");
      return;
    }

    // Update altar display
    displayName.textContent = name;
    displayYears.textContent = years ? `${years} (${relation})` : relation;

    // UI Loading state
    summonBtn.disabled = true;
    summonBtn.style.opacity = "0.7";
    remembranceText.classList.add("hidden");
    loadingSpinner.classList.remove("hidden");
    audioBar.classList.add("hidden");

    try {
      const response = await fetch("/api/remember", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          relation,
          years,
          favorite_memories: memories,
          favorite_foods: foods,
          favorite_music: music
        })
      });

      const data = await response.json();
      currentEulogy = data.remembrance || "Memory kept eternally in light.";
      remembranceText.textContent = currentEulogy;
      audioBar.classList.remove("hidden");

      // Check for voice narration
      fetchVoiceNarration(currentEulogy);
    } catch (err) {
      console.error("Inference request failed:", err);
      remembranceText.textContent = `A blessing for ${name}: May the candles and marigolds guide your spirit home to us. Forever honored, forever remembered.`;
      audioBar.classList.remove("hidden");
    } finally {
      loadingSpinner.classList.add("hidden");
      remembranceText.classList.remove("hidden");
      summonBtn.disabled = false;
      summonBtn.style.opacity = "1";
    }
  });

  // Optional Voice Narration (ElevenLabs or Browser Speech)
  async function fetchVoiceNarration(text) {
    try {
      const res = await fetch(`/api/tts?text=${encodeURIComponent(text.slice(0, 300))}`, {
        method: "POST"
      });
      const data = await res.json();
      if (data.audio_base64) {
        currentAudioBase64 = data.audio_base64;
      } else {
        currentAudioBase64 = null;
      }
    } catch (e) {
      currentAudioBase64 = null;
    }
  }

  narrateBtn.addEventListener("click", () => {
    if (currentAudioBase64) {
      const audio = new Audio(currentAudioBase64);
      audio.play();
    } else if ("speechSynthesis" in window) {
      // Offline fallback: Web Speech API
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(currentEulogy);
      utterance.pitch = 0.95;
      utterance.rate = 0.88;
      window.speechSynthesis.speak(utterance);
    } else {
      alert("Speech synthesis is not supported on this browser.");
    }
  });
});