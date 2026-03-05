const STATUS_STALE_SECONDS = 6;
const statusEl = document.getElementById("status");
const updatedEl = document.getElementById("updated-at");
const sessionDisplayEl = document.getElementById("session-display");
const rawPayloadEl = document.getElementById("raw-payload");

const statMap = {
  name:     document.getElementById("stat-name"),
  hp:       document.getElementById("stat-hp"),
  maxhp:    document.getElementById("stat-maxhp"),
  lv:       document.getElementById("stat-lv"),
  exp:      document.getElementById("stat-exp"),
  gold:     document.getElementById("stat-gold"),
  at:       document.getElementById("stat-at"),
  df:       document.getElementById("stat-df"),
  weapon:   document.getElementById("stat-weapon"),
  armor:    document.getElementById("stat-armor"),
  area:     document.getElementById("stat-area"),
  location: document.getElementById("stat-location"),
  route:    document.getElementById("stat-route"),
  kills:    document.getElementById("stat-kills"),
  playtime: document.getElementById("stat-playtime"),
  fun:      document.getElementById("stat-fun"),
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

function renderItemList(el, items) {
  if (!el) return;
  if (Array.isArray(items) && items.length > 0) {
    el.innerHTML = items.map(i => `<span class="item-tag">${i}</span>`).join("");
  } else {
    el.textContent = "(empty)";
  }
}

function renderIniData(el, iniData) {
  if (!el) return;
  if (!iniData || typeof iniData !== "object" || Object.keys(iniData).length === 0) {
    el.textContent = "(no INI data)";
    return;
  }
  let html = "";
  for (const [section, kvs] of Object.entries(iniData)) {
    html += `<div class="ini-section"><div class="ini-section-name">[${section}]</div>`;
    for (const [key, val] of Object.entries(kvs)) {
      html += `<div class="ini-row"><span class="ini-key">${key}</span><span class="ini-val">${val}</span></div>`;
    }
    html += "</div>";
  }
  el.innerHTML = html;
}

function renderPayload(payload) {
  statMap.name.textContent     = payload.name     ?? "--";
  statMap.hp.textContent       = payload.hp       ?? "--";
  statMap.maxhp.textContent    = payload.maxhp    ?? "--";
  statMap.lv.textContent       = payload.lv       ?? "--";
  statMap.exp.textContent      = payload.exp      ?? "--";
  statMap.gold.textContent     = payload.gold     ?? "--";
  statMap.at.textContent       = payload.at       ?? "--";
  statMap.df.textContent       = payload.df       ?? "--";
  statMap.weapon.textContent   = payload.weapon   ?? "--";
  statMap.armor.textContent    = payload.armor    ?? "--";
  statMap.area.textContent     = payload.area     ?? "--";
  statMap.location.textContent = payload.location ?? "--";

  const routeEl = statMap.route;
  if (routeEl) {
    routeEl.textContent = payload.route ?? "--";
    routeEl.className = "value route-" + (payload.route || "neutral").toLowerCase();
  }

  statMap.kills.textContent    = payload.kills    ?? "--";
  statMap.playtime.textContent = payload.playtime_formatted ?? payload.playtime ?? "--";
  statMap.fun.textContent      = payload.fun_value ?? "--";

  // Inventory
  renderItemList(document.getElementById("stat-items"), payload.items);

  // Storage boxes
  renderItemList(document.getElementById("stat-box-a"), payload.box_a);
  renderItemList(document.getElementById("stat-box-b"), payload.box_b);
  renderItemList(document.getElementById("stat-box-c"), payload.box_c);
  renderItemList(document.getElementById("stat-box-d"), payload.box_d);
  renderItemList(document.getElementById("stat-box-e"), payload.box_e);

  // INI data
  renderIniData(document.getElementById("stat-ini"), payload.ini_data);

  // Raw payload (omit raw_lines to keep it readable)
  const displayPayload = Object.fromEntries(
    Object.entries(payload).filter(([k]) => k !== "raw_lines" && k !== "flags")
  );
  rawPayloadEl.textContent = JSON.stringify(displayPayload, null, 2);
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
    if (data.lastUpdated) {
      setStatus(age > STATUS_STALE_SECONDS ? "Not updating" : "Live", age > STATUS_STALE_SECONDS);
    } else {
      setStatus("Waiting for data...", false);
    }
  } catch {
    setStatus("Disconnected", true);
  }
}

function startPolling() {
  if (pollTimer) clearInterval(pollTimer);
  pollTimer = setInterval(fetchState, 1000);
  fetchState();
}

function setSessionCode(code) {
  currentCode = code.trim().toUpperCase();
  if (sessionDisplayEl) sessionDisplayEl.textContent = currentCode;
  localStorage.setItem("trackerSession", currentCode);
  startPolling();
}

async function init() {
  // Try the most recently created session on the server first
  try {
    const res = await fetch("/api/sessions/latest");
    if (res.ok) {
      const data = await res.json();
      if (data.code) {
        setSessionCode(data.code);
        return;
      }
    }
  } catch {
    // fall through to create a new session
  }

  // No existing session — create one automatically
  try {
    const res = await fetch("/api/session/create", { method: "POST" });
    const data = await res.json();
    if (data.code) {
      setSessionCode(data.code);
    }
  } catch {
    setStatus("Disconnected", true);
    if (sessionDisplayEl) sessionDisplayEl.textContent = "Error";
  }
}

init();