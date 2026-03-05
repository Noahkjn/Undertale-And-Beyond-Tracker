const STATUS_STALE_SECONDS = 6;
const statusEl = document.getElementById("status");
const updatedEl = document.getElementById("updated-at");
const rawPayloadEl = document.getElementById("raw-payload");

const statMap = {
  hp: document.getElementById("stat-hp"),
  lv: document.getElementById("stat-lv"),
  exp: document.getElementById("stat-exp"),
  gold: document.getElementById("stat-gold"),
  playtime: document.getElementById("stat-playtime"),
  fun_value: document.getElementById("stat-fun-value"),
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
  if (ts === null || ts === undefined) return "No data yet";
  return `Last update: ${new Date(ts * 1000).toLocaleTimeString()}`;
}
function val(v) {
  return v !== null && v !== undefined ? v : "--";
}
function renderPayload(payload) {
  statMap.hp.textContent = val(payload.hp);
  statMap.lv.textContent = val(payload.lv);
  statMap.exp.textContent = val(payload.exp);
  statMap.gold.textContent = val(payload.gold);
  statMap.playtime.textContent = val(payload.playtime);
  statMap.fun_value.textContent = val(payload.fun_value);
  statMap.location.textContent = val(payload.location);
  const items = Array.isArray(payload.items) ? payload.items.join(", ") : payload.items;
  statMap.items.textContent = val(items);
  rawPayloadEl.textContent = JSON.stringify(payload, null, 2);
}

async function fetchState() {
  if (!currentCode) return;
  try {
    const res = await fetch(`/api/state?code=${currentCode}`);
    if (!res.ok) return setStatus("Disconnected", true);
    const data = await res.json();
    renderPayload(data.payload || {});
    const ts = data.lastUpdated !== null && data.lastUpdated !== undefined ? data.lastUpdated : null;
    updatedEl.textContent = formatUpdated(ts);
    const age = Math.floor(Date.now() / 1000) - (ts !== null ? ts : Math.floor(Date.now() / 1000));
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

async function initSession() {
  // Try the most-recently-active session
  try {
    const res = await fetch("/api/sessions/latest");
    if (res.ok) {
      const data = await res.json();
      if (data.code) {
        currentCode = data.code;
        startPolling();
        return;
      }
    }
  } catch { /* ignore */ }

  // No session exists yet — create one automatically
  try {
    const res = await fetch("/api/session/create", { method: "POST" });
    if (res.ok) {
      const data = await res.json();
      if (data.code) {
        currentCode = data.code;
        startPolling();
        return;
      }
    }
  } catch { /* ignore */ }

  setStatus("Disconnected", true);
}

initSession();
