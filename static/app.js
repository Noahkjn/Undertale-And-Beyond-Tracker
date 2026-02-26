const STATUS_STALE_SECONDS = 6;
const statusEl = document.getElementById("status");
const updatedEl = document.getElementById("updated-at");
const joinUrlEl = document.getElementById("join-url");
const rawPayloadEl = document.getElementById("raw-payload");
const sessionCodeInput = document.getElementById("session-code");
const createBtn = document.getElementById("create-session");
const connectBtn = document.getElementById("connect-session");
const copyBtn = document.getElementById("copy-join");

const statMap = {
  hp: document.getElementById("stat-hp"),
  lv: document.getElementById("stat-lv"),
  exp: document.getElementById("stat-exp"),
  gold: document.getElementById("stat-gold"),
  location: document.getElementById("stat-location"),
  items: document.getElementById("stat-items"),
};

let currentCode = "";
let pollTimer = null;

function setStatus(text, isStale) {
  statusEl.textContent = text;
  statusEl.classList.toggle("stale", Boolean(isStale));
}
function formatUpdated(ts) {
  if (!ts) return "No data yet";
  return `Last update: ${new Date(ts * 1000).toLocaleTimeString()}`;
}
function renderPayload(payload) {
  statMap.hp.textContent = payload.hp ?? "--";
  statMap.lv.textContent = payload.lv ?? "--";
  statMap.exp.textContent = payload.exp ?? "--";
  statMap.gold.textContent = payload.gold ?? "--";
  statMap.location.textContent = payload.location ?? "--";
  const items = Array.isArray(payload.items) ? payload.items.join(", ") : payload.items;
  statMap.items.textContent = items ?? "--";
  rawPayloadEl.textContent = JSON.stringify(payload, null, 2);
}

async function fetchState() {
  if (!currentCode) return;
  try {
    const res = await fetch(`/api/state?code=${currentCode}`);
    if (!res.ok) return setStatus("Disconnected", true);
    const data = await res.json();
    renderPayload(data.payload || {});
    updatedEl.textContent = formatUpdated(data.lastUpdated || 0);
    const age = Math.floor(Date.now() / 1000) - (data.lastUpdated || 0);
    setStatus(age > STATUS_STALE_SECONDS ? "Not updating" : "Live", age > STATUS_STALE_SECONDS);
  } catch {
    setStatus("Disconnected", true);
  }
}

function startPolling() {
  if (pollTimer) clearInterval(pollTimer);
  pollTimer = setInterval(fetchState, 1000);
  fetchState();
}

async function createSession() {
  const res = await fetch("/api/session/create", { method: "POST" });
  const data = await res.json();
  if (data.code) {
    setSessionCode(data.code);
    joinUrlEl.textContent = `${location.origin}${data.joinUrl}`;
  }
}

function setSessionCode(code) {
  currentCode = code.trim().toUpperCase();
  sessionCodeInput.value = currentCode;
  localStorage.setItem("trackerSession", currentCode);
  startPolling();
}

function initFromStorage() {
  const stored = localStorage.getItem("trackerSession");
  if (stored) {
    setSessionCode(stored);
    joinUrlEl.textContent = `${location.origin}/session/${stored}`;
  }
}

createBtn?.addEventListener("click", createSession);
connectBtn?.addEventListener("click", () => {
  if (sessionCodeInput.value) {
    setSessionCode(sessionCodeInput.value);
    joinUrlEl.textContent = `${location.origin}/session/${currentCode}`;
  }
});
copyBtn?.addEventListener("click", async () => {
  const text = joinUrlEl.textContent;
  if (text.startsWith("http")) await navigator.clipboard.writeText(text);
});

initFromStorage();