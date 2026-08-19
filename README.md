# MonoChrome — Personal Voice AI Agent (v0.1) — 100% FREE Version

Ei project ta diye apni ekta Siri-er moto voice assistant banaben, jeta
**PC-r browser** ebong **Mobile-er browser** dutoi te kaj korbe — 
ebong **completely free**, kono card ba payment lagbe na.

Brain hishebe amra **Groq** use korchi (Claude na) — karon Groq-er 
permanent free tier ache: card lage na, prottidin 14,400 request free, 
r ultra-fast (voice assistant-er jonno perfect, karon delay kom lagbe).

## Kivabe kaj kore (Architecture)

```
[Browser - Mic diye kotha bolen]
        |  (Web Speech API - voice -> text, FREE, built-in)
        v
[Backend Server - Python FastAPI]
        |  (Claude API - text bujhe reply banay)
        v
[Reply text ferot Browser-e]
        |  (Web Speech API - text -> voice, FREE, built-in)
        v
[MonoChrome reply bole shonay]
```

Voice-to-text ebong text-to-voice **browser nijei** kore dey (Chrome/Edge),
tai Whisper ba kono expensive TTS service lagbe na — ekdom free.

---

## STEP 1: Backend Setup

1. Terminal khulun ebong `backend` folder-e jan:
   ```
   cd ai-agent/backend
   ```

2. Virtual environment banান (optional kintu recommended):
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

3. Dependencies install korun:
   ```
   pip install -r requirements.txt
   ```

4. **FREE API key nen (2 minute lagbe, card lagbe na):**
   - Browser-e jan: **console.groq.com**
   - Google/Email diye Sign up korun
   - Left menu-te **"API Keys"** click korun
   - **"Create API Key"** button-e click korun, ekta name din (jemon "nova")
   - Key ta copy korun (eta shudhu ekbar dekhabe, tai copy kore rakhun)

5. `.env.example` file ta copy kore `.env` name-e rename korun, tarpor 
   copy kora key ta boshan:
   ```
   GROQ_API_KEY=gsk_apnar-real-key-ekhane
   ```

6. Server start korun:
   ```
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Terminal-e `MonoChrome backend is running` type kichu message dekhben.
   Browser-e `http://localhost:8000` khule check korte paren — 
   `{"status": "MonoChrome backend is running ✅"}` dekhle sob thik ache.

---

## STEP 2: Frontend Run (PC-te)

1. `frontend/index.html` file ta shudhu **double-click** korun — 
   browser-e (Chrome recommended) khule jabe.

2. Top-er box-e server URL thik ache kina check korun: `http://localhost:8000`

3. Mic button-e tap korun, kotha bolun — MonoChrome shunbe, bujhbe, ebong 
   voice-e reply dibe.

---

## STEP 3: Mobile theke Access korte chaile

Mobile ebong PC **same WiFi network**-e thakte hobe.

1. PC-r local IP ber korun:
   - Windows: `ipconfig` (IPv4 Address dekhun, jemon `192.168.0.105`)
   - Mac: `ifconfig | grep inet`

2. Backend run korar somoy already `--host 0.0.0.0` deya ache, tai 
   mobile theke access kora jabe.

3. Mobile browser-e frontend URL-e server box-e boshan:
   ```
   http://192.168.0.105:8000
   ```
   (apnar actual IP diye)

4. Frontend file ta mobile-e pathanor jonno, PC theke ekta simple 
   file server chalan (backend folder-e na, frontend folder-e):
   ```
   cd ai-agent/frontend
   python -m http.server 5500
   ```
   Tarpor mobile browser-e: `http://192.168.0.105:5500`

---

## Porer Steps (Future Upgrades)

- [ ] **Wake word** ("Hey MonoChrome") add kora — Porcupine library diye
- [ ] **Deploy kora** internet-e (Render/Railway free tier) — jate WiFi 
      chara-o mobile theke access kora jay
- [ ] **Tools add kora** — alarm set, weather check, calculator
- [ ] **ESP32-S3 port** — jokhon software version stable hobe, ESP32-e 
      mic+speaker+wake-word rekhe, ekhon-er backend API-tei call korte 
      hobe (notun backend lagbe na)

---

## Problem hole

- **"Connect kora jacche na"** → backend run hocche kina check korun, 
  URL thik ache kina dekhun
- **Mic kaj kore na** → Chrome/Edge use korun (Safari-te issue thakte pare), 
  browser mic permission dite hobe
- **API error** → `.env` file-e API key thik ache kina check korun
