# 🕯️ Ofrenda Digital — Local Memory Sanctuary

> *Ghost in the Machine Challenge (Hacktoberfest 2026 / Día de los Muertos)*  
> Built with **Google Gemma (Open-Weight)**, **FastAPI**, and **Docker**.

---

## 🌺 What I Built
**Ofrenda Digital** is an offline, private virtual altar (ofrenda) inspired by the traditions of Día de los Muertos (Day of the Dead). It allows families and individuals to honor loved ones, ancestors, or cherished companions who have passed on. 

Users place offerings on the altar: their loved one's name, favorite meals, songs, and cherished memories. Powered by Google's open-weight **Gemma** model running completely on your local machine, the application weaves these intimate recollections into a poetic, heartwarming eulogy and oral history blessing.

## 💀 How I Built It
- **Open-Source AI Core:** **Gemma 2 (2B)** open-weight model by Google, executed locally through Ollama.
- **Backend:** Python with **FastAPI** providing the local REST endpoints.
- **Frontend:** Pure HTML5, CSS3, and JavaScript featuring animated flickering candlelight, papel picado motifs, and an interactive ofrenda offering shelf.
- **Audio:** Web Speech API fallback + optional ElevenLabs voice synthesis.
- **Containerization:** Fully containerized with **Docker** and `docker-compose` for reproducible one-command local runs.

## 🌟 Why Does Open Innovation Matter?
1. **Sacred Privacy for Family Memories:** Cherished memories, names of deceased family members, and personal photographs should never be harvested, monetized, or retained by closed corporate cloud APIs. Running Gemma locally guarantees **0 bytes of private family data ever leave your laptop**.
2. **True Permanence (Offline & Zero Cost):** Cloud services shutdown, raise subscription fees, or deprecate APIs. With an open-weight model and Docker, your memorial altar functions 10 years from now, with the internet disconnected and the lights off.
3. **Freedom to Fine-Tune & Customize:** Open weights allow cultural communities to fine-tune the model on regional folklore, indigenous oral traditions, and bilingual dialects (e.g., Spanish/Nahuatl/English) without vendor censorship.

## 🏆 Prize Categories Entered
- **Top Prize** — Ghost in the Machine
- **Best Use of Gemma ($200)** — Powered by Google's open-weight Gemma model running local inference.
- **Best Use of ElevenLabs ($100)** — Voice narration of ofrenda blessings.

## 🚀 Quickstart

### 1. Ensure Ollama & Gemma are running locally:
```bash
ollama run gemma2:2b
```

### 2. Run with Docker:
```bash
docker compose up --build
```
Open your browser at `http://localhost:8000`.

---
*Created for Hacktoberfest Open-Source AI Challenge Week 4: Ghost in the Machine.*