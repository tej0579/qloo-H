import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.bot import videogame_bot
from app.memory import memory_store
from app.qloo import QLOO_API_KEY, QLOO_BASE_URL
import httpx
import time

app = FastAPI(title="Qloo Videogame Cultural Intelligence Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ResetRequest(BaseModel):
    session_id: str

@app.get("/api/health")
async def health():
    qloo_ok = False
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            res = await client.get(
                f"{QLOO_BASE_URL}/search",
                headers={"X-Api-Key": QLOO_API_KEY, "Accept": "application/json"},
                params={"query": "Elden Ring", "type": "urn:entity:videogame", "limit": 1}
            )
            qloo_ok = (res.status_code == 200)
    except Exception:
        pass

    return {
        "status": "online",
        "qloo_connected": qloo_ok,
        "category": "urn:entity:videogame"
    }

@app.post("/api/chat")
async def chat(req: ChatRequest):
    resp = await videogame_bot.process_turn(session_id=req.session_id, message=req.message)
    return resp

@app.post("/api/reset")
async def reset(req: ResetRequest):
    memory_store.reset(req.session_id)
    return {"status": "SUCCESS", "message": "Session reset."}

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """
    Direct, standalone interactive Cyber-themed Chat UI embedded directly in FastAPI.
    Zero-config: runs straight out of http://localhost:8000
    """
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Qloo Cultural Agent — Category 1: Videogames</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Space+Grotesk:wght@400;600;700&display=swap');
    body { font-family: 'Space Grotesk', sans-serif; background-color: #090a0f; }
    .mono { font-family: 'JetBrains Mono', monospace; }
    .glow-cyan { text-shadow: 0 0 10px rgba(0, 240, 255, 0.5); }
    .border-glow { border-color: rgba(0, 240, 255, 0.3); box-shadow: 0 0 15px rgba(0, 240, 255, 0.1); }
  </style>
</head>
<body class="text-zinc-200 flex flex-col h-screen overflow-hidden">
  <!-- Header Bar -->
  <header class="border-b border-zinc-800 bg-[#0d0f18] px-6 py-3 flex items-center justify-between shrink-0">
    <div class="flex items-center gap-3">
      <div class="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/40 flex items-center justify-center text-cyan-400 font-bold">
        🎮
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-sm font-bold text-white tracking-wide">QLOO VIDEOGAME CULTURAL BOT</h1>
          <span class="mono text-[10px] px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30">Category 1/14: urn:entity:videogame</span>
        </div>
        <p class="mono text-[11px] text-zinc-400">Architecture: Ingest &rarr; Qloo Search &rarr; Counter-Prompts &rarr; Accumulate &rarr; Final LLM</p>
      </div>
    </div>
    <div class="flex items-center gap-3">
      <div id="turn-badge" class="mono text-xs px-2.5 py-1 rounded bg-zinc-900 border border-zinc-700 text-cyan-400 font-bold">Turn 0: Awaiting Game</div>
      <button onclick="resetSession()" class="px-2.5 py-1 text-xs text-zinc-400 hover:text-white bg-zinc-800 hover:bg-zinc-700 rounded transition">Reset</button>
    </div>
  </header>

  <!-- Chat Log -->
  <main id="chat-box" class="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 max-w-4xl mx-auto w-full">
    <!-- Welcome message -->
    <div class="flex flex-col items-start space-y-1">
      <span class="mono text-[10px] text-zinc-500">Qloo Agent</span>
      <div class="p-4 rounded-xl rounded-tl-sm bg-[#121524] border border-zinc-800 text-sm leading-relaxed max-w-2xl space-y-2">
        <p>Welcome! I am the <strong>Qloo Videogame Cultural Intelligence Agent</strong>.</p>
        <p class="text-zinc-400">I strictly scout video games by querying Qloo's 250M+ entity taste graph. Name any video game you love to begin the 3-question calibration loop.</p>
      </div>
    </div>
  </main>

  <!-- Input and Quick Anchor Bar -->
  <footer class="border-t border-zinc-800 bg-[#0d0f18] p-4 shrink-0 max-w-4xl mx-auto w-full space-y-2">
    <div id="quick-anchors" class="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
      <span class="mono text-zinc-500 text-[11px]">Quick Anchors:</span>
      <button onclick="sendMsg('Elden Ring')" class="px-2.5 py-1 rounded bg-zinc-900 border border-zinc-700 text-zinc-300 hover:border-cyan-400 hover:text-white transition">+ Elden Ring</button>
      <button onclick="sendMsg('Cyberpunk 2077')" class="px-2.5 py-1 rounded bg-zinc-900 border border-zinc-700 text-zinc-300 hover:border-cyan-400 hover:text-white transition">+ Cyberpunk 2077</button>
      <button onclick="sendMsg('Hades')" class="px-2.5 py-1 rounded bg-zinc-900 border border-zinc-700 text-zinc-300 hover:border-cyan-400 hover:text-white transition">+ Hades</button>
      <button onclick="sendMsg('DOOM')" class="px-2.5 py-1 rounded bg-zinc-900 border border-zinc-700 text-zinc-300 hover:border-cyan-400 hover:text-white transition">+ DOOM</button>
    </div>
    <form id="chat-form" onsubmit="event.preventDefault(); submitInput();" class="flex gap-2">
      <input id="user-input" type="text" placeholder="Enter a video game title (e.g. Elden Ring, Hades, Cyberpunk)..." 
        class="flex-1 px-4 py-2.5 rounded-lg bg-zinc-900 border border-zinc-700 text-sm text-white focus:outline-none focus:border-cyan-400 transition" />
      <button id="send-btn" type="submit" class="px-5 py-2.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black font-bold text-sm transition">Send</button>
    </form>
  </footer>

  <script>
    let sessionId = "sess_" + Date.now();
    let currentTurn = 0;

    function appendMessage(sender, text, isRollback = false, options = null, qlooData = null) {
      const box = document.getElementById("chat-box");
      const wrap = document.createElement("div");
      wrap.className = "flex flex-col " + (sender === "user" ? "items-end" : "items-start") + " space-y-1";

      const label = document.createElement("span");
      label.className = "mono text-[10px] text-zinc-500";
      label.innerText = sender === "user" ? "You" : "Qloo Agent";
      wrap.appendChild(label);

      const bubble = document.createElement("div");
      if (sender === "user") {
        bubble.className = "px-4 py-2.5 rounded-xl rounded-tr-sm bg-cyan-500 text-black font-semibold text-sm max-w-md";
        bubble.innerText = text;
      } else {
        bubble.className = "p-4 rounded-xl rounded-tl-sm " + (isRollback ? "bg-red-950/40 border border-red-500/50 text-red-200" : "bg-[#121524] border border-zinc-800 text-zinc-200") + " text-sm leading-relaxed max-w-2xl space-y-3";
        bubble.innerHTML = marked.parse(text);

        if (options && options.length > 0) {
          const optWrap = document.createElement("div");
          optWrap.className = "pt-2 border-t border-zinc-800 flex flex-wrap gap-2";
          options.forEach(opt => {
            const btn = document.createElement("button");
            btn.className = "px-3 py-1.5 rounded-md bg-zinc-800 hover:bg-cyan-500/20 hover:border-cyan-400 border border-zinc-700 text-xs text-zinc-300 font-medium transition text-left";
            btn.innerHTML = "&rarr; " + opt;
            btn.onclick = () => sendMsg(opt);
            optWrap.appendChild(btn);
          });
          bubble.appendChild(optWrap);
        }
      }

      wrap.appendChild(bubble);
      box.appendChild(wrap);
      box.scrollTop = box.scrollHeight;
    }

    async function sendMsg(text) {
      if (!text.trim()) return;
      appendMessage("user", text);
      document.getElementById("user-input").value = "";
      const sendBtn = document.getElementById("send-btn");
      sendBtn.disabled = true;
      sendBtn.innerText = "Thinking...";

      try {
        const res = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId, message: text })
        });
        const data = await res.json();
        currentTurn = data.turn;
        updateTurnBadge();

        appendMessage("bot", data.message, data.is_rollback, data.counter_prompt?.options, data.qloo_data);
      } catch (err) {
        appendMessage("bot", "⚠️ Connection error to Qloo agent backend.", true);
      } finally {
        sendBtn.disabled = false;
        sendBtn.innerText = "Send";
      }
    }

    function submitInput() {
      const val = document.getElementById("user-input").value;
      sendMsg(val);
    }

    function updateTurnBadge() {
      const badge = document.getElementById("turn-badge");
      const qa = document.getElementById("quick-anchors");
      const titles = [
        "Turn 0: Awaiting Game",
        "Turn 1: Mechanics Calibration",
        "Turn 2: Aesthetics Calibration",
        "Turn 3: Platform Scoping",
        "Turn 4: Synthesized"
      ];
      badge.innerText = titles[currentTurn] || "Turn " + currentTurn;
      if (currentTurn > 0) {
        qa.style.display = "none";
        document.getElementById("user-input").placeholder = "Type your response or select an option above...";
      } else {
        qa.style.display = "flex";
        document.getElementById("user-input").placeholder = "Enter a video game title (e.g. Elden Ring, Hades, Cyberpunk)...";
      }
    }

    async function resetSession() {
      await fetch("/api/reset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId })
      });
      sessionId = "sess_" + Date.now();
      currentTurn = 0;
      updateTurnBadge();
      const box = document.getElementById("chat-box");
      box.innerHTML = "";
      appendMessage("bot", "Session reset. Enter any video game title to begin scouting.");
    }
  </script>
</body>
</html>"""
    return HTMLResponse(content=html_content)
