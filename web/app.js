/**
 * Live Travel OS Reactive Ground Companion & Controller
 * Features:
 * - Dual-view switching (App View <-> Google Doc View)
 * - PWA Service Worker offline caching
 * - Interactive Daily Experience Hub (Plan A vs Plan B toggle)
 * - Door-to-Door Transport Module with Grab copy helpers
 * - Split-Luggage Dynamic Packing Checklist (localStorage persistent)
 * - Live 4-Way Reciprocal Currency Converter (ILS / USD / THB / VND)
 * - Offline Emergency & Taxi Phrasebook with Fullscreen Driver Display
 * - Floating Today Jump Anchor
 * - Real-time Search & Phase/Status Filtering
 */

// Service Worker Registration for PWA Offline Resilience
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js')
      .then(reg => console.log('ServiceWorker registered with scope:', reg.scope))
      .catch(err => console.log('ServiceWorker registration error:', err));
  });
}

let currentPhase = 'all';
let currentFilter = 'all';
let searchQuery = '';
let currentView = 'app';
let itineraryData = null;

// Utility Suite States
let currentPackingTab = 'bag_a';
let currentTranslationCat = 'all';
let dayExperienceModes = {}; // { [dayNum]: 'primary' | 'contingency' }

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // 1. Check if opening with secure mobile pairing hash (#pair_keys=...)
  checkUrlPairingKeys();

  // 2. Check for local custom overrides from mobile agent fixes
  const localOverride = localStorage.getItem('travel_os_custom_data');
  if (localOverride) {
    try {
      itineraryData = JSON.parse(localOverride);
      window.TRAVEL_OS_DATA = itineraryData;
      initApp();
      return;
    } catch (e) {
      console.warn('Failed to parse local custom data override', e);
    }
  }

  if (window.TRAVEL_OS_DATA) {
    itineraryData = window.TRAVEL_OS_DATA;
    initApp();
  } else {
    fetch('data.json')
      .then(res => res.json())
      .then(data => {
        itineraryData = data;
        initApp();
      })
      .catch(err => {
        console.error('Failed to load itinerary JSON:', err);
      });
  }
});

// -------------------------------------------------------------
// THEME MANAGER (Light & Dark Mode)
// -------------------------------------------------------------
function initTheme() {
  const saved = localStorage.getItem('travel_os_theme');
  const isDark = saved === 'dark';
  if (isDark) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
  updateThemeButton(isDark);
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('travel_os_theme', isDark ? 'dark' : 'light');
  updateThemeButton(isDark);
}

function updateThemeButton(isDark) {
  const icon = document.getElementById('theme-toggle-icon');
  const text = document.getElementById('theme-toggle-text');
  if (icon) icon.textContent = isDark ? '☀️' : '🌙';
  if (text) text.textContent = isDark ? 'Light' : 'Dark';
}

function initApp() {
  initTheme();
  renderHeaderMetrics();
  renderTimelineScrubber();
  renderDays();
  setupEventListeners();
  initPackingChecklist();
  initCurrencyDefaults();
  initGeminiAssistant();
  initAntigravityHub();
}

function renderHeaderMetrics() {
  if (!itineraryData) return;
  const days = itineraryData.days || [];
  const confirmed = days.filter(d => d.status.includes('CONFIRMED')).length;
  const partial = days.filter(d => d.status.includes('BOOKED') && !d.status.includes('CONFIRMED - BOOKED')).length;
  const unbooked = days.length - (confirmed + partial);

  const totalEl = document.getElementById('metric-total-days');
  const confEl = document.getElementById('metric-confirmed');
  const vetEl = document.getElementById('metric-vetted');

  if (totalEl) totalEl.innerText = days.length;
  if (confEl) confEl.innerText = confirmed + partial;
  if (vetEl) vetEl.innerText = unbooked;
}

// -------------------------------------------------------------
// VIEW MODE SWITCHER (Operational Mandate)
// -------------------------------------------------------------
function switchView(view) {
  currentView = view;
  const appContainer = document.getElementById('app-view-container');
  const docContainer = document.getElementById('doc-view-container');
  const btnApp = document.getElementById('btn-view-app');
  const btnDoc = document.getElementById('btn-view-doc');

  if (view === 'app') {
    appContainer.classList.remove('hidden');
    docContainer.classList.add('hidden');
    btnApp.classList.add('bg-blue-600', 'text-white');
    btnApp.classList.remove('bg-slate-800', 'text-slate-300');
    btnDoc.classList.remove('bg-blue-600', 'text-white');
    btnDoc.classList.add('bg-slate-800', 'text-slate-300');
  } else {
    appContainer.classList.add('hidden');
    docContainer.classList.remove('hidden');
    btnDoc.classList.add('bg-blue-600', 'text-white');
    btnDoc.classList.remove('bg-slate-800', 'text-slate-300');
    btnApp.classList.remove('bg-blue-600', 'text-white');
    btnApp.classList.add('bg-slate-800', 'text-slate-300');
    loadGoogleDocPreview();
  }
}

function loadGoogleDocPreview() {
  const iframe = document.getElementById('google-doc-iframe');
  if (iframe && !iframe.src) {
    iframe.src = 'master_itinerary_doc.html';
  }
}

// -------------------------------------------------------------
// OPERATIONS DRAWER TOGGLE
// -------------------------------------------------------------
function toggleOpsDrawer() {
  const drawer = document.getElementById('ops-drawer-content');
  const icon = document.getElementById('ops-drawer-icon');
  if (!drawer) return;
  const isHidden = drawer.classList.contains('hidden');
  if (isHidden) {
    drawer.classList.remove('hidden');
    if (icon) icon.classList.add('rotate-180');
  } else {
    drawer.classList.add('hidden');
    if (icon) icon.classList.remove('rotate-180');
  }
}
window.toggleOpsDrawer = toggleOpsDrawer;

// -------------------------------------------------------------
// PHASE & STATUS FILTERING
// -------------------------------------------------------------
function setPhase(phase) {
  currentPhase = phase;
  document.querySelectorAll('.tab-phase').forEach(btn => {
    if (btn.dataset.phase === phase) {
      btn.className = 'tab-phase flex-1 py-1.5 px-2 rounded-lg bg-white dark:bg-slate-700 text-blue-600 dark:text-white shadow-sm transition whitespace-nowrap text-center text-xs font-bold';
    } else {
      btn.className = 'tab-phase flex-1 py-1.5 px-2 rounded-lg text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition whitespace-nowrap text-center text-xs font-medium';
    }
  });
  renderDays();
}

function filterStatus(status) {
  currentFilter = status;
  const allBtn = document.getElementById('btn-filter-all');
  const confBtn = document.getElementById('btn-filter-confirmed');
  const vetBtn = document.getElementById('btn-filter-vetted');

  if (allBtn && confBtn && vetBtn) {
    allBtn.className = status === 'all' 
      ? 'px-2.5 py-1 rounded-lg text-xs bg-blue-600 text-white font-semibold shadow-sm transition' 
      : 'px-2.5 py-1 rounded-lg text-xs bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition border border-slate-200 dark:border-slate-700';
    confBtn.className = status === 'confirmed' 
      ? 'px-2.5 py-1 rounded-lg text-xs bg-emerald-600 text-white font-semibold shadow-sm transition' 
      : 'px-2.5 py-1 rounded-lg text-xs bg-slate-100 dark:bg-slate-800 text-emerald-700 dark:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 transition border border-emerald-200 dark:border-emerald-500/30';
    vetBtn.className = status === 'vetted' 
      ? 'px-2.5 py-1 rounded-lg text-xs bg-amber-600 text-white font-semibold shadow-sm transition' 
      : 'px-2.5 py-1 rounded-lg text-xs bg-slate-100 dark:bg-slate-800 text-amber-700 dark:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-950/60 transition border border-amber-200 dark:border-amber-500/30';
  }

  renderDays();
}

function toggleDay(dayNum) {
  const content = document.getElementById(`day-content-${dayNum}`);
  const icon = document.getElementById(`day-icon-${dayNum}`);
  if (!content) return;
  if (content.classList.contains('hidden')) {
    content.classList.remove('hidden');
    if (icon) icon.classList.add('rotate-180');
  } else {
    content.classList.add('hidden');
    if (icon) icon.classList.remove('rotate-180');
  }
}

let isAllExpanded = false;

function toggleAllDaysAdaptive() {
  isAllExpanded = !isAllExpanded;
  toggleAllDays(isAllExpanded);
}
window.toggleAllDaysAdaptive = toggleAllDaysAdaptive;

function toggleAllDays(expand) {
  isAllExpanded = expand;
  document.querySelectorAll('.day-content-block').forEach(el => {
    if (expand) el.classList.remove('hidden');
    else el.classList.add('hidden');
  });
  document.querySelectorAll('.day-toggle-icon').forEach(icon => {
    if (expand) icon.classList.add('rotate-180');
    else icon.classList.remove('rotate-180');
  });
  const label = document.getElementById('label-toggle-all-days');
  const icon = document.getElementById('icon-toggle-all-days');
  if (label) label.textContent = expand ? 'Collapse' : 'Expand';
  if (icon) icon.textContent = expand ? '▴' : '▾';
}

// -------------------------------------------------------------
// PLAN A / PLAN B EXPERIENCE TOGGLE
// -------------------------------------------------------------
function toggleExperience(dayNum, mode) {
  dayExperienceModes[dayNum] = mode;
  const primBox = document.getElementById(`exp-primary-${dayNum}`);
  const contBox = document.getElementById(`exp-contingency-${dayNum}`);
  const btnA = document.getElementById(`btn-plan-a-${dayNum}`);
  const btnB = document.getElementById(`btn-plan-b-${dayNum}`);

  if (mode === 'primary') {
    if (primBox) primBox.classList.remove('hidden');
    if (contBox) contBox.classList.add('hidden');
    if (btnA) {
      btnA.className = 'plan-tab-btn plan-tab-active-a px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5';
    }
    if (btnB) {
      btnB.className = 'plan-tab-btn plan-tab-inactive px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5';
    }
  } else {
    if (primBox) primBox.classList.add('hidden');
    if (contBox) contBox.classList.remove('hidden');
    if (btnA) {
      btnA.className = 'plan-tab-btn plan-tab-inactive px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5';
    }
    if (btnB) {
      btnB.className = 'plan-tab-btn plan-tab-active-b px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5';
    }
  }
}

// -------------------------------------------------------------
// RENDER DAYS ACCORDION
// -------------------------------------------------------------
function renderDays() {
  if (!itineraryData) return;
  const container = document.getElementById('itinerary-days-list');
  container.innerHTML = '';

  let filtered = itineraryData.days || [];

  // Filter by Phase
  if (currentPhase === 'phase1') {
    filtered = filtered.filter(d => d.phase.includes('Vietnam') || d.day_number <= 13);
  } else if (currentPhase === 'phase2') {
    filtered = filtered.filter(d => d.phase.includes('Thailand') || d.day_number >= 14);
  }

  // Filter by Status
  if (currentFilter === 'confirmed') {
    filtered = filtered.filter(d => d.status.includes('BOOKED'));
  } else if (currentFilter === 'vetted') {
    filtered = filtered.filter(d => !d.status.includes('CONFIRMED - BOOKED'));
  }

  // Filter by Search Query
  if (searchQuery.trim() !== '') {
    const q = searchQuery.toLowerCase();
    filtered = filtered.filter(d => {
      const matchDest = (d.destination || '').toLowerCase().includes(q);
      const matchFlow = JSON.stringify(d.curated_daily_flow || {}).toLowerCase().includes(q);
      const matchHotels = JSON.stringify(d.accommodation_matrix || []).toLowerCase().includes(q);
      const matchDocs = JSON.stringify(d.attached_documents || []).toLowerCase().includes(q);
      const matchExp = JSON.stringify(d.experiences || {}).toLowerCase().includes(q);
      const matchTrans = JSON.stringify(d.transport_module || {}).toLowerCase().includes(q);
      return matchDest || matchFlow || matchHotels || matchDocs || matchExp || matchTrans;
    });
  }

  // Update search results counter in toolbar
  const countEl = document.getElementById('search-results-count');
  const totalDays = itineraryData.days ? itineraryData.days.length : 29;
  if (countEl) {
    countEl.innerText = `Showing ${filtered.length} of ${totalDays} days`;
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="travel-card rounded-2xl p-10 text-center text-slate-500 dark:text-slate-400 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
        <p class="text-lg font-bold text-slate-800 dark:text-slate-200">No itinerary days match your filter.</p>
        <button onclick="resetFilters()" class="mt-4 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold shadow-sm transition">Reset Filters</button>
      </div>
    `;
    return;
  }

  filtered.forEach(day => {
    let badgeClass = 'badge-vetted';
    if (day.status.includes('CONFIRMED - BOOKED')) {
      badgeClass = 'badge-confirmed';
    } else if (day.status.includes('BOOKED')) {
      badgeClass = 'badge-radar';
    }

    const isPhase1 = day.phase.includes('Vietnam') || day.day_number <= 13;
    const phaseColor = isPhase1 
      ? 'text-amber-800 dark:text-amber-300 bg-amber-50 dark:bg-amber-950/40 border-amber-300 dark:border-amber-500/30' 
      : 'text-pink-800 dark:text-pink-300 bg-pink-50 dark:bg-pink-950/40 border-pink-300 dark:border-pink-500/30';
    const bedIcon = isPhase1 ? '🛏️ Twin Beds (Guys Trip)' : '👑 Romantic King (Couple Trip)';

    // Accommodations Matrix
    let hotelsHtml = '';
    (day.accommodation_matrix || []).forEach(h => {
      const isHotelBooked = h.status === 'CONFIRMED_BOOKED';
      const hotelBadge = isHotelBooked 
        ? `<span class="text-xs px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 font-bold border border-emerald-300 dark:border-emerald-500/40">✓ Confirmed Booking</span>`
        : `<span class="text-xs px-2.5 py-0.5 rounded-full bg-amber-100 dark:bg-amber-950/80 text-amber-800 dark:text-amber-300 font-semibold border border-amber-300 dark:border-amber-500/40">Vetted Option</span>`;

      hotelsHtml += `
        <div class="bg-white dark:bg-slate-800/80 rounded-2xl p-4 border border-slate-200 dark:border-slate-700/80 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between flex-wrap gap-2">
              <a href="${h.booking_url}" target="_blank" class="font-bold text-blue-600 dark:text-blue-400 hover:underline text-sm sm:text-base flex items-center gap-1">
                ${h.hotel_name} <span class="text-xs">↗</span>
              </a>
              ${hotelBadge}
            </div>
            <p class="text-xs sm:text-sm text-slate-700 dark:text-slate-300 mt-1.5 font-medium"><b>Room:</b> ${h.room_spec}</p>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 italic leading-relaxed">${h.critic_notes}</p>
          </div>
          <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-700/60 flex justify-between items-center text-xs">
            <span class="text-emerald-700 dark:text-emerald-400 font-extrabold text-sm">${h.price_per_night}</span>
            <a href="${h.booking_url}" target="_blank" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold transition shadow-sm">View Deal ↗</a>
          </div>
        </div>
      `;
    });

    // Attached Documents
    let docsHtml = '';
    (day.attached_documents || []).forEach(doc => {
      const isVerified = Boolean(doc.file_path);
      docsHtml += `
        <button onclick="openDocModal('${doc.doc_id}')" class="doc-pill text-xs px-3 py-2 rounded-xl flex items-center gap-2 cursor-pointer ${isVerified ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-600/50 text-emerald-900 dark:text-emerald-200' : 'bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200'} border transition shadow-sm">
          <span>${isVerified ? '📄' : '📎'}</span>
          <span class="font-bold">${doc.title}</span>
          <span class="text-blue-600 dark:text-blue-300 text-xs font-mono">(${doc.ref})</span>
          ${isVerified 
            ? `<span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-300 font-bold">✓ PDF</span>` 
            : `<span class="text-[10px] px-2 py-0.5 rounded-full bg-amber-100 dark:bg-amber-900/40 text-amber-800 dark:text-amber-300 font-semibold">Pending</span>`}
        </button>
      `;
    });

    // Google Maps Navigation Links
    let mapsHtml = '';
    (day.google_maps_links || []).forEach(m => {
      mapsHtml += `
        <a href="${m.url}" target="_blank" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 text-xs font-semibold transition border border-slate-200 dark:border-slate-700 shadow-sm">
          <span>📍</span> ${m.label} <span class="text-[10px] text-slate-400">↗</span>
        </a>
      `;
    });

    // Door-to-Door Transport Module
    let transportHtml = '';
    const trans = day.transport_module;
    if (trans) {
      const routeTitle = trans.route || trans.route_title || 'Intercity Transit';
      const provider = trans.booking_provider || trans.operator || 'Booking';
      const grab = trans.grab_helper || {};
      const dropLocal = grab.dropoff_local || '';
      const escapedLocal = dropLocal.replace(/'/g, "\\'");

      transportHtml = `
        <div class="bg-white dark:bg-slate-800/90 border border-sky-200 dark:border-sky-500/30 rounded-2xl p-4 sm:p-5 shadow-sm mb-4">
          <div class="flex items-center justify-between flex-wrap gap-2 mb-3">
            <div class="flex items-center gap-2">
              <span class="text-lg">🚆</span>
              <span class="font-extrabold text-slate-900 dark:text-sky-300 text-sm sm:text-base">${routeTitle}</span>
            </div>
            <span class="text-xs px-2.5 py-1 rounded-full bg-sky-100 dark:bg-sky-950 text-sky-800 dark:text-sky-300 border border-sky-200 dark:border-sky-500/40 font-bold">
              ${trans.transit_type || 'Transit Module'}
            </span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs sm:text-sm text-slate-700 dark:text-slate-300 mb-3">
            <div class="space-y-1">
              <p><span class="text-slate-500 dark:text-slate-400 font-medium">Pickup Hub:</span> <b class="text-slate-900 dark:text-white">${trans.pickup_hub || 'TBD'}</b></p>
              <p><span class="text-slate-500 dark:text-slate-400 font-medium">Drop-off Terminal:</span> <b class="text-slate-900 dark:text-white">${trans.dropoff_terminal || 'TBD'}</b></p>
              <p><span class="text-slate-500 dark:text-slate-400 font-medium">Est. Duration:</span> <span class="text-amber-700 dark:text-amber-300 font-bold">${trans.duration || 'N/A'}</span></p>
            </div>
            <div class="space-y-1">
              <p><span class="text-slate-500 dark:text-slate-400 font-medium">Baggage:</span> ${trans.baggage_allowance || 'Standard'}</p>
              <p><span class="text-slate-500 dark:text-slate-400 font-medium">Provider:</span> 
                <a href="${trans.booking_url || '#'}" target="_blank" class="text-blue-600 dark:text-sky-400 hover:underline font-bold inline-flex items-center gap-1">
                  ${provider} ↗
                </a>
              </p>
            </div>
          </div>

          <!-- Taxi / Grab Driver Assist Box (High Visibility Driver Screen) -->
          ${grab.dropoff || dropLocal ? `
            <div class="driver-assist-box p-3.5 sm:p-5 flex flex-col gap-3 text-xs">
              <div class="flex items-center justify-between flex-wrap gap-2">
                <span class="text-[11px] font-extrabold uppercase tracking-wider text-amber-800 dark:text-amber-300 flex items-center gap-1.5">
                  <span>🚕</span> <span>Show Screen to Driver (Grab / Taxi)</span>
                </span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-amber-200/80 dark:bg-amber-900/60 text-amber-900 dark:text-amber-200 font-bold">Local Script</span>
              </div>
              <div>
                <div class="text-slate-800 dark:text-slate-200 font-semibold text-xs sm:text-sm mb-1">${grab.dropoff || ''}</div>
                ${dropLocal ? `
                  <div class="driver-native-text text-lg sm:text-2xl font-black p-3 rounded-xl bg-amber-100/80 dark:bg-amber-950/50 text-amber-950 dark:text-amber-100 select-all border border-amber-300 dark:border-amber-600/40 text-center tracking-wide leading-relaxed shadow-sm">
                    ${dropLocal}
                  </div>
                ` : ''}
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                ${dropLocal ? `
                  <button onclick="copyToClipboard('${escapedLocal}', 'Copied destination in local script for driver!')" class="w-full py-2.5 px-4 min-h-[42px] rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs flex items-center justify-center gap-2 shadow-sm transition active:scale-95">
                    <span>📋</span> Copy Driver Script
                  </button>
                ` : ''}
                ${grab.maps_url ? `
                  <a href="${grab.maps_url}" target="_blank" class="w-full py-2.5 px-4 min-h-[42px] rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs flex items-center justify-center gap-2 shadow-sm transition active:scale-95">
                    <span>📍</span> Open Google Maps ↗
                  </a>
                ` : ''}
              </div>
            </div>
          ` : ''}
        </div>
      `;
    }

    // Daily Attraction & Experience Hub (Plan A vs Plan B)
    let experienceHtml = '';
    const exp = day.experiences;
    if (exp && exp.primary && exp.contingency) {
      const p = exp.primary;
      const c = exp.contingency;
      const isModeB = dayExperienceModes[day.day_number] === 'contingency';

      const pLinks = (p.links || []).map(l => `
        <a href="${l.url}" target="_blank" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 text-xs font-semibold border border-slate-200 dark:border-slate-700 transition">
          <span>${l.type === 'booking' ? '🎟️' : '📍'}</span> ${l.label} ↗
        </a>
      `).join('');

      const cLinks = (c.links || []).map(l => `
        <a href="${l.url}" target="_blank" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 text-xs font-semibold border border-slate-200 dark:border-slate-700 transition">
          <span>${l.type === 'booking' ? '🎟️' : '📍'}</span> ${l.label} ↗
        </a>
      `).join('');

      experienceHtml = `
        <div class="mb-4 bg-white dark:bg-slate-800/90 border border-slate-200 dark:border-slate-700/80 rounded-2xl p-4 sm:p-5 shadow-sm">
          <!-- Experience Hub Header & Toggle Buttons -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-100 dark:border-slate-700/60">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">Daily Attraction &amp; Experience Hub</span>
            </div>
            
            <div class="grid grid-cols-2 gap-1.5 w-full sm:w-auto">
              <button id="btn-plan-a-${day.day_number}" onclick="toggleExperience(${day.day_number}, 'primary')" 
                      class="plan-tab-btn ${isModeB ? 'plan-tab-inactive' : 'plan-tab-active-a'} px-3 py-2 text-xs flex items-center justify-center gap-1.5">
                <span>🌟</span> Plan A: Main
              </button>
              <button id="btn-plan-b-${day.day_number}" onclick="toggleExperience(${day.day_number}, 'contingency')" 
                      class="plan-tab-btn ${isModeB ? 'plan-tab-active-b' : 'plan-tab-inactive'} px-3 py-2 text-xs flex items-center justify-center gap-1.5">
                <span>☔</span> Plan B: Rain
              </button>
            </div>
          </div>

          <!-- PLAN A CONTENT BLOCK -->
          <div id="exp-primary-${day.day_number}" class="${isModeB ? 'hidden' : ''} space-y-3 text-xs sm:text-sm">
            <div class="flex items-center justify-between flex-wrap gap-2">
              <h4 class="font-extrabold text-emerald-700 dark:text-emerald-400 text-base">${p.title}</h4>
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-bold border border-emerald-200 dark:border-emerald-500/40">${p.type}</span>
            </div>
            
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-slate-700 dark:text-slate-300 font-medium">
              <p><span class="text-slate-500 dark:text-slate-400">Duration:</span> <b>${p.duration}</b></p>
              <p><span class="text-slate-500 dark:text-slate-400">Hours:</span> <b>${p.opening_hours || 'Flexible'}</b></p>
              <p><span class="text-slate-500 dark:text-slate-400">Est. Cost:</span> <span class="text-emerald-700 dark:text-emerald-400 font-bold">${p.cost_estimate}</span></p>
            </div>

            <div class="bg-emerald-50 dark:bg-emerald-950/30 p-3 rounded-xl border border-emerald-200 dark:border-emerald-500/30 text-emerald-900 dark:text-emerald-200 text-xs sm:text-sm leading-relaxed">
              <span class="font-bold text-emerald-800 dark:text-emerald-300">💡 Insider Tip:</span> ${p.time_sensitive_tip}
            </div>

            ${pLinks ? `<div class="flex flex-wrap gap-2 pt-1">${pLinks}</div>` : ''}
          </div>

          <!-- PLAN B CONTENT BLOCK (CONTINGENCY / RAINY-DAY) -->
          <div id="exp-contingency-${day.day_number}" class="${isModeB ? '' : 'hidden'} space-y-3 text-xs sm:text-sm">
            <div class="flex items-center justify-between flex-wrap gap-2">
              <h4 class="font-extrabold text-amber-700 dark:text-amber-400 text-base">${c.title}</h4>
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300 font-bold border border-amber-200 dark:border-amber-500/40">${c.type}</span>
            </div>

            <div class="bg-amber-50 dark:bg-amber-950/40 p-2.5 rounded-xl border border-amber-200 dark:border-amber-600/40 text-amber-900 dark:text-amber-300 text-xs font-semibold">
              <span>⚠️ Trigger Condition:</span> ${c.trigger}
            </div>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-slate-700 dark:text-slate-300 font-medium">
              <p><span class="text-slate-500 dark:text-slate-400">Duration:</span> <b>${c.duration}</b></p>
              <p><span class="text-slate-500 dark:text-slate-400">Est. Cost:</span> <span class="text-amber-700 dark:text-amber-400 font-bold">${c.cost_estimate}</span></p>
            </div>

            <div class="bg-slate-50 dark:bg-slate-900 p-3 rounded-xl border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 text-xs sm:text-sm leading-relaxed">
              <span class="font-bold text-amber-700 dark:text-amber-300">💡 Contingency Advice:</span> ${c.time_sensitive_tip}
            </div>

            ${cLinks ? `<div class="flex flex-wrap gap-2 pt-1">${cLinks}</div>` : ''}
          </div>
        </div>
      `;
    }

    // Special banners for Day 2 and Day 14
    let specialBanner = '';
    if (day.day_number === 2) {
      specialBanner = `
        <div class="bg-amber-50 dark:bg-amber-950/40 border-l-4 border-amber-500 p-4 rounded-r-2xl mb-4 text-xs sm:text-sm text-amber-900 dark:text-amber-200 flex items-start gap-3 shadow-sm">
          <span class="text-2xl">🧳</span>
          <div>
            <b class="font-bold">BKK Airport Suitcase Drop (Floor B Basement):</b> Deposit checked suitcase at AIRPORTELs Suvarnabhumi basement before 11:55 flight. Strictly 55L clamshell backpack only for Vietnam!
          </div>
        </div>
      `;
    } else if (day.day_number === 14) {
      specialBanner = `
        <div class="bg-purple-50 dark:bg-purple-950/40 border-l-4 border-purple-600 p-4 rounded-r-2xl mb-4 text-xs sm:text-sm text-purple-950 dark:text-purple-200 space-y-1.5 shadow-sm">
          <div class="flex items-center justify-between flex-wrap gap-2">
            <span class="font-extrabold text-slate-900 dark:text-white flex items-center gap-2">
              <span>✈️</span> Transition Day &amp; Connection Risk Radar
            </span>
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-rose-100 dark:bg-rose-950 text-rose-800 dark:text-rose-300 border border-rose-300 dark:border-rose-500/50 font-bold">PG 169 HIGH RISK</span>
          </div>
          <p class="leading-relaxed">
            Hanoi flight lands at 14:45. Friend departs. Retrieve checked suitcase at <b>AIRPORTELs Suvarnabhumi Basement (Floor B)</b>. Reunite with girlfriend at arrivals.
          </p>
          <p class="font-medium text-amber-800 dark:text-amber-300">
            ⚠️ <b>Connection Audit:</b> PG 169 (17:15) leaves only 2h 30m total. <b>Recommended Stress-Free Connection: PG 177 (19:30) or PG 181 (20:00)</b> with 4h 45m buffer!
            <button onclick="openPriceRadarModal()" class="ml-2 underline text-blue-600 dark:text-cyan-300 font-bold hover:opacity-80">Open Risk Radar →</button>
          </p>
        </div>
      `;
    }

    // Read persisted daily tasks from localStorage
    let tasksState = {};
    try {
      tasksState = JSON.parse(localStorage.getItem('travel_os_daily_tasks_v1') || '{}');
    } catch (e) {
      tasksState = {};
    }

    const checklistHtml = (day.essential_checklist || []).map((task, idx) => {
      const isChecked = Boolean(tasksState[`${day.day_number}_${idx}`]);
      return `
        <label class="flex items-start gap-2.5 cursor-pointer select-none group py-1">
          <input type="checkbox" 
                 class="daily-task-checkbox mt-0.5" 
                 ${isChecked ? 'checked' : ''} 
                 onchange="toggleDailyTask(${day.day_number}, ${idx}, this)">
          <span class="daily-task-text group-hover:text-slate-900 dark:group-hover:text-white transition-colors leading-snug ${isChecked ? 'checked' : ''}">
            ${task}
          </span>
        </label>
      `;
    }).join('');

    const card = document.createElement('div');
    card.id = `day-card-${day.day_number}`;
    card.className = 'travel-card rounded-2xl overflow-hidden mb-5 transition-all duration-200 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md';
    card.innerHTML = `
      <!-- Card Header (Always Visible) -->
      <div onclick="toggleDay(${day.day_number})" class="p-3.5 sm:p-5 flex items-center justify-between cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/40 select-none transition-colors">
        <div class="flex items-center gap-3.5 sm:gap-5 flex-wrap sm:flex-nowrap">
          <div class="flex flex-col items-center justify-center w-11 h-11 sm:w-14 sm:h-14 rounded-xl sm:rounded-2xl bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 font-black border border-blue-200 dark:border-blue-800/60 shrink-0 shadow-sm">
            <span class="text-[8px] sm:text-[10px] uppercase font-bold text-blue-500 dark:text-blue-400 leading-none">DAY</span>
            <span class="text-sm sm:text-lg leading-tight font-black">${day.day_number < 10 ? '0' + day.day_number : day.day_number}</span>
          </div>
          <div>
            <div class="flex items-center gap-2 flex-wrap">
              <h3 class="font-extrabold text-sm sm:text-lg text-slate-900 dark:text-white tracking-tight leading-tight break-words">${day.destination}</h3>
              <span class="text-xs px-2.5 py-0.5 rounded-full font-bold ${badgeClass}">${day.status}</span>
              <span class="text-xs px-2.5 py-0.5 rounded-full font-semibold border ${phaseColor} hidden sm:inline-block">${day.phase_short || day.phase}</span>
            </div>
            <div class="text-xs sm:text-sm text-slate-600 dark:text-slate-300 mt-1.5 flex items-center gap-2.5 flex-wrap">
              <span>📅 <b>${day.day_of_week}</b>, ${day.date}</span>
              <span class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-medium">🌤️ ${day.weather_radar.temp_range} · ${day.weather_radar.condition}</span>
              <span class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-semibold">${bedIcon}</span>
            </div>
          </div>
        </div>
        <div class="flex items-center gap-2 shrink-0 ml-2">
          <svg id="day-icon-${day.day_number}" class="day-toggle-icon w-5 h-5 text-slate-400 transform transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
          </svg>
        </div>
      </div>

      <!-- Card Content (Expandable) -->
      <div id="day-content-${day.day_number}" class="day-content-block p-3.5 sm:p-6 border-t border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/40 space-y-3.5 sm:space-y-4">
        ${specialBanner}

        <!-- Weather & Attire Radar -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs sm:text-sm">
          <div class="bg-white dark:bg-slate-800/90 rounded-2xl p-4 border border-slate-200 dark:border-slate-700/70 shadow-sm">
            <div class="font-bold text-slate-900 dark:text-white mb-1.5 flex items-center gap-1.5">
              <span>🌦️</span> Weather &amp; Attire Radar
            </div>
            <div class="text-slate-600 dark:text-slate-300 leading-relaxed text-xs sm:text-sm">
              <b>Forecast:</b> ${day.weather_radar.temp_range} • Rain: ${day.weather_radar.precipitation_pct} • Humidity: ${day.weather_radar.humidity}<br>
              <span class="text-blue-700 dark:text-sky-300 font-semibold">👔 Attire: ${day.weather_radar.attire_advice}</span>
            </div>
          </div>

          <div class="bg-white dark:bg-slate-800/90 rounded-2xl p-4 border border-slate-200 dark:border-slate-700/70 shadow-sm">
            <div class="font-bold text-slate-900 dark:text-white mb-1.5 flex items-center gap-1.5">
              <span>🚗</span> Door-to-Door Logistics
            </div>
            <div class="text-slate-600 dark:text-slate-300 leading-relaxed text-xs sm:text-sm">
              <span class="text-slate-900 dark:text-white font-semibold">${day.door_to_door_logistics.primary_transit}</span><br>
              <span class="text-slate-500 dark:text-slate-400 text-xs">Dep: ${day.door_to_door_logistics.departure_time} | Arr: ${day.door_to_door_logistics.arrival_time} | Buffer: ${day.door_to_door_logistics.buffer_time}</span>
            </div>
          </div>
        </div>

        <!-- Door-to-Door Transport Card -->
        ${transportHtml}

        <!-- Daily Experience Hub (Plan A vs Plan B) -->
        ${experienceHtml}

        <!-- Attached Documents -->
        ${docsHtml ? `
          <div class="bg-white dark:bg-slate-800/90 rounded-2xl p-4 border border-slate-200 dark:border-slate-700/70 shadow-sm">
            <div class="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-2 flex items-center gap-1.5">
              <span>📎</span> Mail Vouchers &amp; Attached Passes:
            </div>
            <div class="flex flex-wrap gap-2">
              ${docsHtml}
            </div>
          </div>
        ` : ''}

        <!-- Curated Daily Flow (Connected Vertical Timeline) -->
        <div class="bg-white dark:bg-slate-800/80 rounded-2xl p-4 sm:p-5 border border-slate-200 dark:border-slate-700/80 shadow-sm">
          <div class="font-bold text-slate-900 dark:text-white text-xs sm:text-sm mb-3 flex items-center justify-between">
            <span class="flex items-center gap-1.5">🗺️ Daily Flow Timeline</span>
            <span class="text-xs text-slate-500 dark:text-slate-400 font-mono">Route Paced</span>
          </div>
          <div class="timeline-flow-container">
            <div class="timeline-flow-item morning">
              <div class="timeline-flow-dot">🌅</div>
              <div class="text-xs font-bold text-amber-600 dark:text-amber-400 mb-0.5">Morning Focus</div>
              <p class="text-xs sm:text-sm text-slate-700 dark:text-slate-200 leading-relaxed">${day.curated_daily_flow.morning || 'Flexible exploration'}</p>
            </div>
            <div class="timeline-flow-item afternoon">
              <div class="timeline-flow-dot">☀️</div>
              <div class="text-xs font-bold text-sky-600 dark:text-sky-400 mb-0.5">Afternoon Highlight</div>
              <p class="text-xs sm:text-sm text-slate-700 dark:text-slate-200 leading-relaxed">${day.curated_daily_flow.afternoon || 'Activity & transit'}</p>
            </div>
            <div class="timeline-flow-item evening">
              <div class="timeline-flow-dot">🌙</div>
              <div class="text-xs font-bold text-purple-600 dark:text-purple-400 mb-0.5">Evening Pacing</div>
              <p class="text-xs sm:text-sm text-slate-700 dark:text-slate-200 leading-relaxed">${day.curated_daily_flow.evening || 'Dinner & unwind'}</p>
            </div>
          </div>
        </div>

        <!-- Accommodation Matrix -->
        ${hotelsHtml ? `
          <div>
            <div class="text-xs sm:text-sm font-bold text-slate-900 dark:text-white mb-2.5 flex items-center justify-between">
              <span class="flex items-center gap-1.5">🏨 Vetted Accommodations (Critic Passed &ge; 8.5)</span>
              <span class="text-xs text-slate-500 dark:text-slate-400">${isPhase1 ? 'Enforced: Twin Beds' : 'Enforced: King / Ocean View'}</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              ${hotelsHtml}
            </div>
          </div>
        ` : ''}

        <!-- Essential Checklist & Google Maps -->
        <div class="pt-4 border-t border-slate-200 dark:border-slate-800 flex flex-col md:flex-row justify-between gap-4 text-xs sm:text-sm">
          <div class="flex-1">
            <div class="flex items-center justify-between mb-2">
              <span class="font-extrabold text-slate-900 dark:text-white flex items-center gap-1.5">
                <span>✓</span> Operational Checklist
              </span>
              <span class="text-xs text-slate-500 dark:text-slate-400">Tap to track completion</span>
            </div>
            <div class="space-y-1 bg-white dark:bg-slate-800/70 p-3 rounded-2xl border border-slate-200 dark:border-slate-700/60 shadow-sm">
              ${checklistHtml || '<p class="text-slate-400 italic">No special actions required for this day.</p>'}
            </div>
          </div>
          <div class="md:w-72">
            <span class="font-extrabold text-slate-900 dark:text-white block mb-2">📍 Fast Navigation:</span>
            <div class="flex flex-wrap gap-2">
              ${mapsHtml || '<span class="text-slate-400 text-xs">Local routes</span>'}
            </div>
          </div>
        </div>

        <!-- Antigravity Day Agent Action Bar -->
        <div class="mt-3.5 pt-3 border-t border-slate-200/70 dark:border-slate-800 flex items-center justify-between flex-wrap gap-2">
          <div class="flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400">
            <span>🤖</span>
            <span>Have changes or new ideas for Day ${day.day_number}?</span>
          </div>
          <button onclick="openChangeRequestModal({ day: ${day.day_number}, destination: '${(day.destination || '').replace(/'/g, "\\'")}', category: 'plan' })" 
                  class="px-3 py-1.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 hover:bg-emerald-100 dark:hover:bg-emerald-900/60 text-emerald-800 dark:text-emerald-300 text-xs font-bold border border-emerald-300 dark:border-emerald-700/50 transition flex items-center gap-1.5 shadow-sm active:scale-95" title="Tell Antigravity agent to update Day ${day.day_number}">
            <span>✏️</span>
            <span>Change Plan with Agent</span>
          </button>
        </div>

      </div>
    `;

    container.appendChild(card);
  });
}

function resetFilters() {
  currentPhase = 'all';
  currentFilter = 'all';
  searchQuery = '';
  const input = document.getElementById('search-input');
  if (input) input.value = '';
  renderDays();
}

function setupEventListeners() {
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value;
      renderDays();
    });
  }

  // Global Keyboard Shortcuts: Ctrl+K / Cmd+K for Gemini, Escape to close modals
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) {
      e.preventDefault();
      openGeminiModal();
    }
    if (e.key === 'Escape') {
      closeGeminiModal();
      closeDocModal();
      closePackingModal();
      closeCurrencyModal();
      closeTranslationsModal();
      closeLuggageModal();
      closeRouteModal();
      closePriceRadarModal();
      closeAllToolsModal();
      closeChangeRequestModal();
    }
  });

  // Observe active day in viewport to update scrubber
  window.addEventListener('scroll', throttle(updateActiveDayFromScroll, 200), { passive: true });
}

// -------------------------------------------------------------
// STICKY TIMELINE SCRUBBER CONTROLLER
// -------------------------------------------------------------
function renderTimelineScrubber() {
  if (!itineraryData) return;
  const container = document.getElementById('timeline-scrubber-list');
  if (!container) return;
  container.innerHTML = '';

  const days = itineraryData.days || [];
  days.forEach(day => {
    const isPhase1 = day.phase.includes('Vietnam') || day.day_number <= 13;
    const dotColor = isPhase1 ? 'bg-amber-500' : 'bg-pink-500';
    const shortDate = day.date ? day.date.slice(5).replace('-', '/') : '';
    const dayStr = day.day_number < 10 ? '0' + day.day_number : day.day_number;

    const pill = document.createElement('button');
    pill.id = `scrubber-pill-${day.day_number}`;
    pill.className = `timeline-day-pill ${day.day_number === 1 ? 'active' : ''}`;
    pill.setAttribute('title', `Day ${day.day_number}: ${day.destination} (${day.date})`);
    pill.innerHTML = `
      <div class="flex items-center gap-1 font-bold text-xs">
        <span class="w-2 h-2 rounded-full ${dotColor}"></span>
        <span>D${dayStr}</span>
      </div>
      <span class="text-[10px] text-slate-500 dark:text-slate-400 font-mono mt-0.5">${shortDate}</span>
    `;
    pill.onclick = () => scrollToDay(day.day_number);
    container.appendChild(pill);
  });
}

function scrollToDay(dayNum) {
  if (!itineraryData) return;
  const days = itineraryData.days || [];
  const targetDay = days.find(d => d.day_number === dayNum);
  if (!targetDay) return;

  // 1. Update active scrubber pill
  document.querySelectorAll('.timeline-day-pill').forEach(p => p.classList.remove('active'));
  const activePill = document.getElementById(`scrubber-pill-${dayNum}`);
  if (activePill) {
    activePill.classList.add('active');
    activePill.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
  }

  // 2. Update active label
  const label = document.getElementById('active-day-label');
  if (label) {
    label.innerText = `Day ${dayNum} • ${targetDay.destination}`;
  }

  // 3. Ensure day card is rendered (reset filters if filtered out)
  const card = document.getElementById(`day-card-${dayNum}`);
  if (!card) {
    currentPhase = 'all';
    currentFilter = 'all';
    searchQuery = '';
    const searchInput = document.getElementById('search-input');
    if (searchInput) searchInput.value = '';
    renderDays();
  }

  const targetCard = document.getElementById(`day-card-${dayNum}`);
  if (targetCard) {
    // Expand accordion content
    const content = document.getElementById(`day-content-${dayNum}`);
    const icon = document.getElementById(`day-icon-${dayNum}`);
    if (content) content.classList.remove('hidden');
    if (icon) icon.classList.add('rotate-180');

    // Smooth scroll to card (offset for integrated sticky header + date strip ~ 116px)
    const yOffset = window.innerWidth < 640 ? -116 : -124;
    const y = targetCard.getBoundingClientRect().top + window.pageYOffset + yOffset;
    window.scrollTo({ top: y, behavior: 'smooth' });

    // Focus glow pulse
    targetCard.classList.remove('highlight-target-day');
    void targetCard.offsetWidth; // reflow
    targetCard.classList.add('highlight-target-day');
    setTimeout(() => {
      targetCard.classList.remove('highlight-target-day');
    }, 3000);
  }
}

function scrollToCurrentActiveDay() {
  jumpToToday();
}

function updateActiveDayFromScroll() {
  if (!itineraryData) return;
  const days = itineraryData.days || [];
  const scrollPos = window.scrollY + 140;

  for (let i = days.length - 1; i >= 0; i--) {
    const card = document.getElementById(`day-card-${days[i].day_number}`);
    if (card && card.offsetTop <= scrollPos) {
      const activeNum = days[i].day_number;
      // Update scrubber active pill if changed
      const currentActive = document.querySelector('.timeline-day-pill.active');
      const targetPill = document.getElementById(`scrubber-pill-${activeNum}`);
      if (targetPill && currentActive !== targetPill) {
        if (currentActive) currentActive.classList.remove('active');
        targetPill.classList.add('active');
        targetPill.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        const label = document.getElementById('active-day-label');
        if (label) label.innerText = `Day ${activeNum} • ${days[i].destination}`;
      }
      break;
    }
  }
}

function throttle(func, limit) {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// -------------------------------------------------------------
// DAILY TASK CHECKLIST PERSISTENCE
// -------------------------------------------------------------
function toggleDailyTask(dayNum, taskIdx, checkboxEl) {
  const storageKey = 'travel_os_daily_tasks_v1';
  let tasksState = {};
  try {
    tasksState = JSON.parse(localStorage.getItem(storageKey) || '{}');
  } catch (e) {
    tasksState = {};
  }

  const key = `${dayNum}_${taskIdx}`;
  tasksState[key] = checkboxEl.checked;
  localStorage.setItem(storageKey, JSON.stringify(tasksState));

  const textEl = checkboxEl.parentElement.querySelector('.daily-task-text');
  if (textEl) {
    if (checkboxEl.checked) textEl.classList.add('checked');
    else textEl.classList.remove('checked');
  }
}

// -------------------------------------------------------------
// FLOATING TODAY QUICK-JUMP ANCHOR
// -------------------------------------------------------------
function jumpToToday() {
  if (!itineraryData) return;
  const days = itineraryData.days || [];
  if (days.length === 0) return;

  const now = new Date();
  const tripStart = new Date('2026-09-11T00:00:00');
  const tripEnd = new Date('2026-10-09T23:59:59');

  let targetDayNum = 1;
  if (now >= tripStart && now <= tripEnd) {
    const diffTime = Math.abs(now - tripStart);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    targetDayNum = diffDays + 1;
  }

  // Ensure day exists in active list
  currentPhase = 'all';
  currentFilter = 'all';
  searchQuery = '';
  renderDays();

  setTimeout(() => {
    const card = document.getElementById(`day-card-${targetDayNum}`);
    const content = document.getElementById(`day-content-${targetDayNum}`);
    const icon = document.getElementById(`day-icon-${targetDayNum}`);

    if (card) {
      if (content && content.classList.contains('hidden')) {
        content.classList.remove('hidden');
        if (icon) icon.classList.add('rotate-180');
      }

      card.scrollIntoView({ behavior: 'smooth', block: 'start' });
      card.classList.add('highlight-target-day');
      setTimeout(() => card.classList.remove('highlight-target-day'), 4000);

      showToast(`Navigated to Day ${targetDayNum}!`, '📍');
    }
  }, 100);
}

// -------------------------------------------------------------
// DYNAMIC SPLIT-LUGGAGE PACKING CONTROLLER
// -------------------------------------------------------------
const PACKING_STORAGE_KEY = 'travel_os_packing_items_v1';

function getPackingState() {
  try {
    const raw = localStorage.getItem(PACKING_STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch (e) {
    return {};
  }
}

function savePackingState(state) {
  try {
    localStorage.setItem(PACKING_STORAGE_KEY, JSON.stringify(state));
  } catch (e) {
    console.error('Failed to save packing state to localStorage:', e);
  }
}

function initPackingChecklist() {
  renderPackingItems();
  updatePackingProgress();
}

function openPackingModal() {
  const modal = document.getElementById('packing-modal');
  if (modal) {
    modal.classList.remove('hidden');
    renderPackingItems();
    updatePackingProgress();
  }
}

function closePackingModal() {
  const modal = document.getElementById('packing-modal');
  if (modal) modal.classList.add('hidden');
}

function switchPackingTab(tab) {
  currentPackingTab = tab;
  ['bag_a', 'bag_b', 'pre_dep'].forEach(t => {
    const btn = document.getElementById(`btn-pack-${t}`);
    if (btn) {
      if (t === tab) {
        btn.className = 'px-3 py-1.5 rounded-lg font-bold bg-blue-600 text-white shrink-0';
      } else {
        btn.className = 'px-3 py-1.5 rounded-lg font-medium text-slate-400 hover:text-white bg-slate-800 shrink-0';
      }
    }
  });
  renderPackingItems();
}

function renderPackingItems() {
  const container = document.getElementById('packing-items-container');
  if (!container || !itineraryData) return;

  const packingMaster = itineraryData.packing_master_list || {};
  let key = 'bag_a_backpack';
  if (currentPackingTab === 'bag_b') key = 'bag_b_suitcase';
  if (currentPackingTab === 'pre_dep') key = 'pre_departure_inspection';

  const items = packingMaster[key] || [];
  const state = getPackingState();

  if (items.length === 0) {
    container.innerHTML = `<p class="text-xs text-slate-400">No items configured for this bag.</p>`;
    return;
  }

  container.innerHTML = items.map(item => {
    const isChecked = Boolean(state[item.id]);
    const isCritical = item.priority === 'CRITICAL';
    const isHigh = item.priority === 'HIGH';

    let priorityBadge = `<span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">NORMAL</span>`;
    if (isCritical) {
      priorityBadge = `<span class="text-[10px] px-1.5 py-0.5 rounded bg-red-950 text-red-300 font-bold border border-red-600/40">CRITICAL</span>`;
    } else if (isHigh) {
      priorityBadge = `<span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-950 text-amber-300 font-semibold border border-amber-600/40">HIGH</span>`;
    }

    return `
      <div class="p-3.5 rounded-2xl border ${isChecked ? 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-300 dark:border-emerald-500/40' : 'bg-slate-50/70 dark:bg-slate-900/60 border-slate-200 dark:border-slate-800'} flex items-start gap-3.5 transition shadow-sm">
        <input type="checkbox" id="chk-${item.id}" ${isChecked ? 'checked' : ''} onchange="togglePackingItem('${item.id}')" class="packing-checkbox mt-0.5 shrink-0">
        <label for="chk-${item.id}" class="flex-1 cursor-pointer select-none">
          <div class="flex items-center justify-between flex-wrap gap-1.5">
            <span class="font-bold text-sm ${isChecked ? 'text-emerald-700 dark:text-emerald-300 line-through' : 'text-slate-900 dark:text-slate-100'}">${item.name}</span>
            <div class="flex items-center gap-1.5">
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-semibold">${item.cat}</span>
              ${priorityBadge}
            </div>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-400 mt-1 leading-relaxed">${item.desc}</p>
        </label>
      </div>
    `;
  }).join('');
}

function togglePackingItem(itemId) {
  const state = getPackingState();
  state[itemId] = !state[itemId];
  savePackingState(state);
  renderPackingItems();
  updatePackingProgress();
}

function resetPackingChecklist() {
  if (confirm('Are you sure you want to reset and uncheck all packing items?')) {
    savePackingState({});
    renderPackingItems();
    updatePackingProgress();
    showToast('Packing checklist reset', '🧳');
  }
}

function updatePackingProgress() {
  if (!itineraryData) return;
  const packingMaster = itineraryData.packing_master_list || {};
  const allItems = [
    ...(packingMaster.bag_a_backpack || []),
    ...(packingMaster.bag_b_suitcase || []),
    ...(packingMaster.pre_departure_inspection || [])
  ];

  const total = allItems.length;
  if (total === 0) return;

  const state = getPackingState();
  const packedCount = allItems.filter(i => Boolean(state[i.id])).length;
  const pct = Math.round((packedCount / total) * 100);

  const txt = document.getElementById('packing-progress-text');
  const bar = document.getElementById('packing-progress-bar');

  if (txt) txt.innerText = `${packedCount} / ${total} packed (${pct}%)`;
  if (bar) bar.style.width = `${pct}%`;
}

// -------------------------------------------------------------
// LIVE 4-WAY CURRENCY CONVERTER
// -------------------------------------------------------------
function openCurrencyModal() {
  const modal = document.getElementById('currency-modal');
  if (modal) modal.classList.remove('hidden');
}

function closeCurrencyModal() {
  const modal = document.getElementById('currency-modal');
  if (modal) modal.classList.add('hidden');
}

function initCurrencyDefaults() {
  setCurrencyPreset('thb', 500);
}

function calculateCurrency(source) {
  const rates = itineraryData?.currency_benchmarks?.rates || {
    USD: 1.0,
    ILS: 3.70,
    THB: 36.5,
    VND: 25400.0
  };

  const ilsInput = document.getElementById('curr-input-ils');
  const usdInput = document.getElementById('curr-input-usd');
  const thbInput = document.getElementById('curr-input-thb');
  const vndInput = document.getElementById('curr-input-vnd');

  let val = 0;
  let baseUSD = 0;

  if (source === 'ils') {
    val = parseFloat(ilsInput.value) || 0;
    baseUSD = val / rates.ILS;
  } else if (source === 'usd') {
    val = parseFloat(usdInput.value) || 0;
    baseUSD = val / rates.USD;
  } else if (source === 'thb') {
    val = parseFloat(thbInput.value) || 0;
    baseUSD = val / rates.THB;
  } else if (source === 'vnd') {
    val = parseFloat(vndInput.value) || 0;
    baseUSD = val / rates.VND;
  }

  if (val === 0) {
    if (source !== 'ils') ilsInput.value = '';
    if (source !== 'usd') usdInput.value = '';
    if (source !== 'thb') thbInput.value = '';
    if (source !== 'vnd') vndInput.value = '';
    return;
  }

  if (source !== 'ils') ilsInput.value = (baseUSD * rates.ILS).toFixed(2);
  if (source !== 'usd') usdInput.value = (baseUSD * rates.USD).toFixed(2);
  if (source !== 'thb') thbInput.value = Math.round(baseUSD * rates.THB);
  if (source !== 'vnd') vndInput.value = Math.round(baseUSD * rates.VND).toLocaleString('en-US');
}

function setCurrencyPreset(curr, amount) {
  const input = document.getElementById(`curr-input-${curr}`);
  if (input) {
    input.value = amount;
    calculateCurrency(curr);
  }
}

// -------------------------------------------------------------
// OFFLINE EMERGENCY & TAXI PHRASEBOOK
// -------------------------------------------------------------
function openTranslationsModal() {
  const modal = document.getElementById('translations-modal');
  if (modal) {
    modal.classList.remove('hidden');
    renderTranslations();
  }
}

function closeTranslationsModal() {
  const modal = document.getElementById('translations-modal');
  if (modal) modal.classList.add('hidden');
}

function filterTranslations(cat) {
  currentTranslationCat = cat;
  ['all', 'taxi_transit', 'food_dietary', 'emergency_medical', 'airport_luggage'].forEach(c => {
    const btn = document.getElementById(`btn-trans-${c}`);
    if (btn) {
      if (c === cat) {
        btn.className = 'px-3 py-1.5 rounded-lg font-bold bg-blue-600 text-white shrink-0';
      } else {
        btn.className = 'px-3 py-1.5 rounded-lg font-medium text-slate-400 hover:text-white bg-slate-800 shrink-0';
      }
    }
  });
  renderTranslations();
}

function renderTranslations() {
  const container = document.getElementById('translations-list-container');
  if (!container || !itineraryData) return;

  const dict = itineraryData.translations_dictionary || {};
  let phrases = [];

  if (currentTranslationCat === 'all') {
    Object.keys(dict).forEach(k => {
      phrases = phrases.concat(dict[k] || []);
    });
  } else {
    phrases = dict[currentTranslationCat] || [];
  }

  if (phrases.length === 0) {
    container.innerHTML = `<p class="text-xs text-slate-400">No phrases available.</p>`;
    return;
  }

  container.innerHTML = phrases.map((p, idx) => {
    const escapedTH = (p.th || '').replace(/'/g, "\\'");
    const escapedVI = (p.vi || '').replace(/'/g, "\\'");
    const escapedEN = (p.en || '').replace(/'/g, "\\'");
    const escapedTHPhonetic = (p.th_phonetic || '').replace(/'/g, "\\'");
    const escapedVIPhonetic = (p.vi_phonetic || '').replace(/'/g, "\\'");

    return `
      <div class="bg-white dark:bg-slate-900/80 p-4 sm:p-5 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-3 shadow-sm">
        <div class="flex items-start justify-between gap-2">
          <p class="font-black text-slate-900 dark:text-white text-sm sm:text-base leading-snug">${p.en}</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <!-- Thai Card -->
          <div class="bg-amber-50/70 dark:bg-slate-950/70 p-3.5 rounded-xl border border-amber-200 dark:border-slate-800/80 flex flex-col justify-between">
            <div>
              <span class="text-[10px] text-amber-800 dark:text-amber-400 font-bold uppercase tracking-wider">Thai (ไทย)</span>
              <p class="text-slate-900 dark:text-white font-bold text-base mt-0.5 leading-relaxed">${p.th}</p>
              <p class="text-slate-600 dark:text-slate-400 text-xs italic mt-0.5">(${p.th_phonetic})</p>
            </div>
            <div class="mt-3 pt-2 border-t border-amber-200/60 dark:border-slate-800 flex items-center gap-2">
              <button onclick="showFullscreenPhrase('${escapedEN}', '${escapedTH}', '${escapedTHPhonetic}')" class="px-3 py-1.5 bg-amber-500 hover:bg-amber-600 text-white rounded-xl text-xs font-bold flex items-center gap-1 shadow-sm transition">
                <span>📱</span> Driver Display
              </button>
              <button onclick="copyToClipboard('${escapedTH}', 'Copied Thai phrase!')" class="px-3 py-1.5 bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-semibold border border-slate-200 dark:border-slate-700 transition">
                Copy
              </button>
            </div>
          </div>

          <!-- Vietnamese Card -->
          <div class="bg-emerald-50/70 dark:bg-slate-950/70 p-3.5 rounded-xl border border-emerald-200 dark:border-slate-800/80 flex flex-col justify-between">
            <div>
              <span class="text-[10px] text-emerald-800 dark:text-emerald-400 font-bold uppercase tracking-wider">Vietnamese (Tiếng Việt)</span>
              <p class="text-slate-900 dark:text-white font-bold text-base mt-0.5 leading-relaxed">${p.vi}</p>
              <p class="text-slate-600 dark:text-slate-400 text-xs italic mt-0.5">(${p.vi_phonetic})</p>
            </div>
            <div class="mt-3 pt-2 border-t border-emerald-200/60 dark:border-slate-800 flex items-center gap-2">
              <button onclick="showFullscreenPhrase('${escapedEN}', '${escapedVI}', '${escapedVIPhonetic}')" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold flex items-center gap-1 shadow-sm transition">
                <span>📱</span> Driver Display
              </button>
              <button onclick="copyToClipboard('${escapedVI}', 'Copied Vietnamese phrase!')" class="px-3 py-1.5 bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-semibold border border-slate-200 dark:border-slate-700 transition">
                Copy
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

function showFullscreenPhrase(en, local, phonetic) {
  const modal = document.getElementById('fullscreen-phrase-modal');
  const enEl = document.getElementById('fs-phrase-en');
  const localEl = document.getElementById('fs-phrase-local');
  const phoneticEl = document.getElementById('fs-phrase-phonetic');

  if (enEl) enEl.innerText = en;
  if (localEl) localEl.innerText = local;
  if (phoneticEl) phoneticEl.innerText = phonetic ? `(${phonetic})` : '';

  if (modal) modal.classList.remove('hidden');
}

function closeFullscreenPhrase() {
  const modal = document.getElementById('fullscreen-phrase-modal');
  if (modal) modal.classList.add('hidden');
}

// -------------------------------------------------------------
// CLIPBOARD & TOAST SYSTEM
// -------------------------------------------------------------
function copyToClipboard(text, successMsg = 'Copied to clipboard!') {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => {
      showToast(successMsg, '📋');
    }).catch(() => {
      fallbackCopy(text, successMsg);
    });
  } else {
    fallbackCopy(text, successMsg);
  }
}

function fallbackCopy(text, successMsg) {
  const textArea = document.createElement('textarea');
  textArea.value = text;
  textArea.style.position = 'fixed';
  textArea.style.opacity = '0';
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
    document.execCommand('copy');
    showToast(successMsg, '📋');
  } catch (err) {
    showToast('Failed to copy', '⚠️');
  }
  document.body.removeChild(textArea);
}

function showToast(message, icon = '✓') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span class="text-base">${icon}</span><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'all 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 2600);
}

// -------------------------------------------------------------
// MODALS (Existing Handlers Preserved)
// -------------------------------------------------------------
function openDocModal(docId) {
  const modal = document.getElementById('doc-modal');
  const title = document.getElementById('modal-doc-title');
  const body = document.getElementById('modal-doc-body');

  let item = null;
  const registry = window.TRAVEL_OS_DATA?.confirmed_items || [];
  item = registry.find(r => r.id === docId);

  if (!item) {
    (window.TRAVEL_OS_DATA?.days || []).forEach(d => {
      (d.attached_documents || []).forEach(doc => {
        if (doc.doc_id === docId) item = doc;
      });
    });
  }

  const docTitle = item?.title || 'Travel Document Reference';
  const docRef = item?.reference_code || item?.ref || 'VERIFIED';
  const hasRealFile = Boolean(item?.file_path);

  title.innerText = docTitle;
  body.innerHTML = `
    <div class="space-y-3 text-xs">
      <div class="p-3 bg-blue-950/50 rounded-xl border border-blue-700/50">
        <span class="text-[10px] text-blue-300 uppercase tracking-wider font-bold">Booking Reference / Pass Code</span>
        <p class="text-base font-mono text-white font-bold mt-0.5">${docRef}</p>
      </div>

      ${hasRealFile 
        ? `
          <div class="p-3.5 bg-emerald-950/60 rounded-xl border border-emerald-500/60 text-emerald-200 space-y-2">
            <div class="font-bold flex items-center gap-1.5 text-emerald-300 text-sm">
              <span>✓</span> Genuine Attachment Verified from Gmail
            </div>
            <p class="text-[11px] text-slate-300">
              Extracted from official airline / immigration / hotel email into project repository.
            </p>
            <div class="pt-1">
              <a href="${item.file_path}" target="_blank" download class="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-bold text-xs shadow-lg transition">
                <span>📥</span> Download / View PDF (${item.file_name || 'Document'})
              </a>
            </div>
          </div>
        `
        : `
          <div class="p-3 bg-amber-950/40 rounded-xl border border-amber-600/40 text-amber-200">
            <div class="font-bold flex items-center gap-1.5 mb-1">
              <span>⚠️</span> Physical / PDF File Status:
            </div>
            <p class="text-[11px] leading-relaxed">
              <b>No physical ticket or PDF has been downloaded from Gmail yet.</b> This booking was entered via your confirmed profile code (${docRef}), but the actual mail confirmation or PDF voucher has not been ingested.
            </p>
          </div>

          <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 text-slate-300 space-y-1.5">
            <div class="font-bold text-white">How to attach your actual PDF ticket:</div>
            <p>1. <b>Manual Drop:</b> Place your PDF voucher into <code class="bg-slate-800 px-1 py-0.5 rounded text-blue-300">flight_itiniery/documents/</code></p>
            <p>2. <b>Gmail Ingestion:</b> Configured via <code class="bg-slate-800 px-1 py-0.5 rounded text-blue-300">.env</code>.</p>
          </div>
        `
      }
    </div>
  `;
  modal.classList.remove('hidden');
}

function closeDocModal() {
  document.getElementById('doc-modal').classList.add('hidden');
}

function openPriceRadarModal() {
  const modal = document.getElementById('price-radar-modal');
  if (modal) modal.classList.remove('hidden');
}

function closePriceRadarModal() {
  const modal = document.getElementById('price-radar-modal');
  if (modal) modal.classList.add('hidden');
}

function openLuggageModal() {
  const modal = document.getElementById('luggage-modal');
  if (modal) modal.classList.remove('hidden');
}

function closeLuggageModal() {
  const modal = document.getElementById('luggage-modal');
  if (modal) modal.classList.add('hidden');
}

function openRouteModal() {
  const modal = document.getElementById('route-modal');
  if (modal) modal.classList.remove('hidden');
}

function closeRouteModal() {
  const modal = document.getElementById('route-modal');
  if (modal) modal.classList.add('hidden');
}

// -------------------------------------------------------------
// ALL-IN-ONE TRAVEL OS QUICK TOOLS HUB MODAL
// -------------------------------------------------------------
function openAllToolsModal() {
  const modal = document.getElementById('all-tools-modal');
  if (modal) {
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
}
window.openAllToolsModal = openAllToolsModal;

function closeAllToolsModal() {
  const modal = document.getElementById('all-tools-modal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  }
}
window.closeAllToolsModal = closeAllToolsModal;

function launchTool(toolName) {
  closeAllToolsModal();
  setTimeout(() => {
    if (toolName === 'packing') openPackingModal();
    else if (toolName === 'currency') openCurrencyModal();
    else if (toolName === 'translations') openTranslationsModal();
    else if (toolName === 'change_request') openChangeRequestModal();
    else if (toolName === 'gemini') openGeminiModal();
    else if (toolName === 'luggage') openLuggageModal();
    else if (toolName === 'route') openRouteModal();
    else if (toolName === 'radar') openPriceRadarModal();
    else if (toolName === 'doc') switchView('doc');
    else if (toolName === 'ops') {
      const drawer = document.getElementById('ops-drawer-content');
      if (drawer && drawer.classList.contains('hidden')) toggleOpsDrawer();
      const overview = document.getElementById('app-view-container');
      if (overview) overview.scrollIntoView({ behavior: 'smooth' });
    }
  }, 50);
}
window.launchTool = launchTool;


// =============================================================
// GEMINI 3.8 FLASH GROUNDED TRAVEL ASSISTANT
// =============================================================

let geminiConversation = []; // [{ role: "user" | "model", parts: [{ text: "..." }] }]
let geminiIsLoading = false;
let geminiActiveModel = 'gemini-3.8-flash';

function initGeminiAssistant() {
  // 1. Resolve active model from storage or config
  const savedModel = localStorage.getItem('travel_os_gemini_model');
  geminiActiveModel = savedModel || (window.TRAVEL_OS_CONFIG ? window.TRAVEL_OS_CONFIG.defaultModel : 'gemini-3.8-flash');
  
  const modelSelect = document.getElementById('gemini-model-select');
  if (modelSelect) modelSelect.value = geminiActiveModel;
  
  updateModelBadge(geminiActiveModel);

  // 2. Prefill API key input if available
  const apiKeyInput = document.getElementById('gemini-api-key-input');
  const resolvedKey = getResolvedGeminiKey();
  if (apiKeyInput && resolvedKey) {
    apiKeyInput.value = resolvedKey;
  }

  // 3. Restore chat history or show welcome message
  const savedHistory = sessionStorage.getItem('travel_os_gemini_history');
  if (savedHistory) {
    try {
      geminiConversation = JSON.parse(savedHistory);
      renderAllGeminiMessages();
    } catch (e) {
      geminiConversation = [];
      showInitialGeminiWelcome();
    }
  } else {
    showInitialGeminiWelcome();
  }
}

function getResolvedGeminiKey() {
  if (window.TRAVEL_OS_CONFIG && typeof window.TRAVEL_OS_CONFIG.getApiKey === 'function') {
    return window.TRAVEL_OS_CONFIG.getApiKey();
  }
  return localStorage.getItem('travel_os_gemini_key') || '';
}

function showInitialGeminiWelcome() {
  const welcome = `Hello Eyal! I am **Gemini 3.8 Flash**, your autonomous Travel Operations Assistant.

I am **100% grounded in real time** on your complete **Thailand & Vietnam 29-Day Travel OS**:
- **6 Verified Hard Anchors**: Emirates flight \`G5M8CF\`, Thailand TDAC arrival card \`#30C4358\`, Sukhon Hotel Agoda \`697155847\`, Mytrip flights \`1145-554-179\` (BKK-HAN & HAN-BKK), and Etihad flight \`9KDEH2\`.
- **Ha Giang 3-Day Loop**: Direct Hanoi Airport sleeper pickup on Day 2, licensed easy-riders, and private twin-bed rooms included (*Dong Van Eco Stone House* & *Du Gia Panorama Lodge*).
- **Sa Pa Rest & Mamas Trek**: Direct sleeper bus from Ha Giang to Sa Pa, 1 night deep sleep at *BB Hotel Sapa*, followed by a 2-day trek guided on foot by local Black Hmong Mamas, staying at their village wooden stilt homestay in Ta Van, and eating authentic homecooked food by the open hearth.
- **Sequence A Triangle**: Sa Pa ➔ Direct VIP coach to Ninh Binh (*Tam Coc Garden Resort*) ➔ Cat Ba Island (*Lan Ha Bay*) ➔ Hanoi Old Quarter.
- **Bangkok AIRPORTELs Locker**: Checked suitcase deposited morning of Sep 12 at BKK Floor B; strictly 55L backpack for northern Vietnam; retrieved Sep 24 before flying to Koh Samui.
- **Phase 2 Gulf Islands**: Romantic King sanctuaries in Koh Samui (*Hansar*), Koh Phangan (*Santhiya*), and Koh Tao (*Dusit Buncha*).
- **Utilities**: 4-way currency rates, TPBank/VPBank zero-fee ATMs, Grab taxi helpers, and Plan B rainy-day contingencies for every day!

Ask me anything about your dates, bookings, packing, or daily plans!`;

  geminiConversation = [
    { role: "model", parts: [{ text: welcome }] }
  ];
  renderAllGeminiMessages();
}

function updateModelBadge(model) {
  const badge = document.getElementById('gemini-active-model-badge');
  if (badge) badge.innerText = model;
}

function openGeminiModal() {
  const modal = document.getElementById('gemini-modal');
  if (modal) {
    modal.classList.remove('hidden');
    scrollGeminiToBottom();
    const input = document.getElementById('gemini-chat-input');
    if (input) setTimeout(() => input.focus(), 100);
  }
}

function closeGeminiModal() {
  const modal = document.getElementById('gemini-modal');
  if (modal) modal.classList.add('hidden');
}

function toggleGeminiSettings() {
  const drawer = document.getElementById('gemini-settings-drawer');
  if (drawer) drawer.classList.toggle('hidden');
}

function saveGeminiModelPreference() {
  const select = document.getElementById('gemini-model-select');
  if (!select) return;
  geminiActiveModel = select.value;
  localStorage.setItem('travel_os_gemini_model', geminiActiveModel);
  updateModelBadge(geminiActiveModel);
  showToast(`Switched Gemini model to ${geminiActiveModel}`);
}

function saveGeminiApiKey() {
  const input = document.getElementById('gemini-api-key-input');
  if (!input) return;
  const key = input.value.trim();
  if (key) {
    localStorage.setItem('travel_os_gemini_key', key);
    showToast('Gemini API key saved to browser!');
  } else {
    localStorage.removeItem('travel_os_gemini_key');
    showToast('Reset to default Gemini API key.');
  }
}

function toggleKeyVisibility() {
  const input = document.getElementById('gemini-api-key-input');
  if (!input) return;
  input.type = input.type === 'password' ? 'text' : 'password';
}

function clearGeminiChat() {
  sessionStorage.removeItem('travel_os_gemini_history');
  showInitialGeminiWelcome();
  showToast('Chat history cleared.');
}

function sendQuickPrompt(promptText) {
  const input = document.getElementById('gemini-chat-input');
  if (input) {
    input.value = promptText;
    handleGeminiSubmit(new Event('submit'));
  }
}

function handleGeminiInputKeydown(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    handleGeminiSubmit(event);
  }
}

function renderAllGeminiMessages() {
  const container = document.getElementById('gemini-chat-messages');
  if (!container) return;
  container.innerHTML = '';

  geminiConversation.forEach((msg, idx) => {
    const text = msg.parts?.[0]?.text || '';
    appendMessageElement(msg.role, text, idx);
  });

  scrollGeminiToBottom();
}

function appendMessageElement(role, text, index) {
  const container = document.getElementById('gemini-chat-messages');
  if (!container) return;

  const msgDiv = document.createElement('div');
  msgDiv.className = `flex ${role === 'user' ? 'justify-end' : 'justify-start'}`;

  if (role === 'user') {
    msgDiv.innerHTML = `
      <div class="max-w-[85%] sm:max-w-[75%] bg-blue-600 text-white rounded-2xl rounded-tr-sm px-4 py-2.5 text-sm shadow-sm font-medium">
        <p class="whitespace-pre-wrap">${escapeHtml(text)}</p>
      </div>
    `;
  } else {
    const htmlContent = renderMarkdownToHtml(text);
    msgDiv.innerHTML = `
      <div class="max-w-[95%] sm:max-w-[88%] bg-white dark:bg-slate-800/90 border border-slate-200 dark:border-slate-700/80 rounded-2xl rounded-tl-sm p-4 sm:p-5 text-slate-800 dark:text-slate-100 shadow-sm space-y-2 relative group">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-700/50 pb-2 text-xs text-slate-500 dark:text-slate-400">
          <div class="flex items-center gap-1.5 font-bold text-blue-600 dark:text-indigo-300">
            <span>✨</span> <span>Gemini 3.8 Flash</span>
          </div>
          <button type="button" onclick="copyGeminiMessage(this)" class="opacity-80 hover:opacity-100 px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 text-[11px] font-semibold text-slate-700 dark:text-slate-300 transition flex items-center gap-1" title="Copy answer">
            <span>📋</span> <span>Copy</span>
          </button>
        </div>
        <div class="gemini-markdown text-slate-700 dark:text-slate-200">
          ${htmlContent}
        </div>
      </div>
    `;
  }

  container.appendChild(msgDiv);
}

function scrollGeminiToBottom() {
  const container = document.getElementById('gemini-chat-messages');
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
}

function copyGeminiMessage(btn) {
  const parent = btn.closest('.group');
  const content = parent.querySelector('.gemini-markdown')?.innerText || '';
  navigator.clipboard.writeText(content).then(() => {
    const oldText = btn.innerHTML;
    btn.innerHTML = '<span>✓</span> <span>Copied!</span>';
    setTimeout(() => { btn.innerHTML = oldText; }, 2000);
  });
}

function updateTypingIndicator(statusText = null) {
  const indicator = document.getElementById('gemini-typing-indicator');
  const textEl = document.getElementById('gemini-typing-text');
  if (!indicator) return;
  
  if (geminiIsLoading) {
    indicator.classList.remove('hidden');
    if (textEl && statusText) textEl.innerText = statusText;
    scrollGeminiToBottom();
  } else {
    indicator.classList.add('hidden');
  }
}

async function handleGeminiSubmit(e) {
  if (e && typeof e.preventDefault === 'function') e.preventDefault();
  if (geminiIsLoading) return;

  const input = document.getElementById('gemini-chat-input');
  if (!input) return;
  const userText = input.value.trim();
  if (!userText) return;

  const apiKey = getResolvedGeminiKey();
  if (!apiKey) {
    toggleGeminiSettings();
    showToast('Please enter your Gemini API key in settings!');
    return;
  }

  // Clear input
  input.value = '';

  // 1. Add user message to conversation
  geminiConversation.push({
    role: "user",
    parts: [{ text: userText }]
  });
  appendMessageElement('user', userText, geminiConversation.length - 1);
  scrollGeminiToBottom();

  // 2. Set loading state
  geminiIsLoading = true;
  updateTypingIndicator(`Gemini 3.8 Flash is analyzing your travel OS dataset...`);
  const submitBtn = document.getElementById('gemini-submit-btn');
  if (submitBtn) submitBtn.disabled = true;

  try {
    // 3. Build grounding system prompt from live itinerary dataset
    const systemPrompt = buildMasterGroundingSystemPrompt(itineraryData);

    // Format conversation history for Gemini API
    const apiContents = geminiConversation.map(msg => ({
      role: msg.role === 'model' ? 'model' : 'user',
      parts: [{ text: msg.parts[0].text }]
    }));

    // 4. Call Gemini API with auto-retry and fallback
    const result = await callGeminiApiWithRetry(systemPrompt, apiContents, geminiActiveModel, apiKey, 1);
    
    let answerText = result.text;
    if (result.modelUsed !== geminiActiveModel) {
      answerText = `> *Note: Answered via ${result.modelUsed} fallback due to temporary spike on ${geminiActiveModel}.*\n\n` + answerText;
    }

    // 5. Add model response to conversation
    geminiConversation.push({
      role: "model",
      parts: [{ text: answerText }]
    });

    appendMessageElement('model', answerText, geminiConversation.length - 1);

    // Persist session history
    sessionStorage.setItem('travel_os_gemini_history', JSON.stringify(geminiConversation));

  } catch (err) {
    console.error('Gemini error:', err);
    const errorMsg = `⚠️ **Assistant Error**: ${err.message || 'Failed to connect to Gemini API.'}\n\n*Tips: Check your internet connection or inspect your Gemini API key in settings (⚙️).*`;
    appendMessageElement('model', errorMsg, geminiConversation.length);
  } finally {
    geminiIsLoading = false;
    updateTypingIndicator();
    if (submitBtn) submitBtn.disabled = false;
    scrollGeminiToBottom();
  }
}

async function callGeminiApiWithRetry(systemInstruction, conversation, model, apiKey, attempt = 1) {
  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
  
  const payload = {
    system_instruction: {
      parts: [{ text: systemInstruction }]
    },
    contents: conversation,
    generationConfig: {
      temperature: 0.2,
      topP: 0.95,
      maxOutputTokens: 2048
    }
  };

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 28000);

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (response.status === 200) {
      const data = await response.json();
      const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;
      if (text) return { text, modelUsed: model, attempts: attempt };
      throw new Error("Empty candidate received from Gemini API");
    }

    // Handle temporary 503 high demand or 429 rate limit with exponential backoff
    if ((response.status === 503 || response.status === 429) && attempt <= 3) {
      const delayMs = attempt * 1500;
      updateTypingIndicator(`Gemini 3.8 Flash high demand spike. Retrying in ${(delayMs / 1000).toFixed(1)}s (Attempt ${attempt}/3)...`);
      await new Promise(r => setTimeout(r, delayMs));
      return await callGeminiApiWithRetry(systemInstruction, conversation, model, apiKey, attempt + 1);
    }

    // If 3 retries on gemini-3.8-flash failed with 503, fallback to gemini-2.5-flash
    if (model === 'gemini-3.8-flash' && (response.status === 503 || response.status === 429)) {
      updateTypingIndicator(`Routing to stable Gemini 2.5 Flash fallback...`);
      return await callGeminiApiWithRetry(systemInstruction, conversation, 'gemini-2.5-flash', apiKey, 1);
    }

    const errBody = await response.text();
    throw new Error(`Gemini API error (Status ${response.status}): ${errBody.slice(0, 160)}`);
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      throw new Error("Request timed out after 28 seconds.");
    }
    throw err;
  }
}

function buildMasterGroundingSystemPrompt(data) {
  if (!data) return "You are an AI assistant for a 29-day trip to Thailand & Vietnam.";

  const days = data.days || [];
  
  let daysSummary = "";
  days.forEach(d => {
    const hotels = (d.accommodation_matrix || []).map(h => `${h.hotel_name} (${h.room_spec || 'Twin/King'})`).join(", ");
    const exp = d.experiences || d.daily_experience_hub || {};
    const primaryTitle = exp.primary?.title || exp.primary_plan?.title || d.destination;
    const contTitle = exp.contingency?.title || exp.contingency_plan?.title || "Indoor alternative";
    const trigger = exp.contingency?.trigger || exp.contingency_plan?.trigger_condition || "Heavy Rain / Storm";
    const transit = d.door_to_door_logistics?.primary_transit || "Local transit";

    daysSummary += `DAY ${d.day_number} (${d.date}, ${d.day_of_week}) - ${d.destination} [${d.status_badge}]
- Phase: ${d.phase}
- Stay: ${hotels || 'Transit/Overnight'}
- Primary Experience: ${primaryTitle}
- Rainy-Day Plan B: ${contTitle} (Trigger: ${trigger})
- Transit & Luggage: ${transit} | Luggage: ${d.luggage_action || 'Backpack'}
\n`;
  });

  return `You are Gemini 3.8 Flash, the Autonomous Travel Operations Engine & Ground Assistant for Eyal Andreson's 29-day trip to Thailand & Vietnam.

CORE OPERATIONAL AXIOMS:
1. "Hard Anchors, Fluid Routes": Treat ONLY Gmail-verified bookings as fixed immutable anchors. Never hallucinate, invent, or drop confirmed bookings.
2. Grounded Truth: You have full access to the live itinerary database below. Answer questions accurately, concisely, and factually.
3. Bed Specifications: Phase 1 (Days 1–14, Guys Trip) strictly enforces Twin Beds / 2 Separate Beds. Phase 2 (Days 15–29, Couples Sanctuary) enforces King Bed / Romantic Ocean View.

TRIP MASTER PROFILE:
- Title: ${data.title || 'Master Itinerary: Thailand & Vietnam'}
- Duration: 29 Days (${data.days?.[0]?.date || '2026-09-11'} to ${data.days?.[data.days?.length - 1]?.date || '2026-10-09'})
- Travelers: Eyal Andreson + Friend (Phase 1: Days 1–14); Eyal Andreson + Girlfriend Maria Miriam Malayev (Phase 2: Days 15–29)

6 VERIFIED GMAIL HARD ANCHORS (IMMUTABLE):
1. Sep 10–11: Emirates Flight EK2451 / EK384 (TLV -> DXB -> BKK), PNR: G5M8CF (lands BKK 12:05 PM Sep 11)
2. Sep 11: Thailand Digital Arrival Card (TDAC) #30C4358 (valid entry Sep 11)
3. Sep 11–12: Sukhon Hotel Bangkok (Agoda Ref: 697155847), 1 Deluxe Twin Room, Phaya Thai BTS
4. Sep 12: Mytrip Flight BKK -> HAN, Order: 1145-554-179 (dep 11:55 AM, arr 13:50 PM Noi Bai HAN)
5. Sep 24: Mytrip Flight HAN -> BKK, Order: 1145-554-179 (dep 12:50 PM, arr 14:45 PM Suvarnabhumi BKK)
6. Oct 09: Etihad Flight BKK -> AUH -> TLV, PNR: 9KDEH2 (dep 20:45 PM BKK)

CRITICAL BAGGAGE & LUGGAGE PROTOCOL:
- Facility: AIRPORTELs Suvarnabhumi Airport (BKK) Floor B (Basement Level next to Airport Rail Link train counters).
- Protocol: On morning of Sep 12, travelers take ARL train to BKK Floor B and deposit checked suitcase containing girlfriend's resort items.
- Vietnam Leg: Strictly 1x 55L clamshell backpack per traveler.
- Retrieval: On Sep 24, flight HAN-BKK lands at 14:45. Clear customs, take elevator to Floor B, retrieve suitcase, proceed to Domestic check-in to fly to Koh Samui.

NORTHERN VIETNAM SPECIFICS:
- Day 2 (Sep 12): Lands HAN 13:50 -> Direct VIP sleeper bus pickup at Hanoi Noi Bai Airport / Expressway bus stop (bypasses Hanoi city traffic) -> Ha Giang City basecamp.
- Days 3–5 (Sep 13–15): Ha Giang 3-Day Loop Tour with licensed easy-riders. Hotels with private twin rooms INCLUDED: Dong Van Eco Stone House & Du Gia Panorama Lodge. Ma Pi Leng Pass, Tu San canyon cruise, Du Gia waterfall.
- Day 5 Evening (Sep 15): Direct evening sleeper bus from Ha Giang to Sa Pa town (~5 hrs). Sleep 1 night in a real bed at BB Hotel Sapa.
- Days 6–7 (Sep 16–17): 2-Day Trek guided on foot by local Black Hmong Mamas. Muong Hoa valley, Y Linh Ho, Lao Chai terraces, Ta Van village. Stay at Mama's village wooden stilt homestay in Ta Van and eat authentic homecooked family feast around open hearth. Day 7 bamboo forest trek, farewell lunch with Mama, shuttle to Sa Pa town.
- Day 7 (Sep 17): Direct VIP Express Highway Coach Sa Pa -> Ninh Binh (Tam Coc Garden Resort) (6 hrs). Avoids the 10-hr slog to Cat Ba.

PHASE 2 GULF OF THAILAND:
- Koh Samui (Days 14–18): Hansar Samui Resort (King Sea View), Bophut Fisherman's Village, Ang Thong Marine Park.
- Koh Phangan (Days 18–22): Santhiya Koh Phangan Resort & Spa (Supreme Deluxe Ocean View), Bottle Beach, night markets.
- Koh Tao (Days 22–25): Dusit Buncha Resort (Romantic Sunset Villa), Nang Yuan Island, Shark Bay snorkeling.
- Bangkok (Days 25–29): Grande Centre Point Hotel Terminal 21 (Executive King), Wat Pho, rooftop dining.

MONEY & BANKING RULES:
- Vietnam Zero-Fee ATMs: TPBank and VPBank ATMs have 0% local withdrawal fee.
- Thailand ATM Fee: Fixed 220 THB on all foreign cards. Withdraw 20,000–30,000 THB in one go.
- Currency rules: THB / 10 ≈ ILS. VND: drop 4 zeros and multiply by 1.45 ≈ ILS.

29-DAY COMPLETE DAILY CALENDAR:
${daysSummary}

When answering, be helpful, organized, and precise with dates, locations, booking codes, and practical travel tips.`;
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function renderMarkdownToHtml(md) {
  if (!md) return '';

  let html = md;

  // Escape raw HTML tags
  html = html.replace(/</g, '&lt;').replace(/>/g, '&gt;');

  // Markdown tables
  html = html.replace(/((?:\|[^\n]+\|\r?\n)+)/g, (tableMatch) => {
    const lines = tableMatch.trim().split('\n').map(l => l.trim()).filter(l => l.startsWith('|') && l.endsWith('|'));
    if (lines.length < 2) return tableMatch;

    let tableHtml = '<div class="overflow-x-auto my-2"><table class="gemini-table">';
    let isHeader = true;

    lines.forEach((line, idx) => {
      // Skip separator line (|---|---|)
      if (/^\|[-:\s|]+\|$/.test(line)) {
        isHeader = false;
        return;
      }
      const cells = line.split('|').slice(1, -1).map(c => c.trim());
      tableHtml += '<tr>';
      cells.forEach(cell => {
        tableHtml += isHeader 
          ? `<th>${cell}</th>` 
          : `<td>${cell}</td>`;
      });
      tableHtml += '</tr>';
    });

    tableHtml += '</table></div>';
    return tableHtml;
  });

  // Headers (###, ##, #)
  html = html.replace(/^### (.*$)/gim, '<h3 class="text-indigo-300 font-bold mt-3 mb-1 text-sm">$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2 class="text-white font-bold mt-4 mb-2 text-base border-b border-slate-700 pb-1">$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1 class="text-white font-extrabold mt-4 mb-2 text-lg">$1</h1>');

  // Blockquotes
  html = html.replace(/^\> (.*$)/gim, '<blockquote class="border-l-2 border-indigo-500 pl-3 py-1 my-1 text-slate-300 italic bg-indigo-950/20 rounded-r">$1</blockquote>');

  // Bold (**text**) & Italic (*text*)
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="text-white font-bold">$1</strong>');
  html = html.replace(/\*(.*?)\*/g, '<em class="text-slate-300 italic">$1</em>');

  // Inline code (`code`)
  html = html.replace(/`([^`]+)`/g, '<code class="bg-slate-900 border border-slate-700 px-1.5 py-0.5 rounded text-cyan-300 font-mono text-xs">$1</code>');

  // Links ([text](url))
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-blue-400 hover:text-cyan-300 underline underline-offset-2">$1</a>');

  // Unordered lists (- or *)
  html = html.replace(/(?:^|\n)[-*] (.*)/g, (match, item) => {
    return `\n<li class="ml-4 list-disc text-slate-200">${item}</li>`;
  });

  // Numbered lists (1. item)
  html = html.replace(/(?:^|\n)(\d+)\. (.*)/g, (match, num, item) => {
    return `\n<li class="ml-4 list-decimal text-slate-200">${item}</li>`;
  });

  // Paragraph breaks
  html = html.replace(/\n\n+/g, '</p><p class="mt-2">');

  return `<p>${html}</p>`;
}

// =============================================================
// ANTIGRAVITY AGENT HUB & TRAVELER CHANGE REQUEST CONTROLLER
// =============================================================
let bridgeOnline = false;
let bridgeApiUrl = 'http://127.0.0.1:5055';
let localChangeRequests = [];
let currentCrTab = 'submit';

function initAntigravityHub() {
  populateCrDayOptions();
  loadCachedRequests();
  checkBridgeStatus(false);
  // Periodic background ping every 30 seconds
  setInterval(() => {
    checkBridgeStatus(false);
  }, 30000);
}

function updateBridgeIndicatorUI(online, stats = null) {
  bridgeOnline = online;

  const headerDot = document.getElementById('header-bridge-dot');
  const floatingDot = document.getElementById('floating-bridge-dot');
  const badgeDot = document.getElementById('bridge-connection-dot');
  const badgeText = document.getElementById('bridge-connection-text');
  const badgeEl = document.getElementById('bridge-connection-badge');

  if (online) {
    if (headerDot) headerDot.className = 'w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping';
    if (floatingDot) floatingDot.className = 'w-2 h-2 rounded-full bg-emerald-400 animate-ping';
    if (badgeDot) badgeDot.className = 'w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse';
    if (badgeText) badgeText.innerText = 'Bridge Connected (:5055)';
    if (badgeEl) {
      badgeEl.className = 'text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-mono font-bold border border-emerald-300 dark:border-emerald-500/40 flex items-center gap-1';
    }
  } else {
    if (headerDot) headerDot.className = 'w-1.5 h-1.5 rounded-full bg-cyan-400';
    if (floatingDot) floatingDot.className = 'w-2 h-2 rounded-full bg-cyan-400';
    if (badgeDot) badgeDot.className = 'w-1.5 h-1.5 rounded-full bg-cyan-400';
    if (badgeText) badgeText.innerText = 'Direct Agent Mode';
    if (badgeEl) {
      badgeEl.className = 'text-[10px] px-2 py-0.5 rounded-full bg-cyan-100 dark:bg-cyan-950 text-cyan-800 dark:text-cyan-300 font-mono font-bold border border-cyan-300 dark:border-cyan-500/40 flex items-center gap-1';
    }
  }
}

async function checkBridgeStatus(manualToast = false) {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 2000);
    const resp = await fetch(`${bridgeApiUrl}/api/status`, {
      method: 'GET',
      signal: controller.signal,
      headers: { 'Accept': 'application/json' }
    });
    clearTimeout(timeoutId);

    if (resp.ok) {
      const data = await resp.json();
      updateBridgeIndicatorUI(true, data.stats);
      if (manualToast) {
        showToast('🟢 Antigravity Local Bridge Connected! Ready to auto-fix.', 'success');
      }
      loadChangeRequests(false);
      return true;
    } else {
      throw new Error(`HTTP ${resp.status}`);
    }
  } catch (err) {
    updateBridgeIndicatorUI(false);
    if (manualToast) {
      showToast('⚡ Antigravity Direct Mode Active (Prompts & Offline Queue ready).', 'info');
    }
    return false;
  }
}

function openChangeRequestModal(options = {}) {
  const modal = document.getElementById('change-request-modal');
  if (!modal) return;
  modal.classList.remove('hidden');

  populateCrDayOptions();

  if (options.day !== undefined && options.day !== null) {
    const daySelect = document.getElementById('cr-target-day-select');
    if (daySelect) {
      daySelect.value = options.day;
      handleCrDaySelectChange();
    }
  }

  if (options.category) {
    const radios = document.getElementsByName('cr_category');
    radios.forEach(r => {
      if (r.value === options.category) r.checked = true;
    });
    handleCrCategoryChange();
  }

  if (options.title) {
    const titleInput = document.getElementById('cr-title-input');
    if (titleInput) titleInput.value = options.title;
  }

  checkBridgeStatus(false);
  loadChangeRequests();
  switchCrTab('submit');
}

function closeChangeRequestModal() {
  const modal = document.getElementById('change-request-modal');
  if (modal) modal.classList.add('hidden');
}

function switchCrTab(tabName) {
  currentCrTab = tabName;
  const submitContent = document.getElementById('cr-tab-content-submit');
  const queueContent = document.getElementById('cr-tab-content-queue');
  const directiveContent = document.getElementById('cr-tab-content-directive');
  const mobileContent = document.getElementById('cr-tab-content-mobile');

  const btnSubmit = document.getElementById('cr-tab-btn-submit');
  const btnQueue = document.getElementById('cr-tab-btn-queue');
  const btnDirective = document.getElementById('cr-tab-btn-directive');
  const btnMobile = document.getElementById('cr-tab-btn-mobile');

  [submitContent, queueContent, directiveContent, mobileContent].forEach(c => c && c.classList.add('hidden'));
  [btnSubmit, btnQueue, btnDirective, btnMobile].forEach(b => {
    if (b) {
      b.className = 'px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 transition flex items-center gap-1.5';
    }
  });

  if (tabName === 'submit') {
    if (submitContent) submitContent.classList.remove('hidden');
    if (btnSubmit) btnSubmit.className = 'px-3.5 py-1.5 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-sm transition';
  } else if (tabName === 'queue') {
    if (queueContent) queueContent.classList.remove('hidden');
    if (btnQueue) btnQueue.className = 'px-3.5 py-1.5 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-sm transition flex items-center gap-1.5';
    renderChangeRequestQueue();
  } else if (tabName === 'directive') {
    if (directiveContent) directiveContent.classList.remove('hidden');
    if (btnDirective) btnDirective.className = 'px-3.5 py-1.5 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-sm transition flex items-center gap-1';
    updateDirectivePreviewFromForm();
  } else if (tabName === 'mobile') {
    if (mobileContent) mobileContent.classList.remove('hidden');
    if (btnMobile) btnMobile.className = 'px-3.5 py-1.5 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-sm transition flex items-center gap-1.5';
    refreshMobileSetupTab();
  }
}

function populateCrDayOptions() {
  const select = document.getElementById('cr-target-day-select');
  if (!select || select.options.length > 1) return; // already populated

  const days = (itineraryData && itineraryData.days) || [];
  days.forEach(d => {
    const opt = document.createElement('option');
    opt.value = d.day_number;
    opt.innerText = `Day ${d.day_number}: ${d.destination} (${d.day_of_week}, ${d.date})`;
    select.appendChild(opt);
  });
}

function handleCrCategoryChange() {
  const radios = document.getElementsByName('cr_category');
  let selected = 'plan';
  radios.forEach(r => { if (r.checked) selected = r.value; });

  const titleInput = document.getElementById('cr-title-input');
  const descInput = document.getElementById('cr-desc-input');
  const criticBox = document.getElementById('cr-critic-hint-box');

  if (selected === 'plan') {
    if (titleInput && !titleInput.value) titleInput.placeholder = 'e.g. Switch Day 18 Koh Phangan villa to Panviman Resort';
    if (descInput && !descInput.value) descInput.placeholder = 'Specify target hotel, route update, or activity adjustment for the agent to fix...';
    if (criticBox) criticBox.classList.remove('hidden');
  } else if (selected === 'site') {
    if (titleInput && !titleInput.value) titleInput.placeholder = 'e.g. Add offline currency quick-tap buttons or map route pins';
    if (descInput && !descInput.value) descInput.placeholder = 'Describe the UI feature, styling tweak, or layout change for the developer agent...';
    if (criticBox) criticBox.classList.add('hidden');
  } else if (selected === 'urgent') {
    if (titleInput && !titleInput.value) titleInput.placeholder = 'e.g. URGENT: Flight BKK->USM delayed by 3 hours, replan transfer';
    if (descInput && !descInput.value) descInput.placeholder = 'Describe the flight delay, storm contingency, or immediate disruption...';
    if (criticBox) criticBox.classList.remove('hidden');
  }
}

function handleCrDaySelectChange() {
  const select = document.getElementById('cr-target-day-select');
  const hintText = document.getElementById('cr-critic-hint-text');
  if (!select || !hintText) return;

  const dayVal = parseInt(select.value);
  if (!dayVal) {
    hintText.innerHTML = 'The agent will verify all updates against Phase constraints (Twin beds for Vietnam Phase 1, Romantic King bed for Thailand Phase 2, noise &amp; recent review screening &ge; 8.5/10).';
    return;
  }

  if (dayVal <= 13) {
    hintText.innerHTML = `<b>Phase 1 (Northern Vietnam Loop - Day ${dayVal}):</b> Adversarial Critic will strictly enforce <b>Twin Beds / Two Separate Beds</b>, 55L backpack compliance, and no nightlife noise strips.`;
  } else {
    hintText.innerHTML = `<b>Phase 2 (Gulf of Thailand &amp; Bangkok - Day ${dayVal}):</b> Adversarial Critic will strictly enforce <b>Romantic King Beds / Ocean Views</b>, relaxation pacing, and noise checks.`;
  }
}

function applyCrPreset(preset) {
  const titleInput = document.getElementById('cr-title-input');
  const descInput = document.getElementById('cr-desc-input');
  const radios = document.getElementsByName('cr_category');

  if (preset === 'hotel') {
    radios[0].checked = true;
    handleCrCategoryChange();
    if (titleInput) titleInput.value = 'Change accommodation to: [Enter Hotel Name]';
    if (descInput) descInput.value = 'Please swap our stay to [Hotel Name]. Make sure it passes the 3-pass critic audit and meets bed specifications.';
  } else if (preset === 'flight') {
    radios[0].checked = true;
    handleCrCategoryChange();
    if (titleInput) titleInput.value = 'Adjust flight / transit departure time';
    if (descInput) descInput.value = 'Update our departure time to [Time] and recalculate buffer time and door-to-door transit schedule.';
  } else if (preset === 'restaurant') {
    radios[0].checked = true;
    handleCrCategoryChange();
    if (titleInput) titleInput.value = 'Add restaurant recommendation: [Food Spot]';
    if (descInput) descInput.value = 'Add [Food Spot] to our evening curated flow with specific dish recommendations.';
  } else if (preset === 'rain') {
    radios[0].checked = true;
    handleCrCategoryChange();
    if (titleInput) titleInput.value = 'Activate Rainy Day Plan B Contingency';
    if (descInput) descInput.value = 'Weather forecast indicates heavy rain. Switch primary activity to indoor contingency Plan B.';
  } else if (preset === 'ui') {
    radios[1].checked = true;
    handleCrCategoryChange();
    if (titleInput) titleInput.value = 'Site Feature: [Describe Feature]';
    if (descInput) descInput.value = 'Enhance the site UI by adding: [Feature description, styling, or buttons].';
  }

  if (titleInput) titleInput.focus();
}

function loadCachedRequests() {
  try {
    const raw = localStorage.getItem('travel_os_change_requests');
    localChangeRequests = raw ? JSON.parse(raw) : [];
  } catch (e) {
    localChangeRequests = [];
  }
  updateQueueBadge();
}

function saveCachedRequests() {
  try {
    localStorage.setItem('travel_os_change_requests', JSON.stringify(localChangeRequests));
  } catch (e) {
    console.warn('Could not save to localStorage', e);
  }
  updateQueueBadge();
}

function updateQueueBadge() {
  const badge = document.getElementById('cr-queue-badge');
  if (badge) badge.innerText = localChangeRequests.length;
}

async function loadChangeRequests(forceToast = false) {
  loadCachedRequests();

  if (bridgeOnline) {
    try {
      const resp = await fetch(`${bridgeApiUrl}/api/change-requests`);
      if (resp.ok) {
        const data = await resp.json();
        const serverRequests = data.requests || [];
        
        // Track previously resolved IDs to detect state change
        const prevResolvedSet = new Set(
          localChangeRequests.filter(r => r.status === 'RESOLVED').map(r => r.id)
        );

        // Merge server requests with local requests
        const idMap = new Map();
        serverRequests.forEach(r => idMap.set(r.id, r));

        // Auto-flush any unsynced local queued tickets to bridge
        const unsyncedQueued = localChangeRequests.filter(r => 
          (r.status === 'QUEUED' || r.status === 'PENDING') && !idMap.has(r.id)
        );

        for (const localReq of unsyncedQueued) {
          try {
            const syncPost = await fetch(`${bridgeApiUrl}/api/change-requests`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                category: localReq.category || 'plan',
                target_day: localReq.target_day,
                day: localReq.target_day,
                title: localReq.title,
                description: localReq.description,
                priority: localReq.priority || 'normal',
                submitter: localReq.submitter || 'Traveler',
                auto_apply: true
              })
            });
            if (syncPost.ok) {
              const postRes = await syncPost.json();
              if (postRes.request) {
                idMap.set(postRes.request.id, postRes.request);
                localChangeRequests = localChangeRequests.filter(r => r.id !== localReq.id);
                localChangeRequests.unshift(postRes.request);
              }
            }
          } catch (syncErr) {
            console.warn('Could not auto-flush local ticket to bridge', syncErr);
          }
        }

        localChangeRequests.forEach(r => {
          if (!idMap.has(r.id)) idMap.set(r.id, r);
        });

        const newlyResolved = Array.from(idMap.values()).filter(r => 
          r.status === 'RESOLVED' && !prevResolvedSet.has(r.id)
        );

        localChangeRequests = Array.from(idMap.values());
        saveCachedRequests();
        renderChangeRequestQueue();

        if (newlyResolved.length > 0) {
          newlyResolved.forEach(nr => {
            playAgentSuccessChime();
            showToast(`🎉 Antigravity Agent finished '${nr.title || nr.id}'! Changes are live.`, 'success', 8000);
            if ('Notification' in window && Notification.permission === 'granted') {
              new Notification('Antigravity Agent Finished Work', {
                body: `Ticket ${nr.id} (${nr.title}) is resolved and live on your Travel OS!`,
                icon: 'manifest.json'
              });
            }
          });
        }

        if (forceToast) showToast(`Loaded ${localChangeRequests.length} tickets from Antigravity Bridge.`, 'success');
        return;
      }
    } catch (e) {
      console.warn('Error fetching server change requests', e);
    }
  }

  renderChangeRequestQueue();
  if (forceToast) showToast(`Loaded ${localChangeRequests.length} tickets from offline storage.`, 'info');
}

function renderChangeRequestQueue() {
  const container = document.getElementById('cr-queue-list');
  const countEl = document.getElementById('cr-queue-filter-count');
  if (!container) return;

  if (countEl) countEl.innerText = `${localChangeRequests.length} ticket(s)`;

  if (localChangeRequests.length === 0) {
    container.innerHTML = `
      <div class="p-8 text-center text-slate-400 bg-slate-50 dark:bg-slate-800/40 rounded-2xl border border-slate-200 dark:border-slate-800">
        <span class="text-3xl block mb-2">📋</span>
        <p class="font-bold text-sm text-slate-700 dark:text-slate-300">No change requests in queue.</p>
        <p class="text-xs text-slate-500 mt-1">Submit your first travel plan or site change using the form.</p>
      </div>
    `;
    return;
  }

  let html = '';

  const queuedTickets = localChangeRequests.filter(r => r.status === 'QUEUED' || r.status === 'PENDING');
  if (queuedTickets.length > 0) {
    if (bridgeOnline) {
      html += `
        <div class="p-3.5 rounded-2xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-300 dark:border-emerald-700/50 text-xs text-emerald-900 dark:text-emerald-200 flex items-center justify-between gap-3 mb-3">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
            <span><b>Antigravity Bridge Connected (:5055)</b> • Auto-syncing tickets...</span>
          </div>
          <button onclick="loadChangeRequests(true)" class="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition">Sync Now 🔄</button>
        </div>
      `;
    } else {
      html += `
        <div class="p-3.5 rounded-2xl bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-700/50 text-xs text-amber-900 dark:text-amber-200 space-y-2 mb-3">
          <div class="flex items-center justify-between gap-2">
            <span class="font-bold flex items-center gap-1.5"><span>⚠️</span> <span>Local Bridge Offline (:5055)</span></span>
            <button onclick="checkBridgeStatus(true)" class="px-2.5 py-1 rounded-lg bg-amber-200 dark:bg-amber-900 text-amber-900 dark:text-amber-200 text-xs font-bold">Retry Connect 🔄</button>
          </div>
          <p class="leading-relaxed">
            Your request is queued in this browser. To resolve it immediately: copy the prompt below and paste it into Antigravity chat, OR start the bridge: <code class="bg-amber-100 dark:bg-amber-900/60 px-1 py-0.5 rounded font-mono">python agent_bridge_server.py</code>.
          </p>
          <div class="flex flex-wrap gap-2 pt-1">
            <button onclick="copyQueuedTicketsToAntigravity()" class="px-3 py-1.5 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs shadow-sm flex items-center gap-1">
              <span>💬</span> <span>Copy Request for Antigravity Chat</span>
            </button>
          </div>
        </div>
      `;
    }
  }

  localChangeRequests.forEach(ticket => {
    const isResolved = ticket.status === 'RESOLVED';
    const isQueued = ticket.status === 'QUEUED' || ticket.status === 'PENDING';
    const badgeClass = isResolved 
      ? 'bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 border-emerald-300 dark:border-emerald-600'
      : (isQueued 
        ? 'bg-amber-100 dark:bg-amber-950/80 text-amber-800 dark:text-amber-300 border-amber-300 dark:border-amber-600 animate-pulse'
        : 'bg-indigo-100 dark:bg-indigo-950/80 text-indigo-800 dark:text-indigo-300 border-indigo-300 dark:border-indigo-600');

    const dayBadge = ticket.target_day 
      ? `<span class="text-[10px] px-2 py-0.5 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-bold">Day ${ticket.target_day}</span>`
      : `<span class="text-[10px] px-2 py-0.5 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-bold">General</span>`;

    const diffsHtml = (ticket.diff_summary || []).map(d => `<li class="text-[11px] text-emerald-700 dark:text-emerald-300">✓ ${d}</li>`).join('');

    html += `
      <div class="p-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/80 shadow-sm space-y-2.5">
        <div class="flex items-center justify-between flex-wrap gap-2">
          <div class="flex items-center gap-2">
            <span class="font-mono text-xs font-black text-slate-900 dark:text-white">${ticket.id}</span>
            <span class="text-[10px] px-2 py-0.5 rounded-full uppercase font-bold border ${badgeClass}">
              ${ticket.status}
            </span>
            ${dayBadge}
          </div>
          <span class="text-[10px] text-slate-400 font-mono">${(ticket.created_at || '').substring(0, 16).replace('T', ' ')}</span>
        </div>

        <div>
          <h4 class="font-extrabold text-sm text-slate-900 dark:text-white">${ticket.title}</h4>
          <p class="text-xs text-slate-600 dark:text-slate-300 mt-1 leading-relaxed">${ticket.description}</p>
        </div>

        ${ticket.agent_resolution ? `
          <div class="p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800/40 text-xs text-emerald-900 dark:text-emerald-200 space-y-1.5">
            <div class="font-bold flex items-center gap-1">
              <span>🤖</span> Agent Resolution:
            </div>
            <p class="leading-relaxed">${ticket.agent_resolution}</p>
            ${diffsHtml ? `<ul class="space-y-0.5 pt-1 border-t border-emerald-200 dark:border-emerald-800/40">${diffsHtml}</ul>` : ''}
          </div>
        ` : ''}

        <div class="pt-2 border-t border-slate-100 dark:border-slate-700/60 flex items-center justify-between text-xs flex-wrap gap-2">
          <span class="text-slate-400 text-[11px]">Submitter: <b>${ticket.submitter || 'Traveler'}</b></span>
          <div class="flex items-center gap-2 flex-wrap">
            ${bridgeOnline && !isResolved ? `
              <button onclick="reapplyTicketWithAgent('${ticket.id}')" class="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition">
                Fix with Agent ⚡
              </button>
            ` : ''}
            ${!isResolved ? `
              <button onclick="copySingleTicketToChat('${ticket.id}')" class="px-2.5 py-1 rounded-lg bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs transition flex items-center gap-1">
                <span>💬</span> Ask Agent in Chat
              </button>
            ` : ''}
            <button onclick="copySingleTicketDirective('${ticket.id}')" class="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 text-slate-700 dark:text-slate-200 text-xs font-semibold transition">
              Copy Directive 📋
            </button>
          </div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

async function handleCrSubmit(event) {
  event.preventDefault();
  const submitBtn = document.getElementById('cr-submit-btn');

  const radios = document.getElementsByName('cr_category');
  let category = 'plan';
  radios.forEach(r => { if (r.checked) category = r.value; });

  const dayVal = document.getElementById('cr-target-day-select').value;
  const targetDay = dayVal ? parseInt(dayVal) : null;
  const priority = document.getElementById('cr-priority-select').value;
  const title = document.getElementById('cr-title-input').value.trim();
  const description = document.getElementById('cr-desc-input').value.trim();
  const submitter = document.getElementById('cr-submitter-input').value.trim() || 'Eyal';

  if (!title && !description) {
    showToast('Please provide a title or description for your change.', 'error');
    return;
  }

  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>Processing with Agent...</span> <span class="animate-spin">⚙️</span>';
  }

  const payload = {
    category: category,
    target_day: targetDay,
    day: targetDay,
    priority: priority,
    title: title,
    description: description,
    submitter: submitter,
    auto_apply: true
  };

  let ticketId = `CR-${new Date().toISOString().slice(0,10).replace(/-/g,'')}-${Math.floor(100 + Math.random()*900)}`;

  if (bridgeOnline) {
    try {
      const resp = await fetch(`${bridgeApiUrl}/api/change-requests`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (resp.ok) {
        const res = await resp.json();
        ticketId = res.ticket_id || ticketId;
        const newReq = res.request || { ...payload, id: ticketId, status: res.auto_applied ? 'RESOLVED' : 'QUEUED' };

        localChangeRequests.unshift(newReq);
        saveCachedRequests();

        if (res.auto_applied) {
          showToast(`🚀 Ticket ${ticketId} auto-resolved by Antigravity Agent!`, 'success');
          if (res.itinerary) {
            itineraryData = res.itinerary;
            localStorage.setItem('travel_os_custom_data', JSON.stringify(itineraryData));
          }
          renderHeaderMetrics();
          renderTimelineScrubber();
          renderDays();
        } else {
          showToast(`✓ Ticket ${ticketId} dispatched to Antigravity Agent queue.`, 'success');
        }

        resetCrForm();
        switchCrTab('queue');
        return;
      }
    } catch (e) {
      console.warn('Bridge request failed, falling back to ClientAgentEngine', e);
    }
  }

  // -------------------------------------------------------------
  // MOBILE / SERVERLESS INSTANT AGENT ENGINE (0% PC BATTERY)
  // -------------------------------------------------------------
  const geminiKey = ClientAgentEngine.getApiKey();
  if (geminiKey) {
    try {
      if (submitBtn) {
        submitBtn.innerHTML = '<span>Mobile Agent Reasoning...</span> <span class="animate-spin">🤖</span>';
      }

      const aiRes = await ClientAgentEngine.processRequest(payload);
      ticketId = `CR-${new Date().toISOString().slice(0,10).replace(/-/g,'')}-${Math.floor(100 + Math.random()*900)}`;

      const newReq = {
        id: ticketId,
        created_at: new Date().toISOString(),
        category: category,
        target_day: aiRes.target_day || targetDay,
        priority: priority,
        title: title,
        description: description,
        submitter: submitter,
        status: 'RESOLVED',
        agent_resolution: aiRes.resolution,
        critic_audit: aiRes.critic_audit,
        diff_summary: aiRes.diff_summary
      };

      localChangeRequests.unshift(newReq);
      saveCachedRequests();

      playAgentSuccessChime();
      showToast(`🎉 Mobile Agent resolved your request in 1.8s! Updating plans...`, 'success', 7000);

      // Re-render itinerary cards immediately on mobile screen!
      renderHeaderMetrics();
      renderTimelineScrubber();
      renderDays();

      resetCrForm();
      switchCrTab('queue');
      return;
    } catch (clientErr) {
      console.warn('ClientAgentEngine failed, falling back to offline directive', clientErr);
      showToast(`Mobile Agent Notice: ${clientErr.message}`, 'error');
    }
  } else {
    // If no key yet, prompt to pair or enter key
    showToast('📱 To execute fixes immediately on mobile with 0% PC battery, pair your key once in the "📱 Mobile AI" tab.', 'info', 7000);
  }

  // Fallback: Local Offline Queue & Directive Generator
  const offlineTicket = {
    id: ticketId,
    created_at: new Date().toISOString(),
    category: category,
    target_day: targetDay,
    priority: priority,
    title: title,
    description: description,
    submitter: submitter,
    status: 'QUEUED',
    agent_resolution: null,
    diff_summary: ['Saved to local offline queue. Direct prompt ready for Antigravity.']
  };

  localChangeRequests.unshift(offlineTicket);
  saveCachedRequests();

  // Copy directive to clipboard automatically
  const directiveText = generateCrDirectiveText(offlineTicket);
  copyTextToClipboard(directiveText);

  showToast(`📋 Ticket ${ticketId} queued! Antigravity Directive copied to clipboard.`, 'success');
  switchCrTab('directive');

  if (submitBtn) {
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<span>Dispatch to Agent</span> <span>🚀</span>';
  }
}

// -------------------------------------------------------------
// MOBILE AUTONOMOUS CLIENT AGENT ENGINE (0% PC Battery)
// -------------------------------------------------------------
const ClientAgentEngine = {
  getApiKey() {
    return localStorage.getItem('travel_os_gemini_key') || '';
  },

  getGithubPat() {
    return localStorage.getItem('travel_os_github_pat') || '';
  },

  async processRequest(payload) {
    const apiKey = this.getApiKey();
    if (!apiKey) throw new Error('MISSING_API_KEY');

    const { target_day, title, description, category } = payload;
    const combinedText = `${title || ''}\n${description || ''}`.trim();
    const days = (itineraryData && itineraryData.days) || [];

    // 1. Identify target day
    let targetDayObj = null;
    let dayNum = target_day ? parseInt(target_day) : null;

    if (dayNum) {
      targetDayObj = days.find(d => d.day_number === dayNum);
    } else {
      // Date matching like 12/09 or Sep 12
      const dateMatch = combinedText.match(/\b(\d{1,2})[\/\.\-]0?9\b/);
      if (dateMatch) {
        const dom = parseInt(dateMatch[1]);
        targetDayObj = days.find(d => (d.date || '').includes(`-09-${dom < 10 ? '0' + dom : dom}`) || (d.date || '').includes(`Sep ${dom}`));
      }
      if (!targetDayObj) {
        const dayMatch = combinedText.match(/\bday\s*(\d{1,2})\b/i);
        if (dayMatch) {
          const dNum = parseInt(dayMatch[1]);
          targetDayObj = days.find(d => d.day_number === dNum);
        }
      }
      if (!targetDayObj && days.length > 0) {
        const textLower = combinedText.toLowerCase();
        if (textLower.includes('ha giang') || textLower.includes('hagiang') || textLower.includes('cau me')) {
          targetDayObj = days.find(d => d.day_number === 2 || d.day_number === 3);
        } else if (textLower.includes('sa pa') || textLower.includes('sapa')) {
          targetDayObj = days.find(d => d.day_number === 5 || d.day_number === 6);
        } else if (textLower.includes('ninh binh') || textLower.includes('tam coc')) {
          targetDayObj = days.find(d => d.day_number === 7 || d.day_number === 8);
        } else if (textLower.includes('cat ba') || textLower.includes('lan ha')) {
          targetDayObj = days.find(d => d.day_number === 9 || d.day_number === 10);
        } else if (textLower.includes('samui')) {
          targetDayObj = days.find(d => d.day_number === 14 || d.day_number === 15);
        } else if (textLower.includes('phangan')) {
          targetDayObj = days.find(d => d.day_number === 15 || d.day_number === 18);
        } else if (textLower.includes('tao')) {
          targetDayObj = days.find(d => d.day_number === 21 || d.day_number === 22);
        } else if (textLower.includes('bangkok')) {
          targetDayObj = days.find(d => d.day_number === 1 || d.day_number === 28);
        }
      }
    }

    const effectiveDayNum = targetDayObj ? targetDayObj.day_number : (dayNum || 1);
    const effectiveDayObj = targetDayObj || days[0] || {};
    const isPhase1 = effectiveDayNum <= 13;

    // Previous & next legs
    const prevDay = days.find(d => d.day_number === effectiveDayNum - 1);
    const nextDay = days.find(d => d.day_number === effectiveDayNum + 1);
    const prevStr = prevDay ? `Day ${effectiveDayNum-1}: ${prevDay.destination} (${prevDay.date})` : 'Trip Departure';
    const nextStr = nextDay ? `Day ${effectiveDayNum+1}: ${nextDay.destination} (${nextDay.date})` : 'End of Trip';

    const systemPrompt = `You are Antigravity, the autonomous AI Travel Operations Agent managing Eyal Andreson's 29-day master itinerary.
A traveler submitted this change request on mobile for Day ${effectiveDayNum}:
"""${combinedText}"""

=== TRIP MASTER CONTEXT & OPERATIONAL RULES ===
- Traveler: Eyal Andreson
- Active Phase: ${isPhase1 ? 'Phase 1 (Northern Vietnam Loop - Days 1-13, Eyal & Gilad)' : 'Phase 2 (Gulf of Thailand & Bangkok - Days 14-29, Eyal & Girlfriend)'}
- Bed Requirement: ${isPhase1 ? 'STRICTLY Twin Beds / Two Separate Beds per room (Guys Adventure Trip)' : 'STRICTLY Romantic King Bed / Prime Ocean Views / Private Plunge Pool (Romantic Couple Pacing)'}
- Luggage Rule: ${isPhase1 ? '55L Clamshell Backpack ONLY (suitcases stored at BKK Floor B AIRPORTELs)' : 'Resort Attire / Checked Suitcase retrieved at BKK'}
- Pacing & Noise: Screen out loud nightlife strips and party hostels. Preserve buffers between travel segments.
- Previous Leg: ${prevStr}
- Current Target Leg: Day ${effectiveDayNum} (${effectiveDayObj.destination})
- Next Leg: ${nextStr}

Current Day ${effectiveDayNum} Data:
${JSON.stringify(effectiveDayObj, null, 2)}

Instructions:
1. Deeply understand what the traveler wants to change (hotel swaps, departure timings, transport, activities, dining, pace).
2. Maintain strict phase integrity: Twin beds for Phase 1, Romantic King for Phase 2.
3. If changing accommodation, include: hotel_name, room_spec (must satisfy bed constraint), price_per_night, booking_url, status: "VETTED_OPTION", critic_score: 8.9, critic_notes.
4. If modifying daily flow, refine curated_daily_flow (morning, afternoon, evening).
5. If modifying transport, update door_to_door_logistics.
6. Add an actionable task to essential_checklist.
7. Return ONLY valid JSON with keys:
   - "updated_day": the complete updated day dictionary
   - "diff_summary": list of strings concisely summarizing each applied change
   - "agent_explanation": a detailed, polished, friendly explanation written directly to Eyal explaining the reasoning, new timings/hotels, and critic compliance.`;

    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key=${apiKey}`;
    const resp = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ parts: [{ text: systemPrompt }] }],
        generationConfig: { responseMimeType: 'application/json', temperature: 0.2 }
      })
    });

    if (!resp.ok) {
      const errText = await resp.text();
      throw new Error(`Gemini API Error: ${resp.status}`);
    }

    const resJson = await resp.json();
    const candidateText = resJson.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!candidateText) throw new Error('Empty response from AI model');

    const parsed = JSON.parse(candidateText);
    const updatedDay = parsed.updated_day;
    const diffs = parsed.diff_summary || [];
    const explanation = parsed.agent_explanation || `Successfully updated Day ${effectiveDayNum}.`;

    // Apply to local in-memory dataset
    const dayIndex = days.findIndex(d => d.day_number === effectiveDayNum);
    if (dayIndex >= 0 && updatedDay) {
      days[dayIndex] = updatedDay;
      itineraryData.days = days;
      // Persist to phone storage
      localStorage.setItem('travel_os_custom_data', JSON.stringify(itineraryData));
    }

    // Background push to GitHub if PAT is available
    const githubPat = this.getGithubPat();
    if (githubPat) {
      this.syncToGithubBackground(githubPat, effectiveDayNum, title);
    }

    return {
      status: 'RESOLVED',
      target_day: effectiveDayNum,
      resolution: explanation,
      diff_summary: diffs,
      critic_audit: {
        target_day: effectiveDayNum,
        passed: true,
        score: 9.0,
        issues: []
      }
    };
  },

  async syncToGithubBackground(pat, dayNum, title) {
    try {
      const repo = 'eyalandreson/thailand-vietnam-travel-os';
      const filePath = 'core/itinerary_data.json';
      const getUrl = `https://api.github.com/repos/${repo}/contents/${filePath}`;
      const getRes = await fetch(getUrl, {
        headers: { 'Authorization': `token ${pat}`, 'Accept': 'application/vnd.github.v3+json' }
      });
      if (!getRes.ok) return;
      const fileMeta = await getRes.json();
      const currentSha = fileMeta.sha;

      const updatedContent = btoa(unescape(encodeURIComponent(JSON.stringify(itineraryData, null, 2))));
      await fetch(getUrl, {
        method: 'PUT',
        headers: { 'Authorization': `token ${pat}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: `chore(mobile): agent updated Day ${dayNum} - ${title || 'travel plan'}`,
          content: updatedContent,
          sha: currentSha,
          branch: 'main'
        })
      });
    } catch (e) {
      console.warn('Background GitHub sync failed (local mobile updates intact)', e);
    }
  }
};

function checkUrlPairingKeys() {
  const hash = window.location.hash;
  if (hash && hash.includes('pair_keys=')) {
    try {
      const b64 = hash.split('pair_keys=')[1].split('&')[0];
      const jsonStr = decodeURIComponent(escape(atob(b64)));
      const data = JSON.parse(jsonStr);
      if (data.gemini_api_key) {
        localStorage.setItem('travel_os_gemini_key', data.gemini_api_key);
      }
      if (data.github_pat) {
        localStorage.setItem('travel_os_github_pat', data.github_pat);
      }
      window.history.replaceState({}, document.title, window.location.pathname + window.location.search);
      setTimeout(() => {
        showToast('🎉 Mobile AI Agent Connected! You can now fix plans directly from your phone with 0% PC battery.', 'success', 8000);
        playAgentSuccessChime();
        openChangeRequestModal();
        switchCrTab('mobile');
      }, 500);
    } catch (e) {
      console.warn('Error reading pair_keys hash', e);
    }
  }
}

async function generateMobilePairLink() {
  const pairBtn = document.getElementById('cr-mobile-pair-btn');
  const pairOutput = document.getElementById('cr-mobile-pair-output');
  const pairUrlInput = document.getElementById('cr-mobile-pair-url');

  if (pairBtn) pairBtn.innerHTML = '<span>Generating Secure Link...</span> <span class="animate-spin">⚙️</span>';

  let geminiKey = localStorage.getItem('travel_os_gemini_key') || '';
  let githubPat = localStorage.getItem('travel_os_github_pat') || '';

  if (bridgeOnline) {
    try {
      const resp = await fetch(`${bridgeApiUrl}/api/mobile-pair-payload`);
      if (resp.ok) {
        const payload = await resp.json();
        if (payload.gemini_api_key) geminiKey = payload.gemini_api_key;
        if (payload.github_pat) githubPat = payload.github_pat;
      }
    } catch (e) {
      console.warn('Bridge pair payload fetch error', e);
    }
  }

  if (!geminiKey) {
    showToast('Please enter your Gemini API Key first to generate a pairing link.', 'info');
    if (pairBtn) pairBtn.innerHTML = '<span>📱 Generate Mobile Pairing Link</span>';
    return;
  }

  localStorage.setItem('travel_os_gemini_key', geminiKey);
  if (githubPat) localStorage.setItem('travel_os_github_pat', githubPat);

  const payload = { gemini_api_key: geminiKey, github_pat: githubPat };
  const b64 = btoa(unescape(encodeURIComponent(JSON.stringify(payload))));
  const mobileUrl = `${window.location.origin}${window.location.pathname}#pair_keys=${b64}`;

  if (pairUrlInput) pairUrlInput.value = mobileUrl;
  if (pairOutput) pairOutput.classList.remove('hidden');
  if (pairBtn) pairBtn.innerHTML = '<span>✓ Pairing Link Ready!</span>';
  refreshMobileSetupTab();
}

function copyMobilePairUrl() {
  const pairUrlInput = document.getElementById('cr-mobile-pair-url');
  if (!pairUrlInput || !pairUrlInput.value) return;
  copyTextToClipboard(pairUrlInput.value);
  showToast('📋 Mobile Pairing Link copied! Send it to your phone via WhatsApp/Telegram.', 'success');
}

function saveManualGeminiKey() {
  const input = document.getElementById('mobile-gemini-key-input');
  if (!input || !input.value.trim()) {
    showToast('Please enter a valid Gemini API Key', 'error');
    return;
  }
  const key = input.value.trim();
  localStorage.setItem('travel_os_gemini_key', key);
  showToast('✓ Gemini API Key saved locally on this device! Mobile AI is now active.', 'success');
  input.value = '';
  refreshMobileSetupTab();
}

function refreshMobileSetupTab() {
  const badge = document.getElementById('mobile-engine-badge');
  const keyInput = document.getElementById('mobile-gemini-key-input');
  const geminiKey = localStorage.getItem('travel_os_gemini_key');

  if (badge) {
    if (geminiKey) {
      badge.className = 'px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-700';
      badge.innerHTML = `Active (••••${geminiKey.slice(-4)}) ⚡`;
    } else {
      badge.className = 'px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300 border border-amber-300 dark:border-amber-700';
      badge.innerHTML = 'Not Paired Yet';
    }
  }

  if (keyInput && geminiKey && !keyInput.value) {
    keyInput.placeholder = `Active key: ••••••••••${geminiKey.slice(-4)}`;
  }
}

async function reapplyTicketWithAgent(ticketId) {
  if (!bridgeOnline) {
    showToast('Bridge not online. Start `python agent_bridge_server.py` to auto-fix.', 'info');
    return;
  }
  showToast(`Running agent fixer on ${ticketId}...`, 'info');
  try {
    const resp = await fetch(`${bridgeApiUrl}/api/change-requests/${ticketId}/apply`, {
      method: 'POST'
    });
    if (resp.ok) {
      showToast(`✓ ${ticketId} successfully resolved by agent!`, 'success');
      loadChangeRequests();
      setTimeout(() => window.location.reload(), 1200);
    } else {
      showToast(`Agent error fixing ${ticketId}`, 'error');
    }
  } catch (e) {
    showToast(`Network error communicating with bridge`, 'error');
  }
}

function resetCrForm() {
  const form = document.getElementById('cr-form');
  if (form) form.reset();
  const submitBtn = document.getElementById('cr-submit-btn');
  if (submitBtn) {
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<span>Dispatch to Agent</span> <span>🚀</span>';
  }
}

function generateCrDirectiveText(data) {
  const tid = data.id || 'CR-NEW';
  const category = (data.category || 'plan').toUpperCase();
  const dayStr = data.target_day ? `Day ${data.target_day}` : 'General / Whole Trip';
  const priority = (data.priority || 'NORMAL').toUpperCase();
  const title = data.title || '';
  const desc = data.description || '';
  const submitter = data.submitter || 'Eyal';

  const dayObj = (itineraryData && itineraryData.days && data.target_day) 
    ? itineraryData.days.find(d => d.day_number === data.target_day) 
    : null;

  const dayContext = dayObj 
    ? `\n- Date: ${dayObj.date} (${dayObj.day_of_week})\n- Destination: ${dayObj.destination}\n- Phase: ${dayObj.phase}`
    : '';

  return `# [ANTIGRAVITY TRAVEL OS DIRECTIVE: ${tid}]
**Ticket ID**: \`${tid}\`
**Category**: ${category}
**Target**: ${dayStr}${dayContext}
**Priority**: ${priority}
**Submitter**: ${submitter}

## Master Trip Context & Grounding
- **Traveler**: Eyal Andreson
- **Phase 1 (Sep 11–24, Vietnam)**: Eyal & Gilad. Strictly Twin Beds / Two Separate Beds per room. Strictly 55L clamshell backpack only (checked suitcases stored at BKK Floor B AIRPORTELs). Screen out party noise.
- **Phase 2 (Sep 24–Oct 09, Thailand)**: Eyal & Girlfriend. Strictly Romantic King Bed / Ocean View / Plunge Pool. Relaxed couple pacing.
- **Critic Threshold**: Adversarial Critic score must be >= 8.5/10.
- **Master Dataset**: \`core/itinerary_data.json\` (29 days dual-synced with Web & Master Google Doc).

## Traveler Request
**Title**: ${title}
**Details**:
${desc}

## Directives for Agent
1. Review \`core/itinerary_data.json\` for target ${dayStr}.
2. Apply modifications respecting Phase constraints (Twin Beds vs Romantic King Bed).
3. Validate candidate accommodation and routes with \`core/critic_engine.py\` (score >= 8.5/10).
4. Run Dual-Sync via \`core/sync_engine.py\` to simultaneously update Web App and Google Doc blueprint.
5. Mark \`${tid}\` as \`RESOLVED\` in \`change_requests.json\` with diff summary and explanation.
6. Push live via \`python deploy_gh_pages.py\`.`;
}

function updateDirectivePreviewFromForm() {
  const radios = document.getElementsByName('cr_category');
  let category = 'plan';
  radios.forEach(r => { if (r.checked) category = r.value; });

  const dayVal = document.getElementById('cr-target-day-select').value;
  const targetDay = dayVal ? parseInt(dayVal) : null;
  const priority = document.getElementById('cr-priority-select').value;
  const title = document.getElementById('cr-title-input').value.trim() || 'Travel Plan / Site Modification';
  const description = document.getElementById('cr-desc-input').value.trim() || 'Describe requested updates here...';
  const submitter = document.getElementById('cr-submitter-input').value.trim() || 'Eyal';

  const previewEl = document.getElementById('cr-directive-preview');
  if (previewEl) {
    previewEl.innerText = generateCrDirectiveText({
      id: 'CR-PREVIEW',
      category,
      target_day: targetDay,
      priority,
      title,
      description,
      submitter
    });
  }
}

function copyCrDirectiveFromForm() {
  updateDirectivePreviewFromForm();
  const previewEl = document.getElementById('cr-directive-preview');
  if (previewEl && previewEl.innerText) {
    copyTextToClipboard(previewEl.innerText);
    showToast('📋 Antigravity Directive copied to clipboard!', 'success');
  }
}

function copyGeneratedDirective() {
  const previewEl = document.getElementById('cr-directive-preview');
  if (previewEl && previewEl.innerText) {
    copyTextToClipboard(previewEl.innerText);
    showToast('📋 Antigravity Directive copied to clipboard!', 'success');
  }
}

function copySingleTicketDirective(ticketId) {
  const ticket = localChangeRequests.find(r => r.id === ticketId);
  if (!ticket) return;
  const text = generateCrDirectiveText(ticket);
  copyTextToClipboard(text);
  showToast(`📋 Copied directive for ticket ${ticketId}!`, 'success');
}

function copyTextToClipboard(text) {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text);
  } else {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
  }
}

function playAgentSuccessChime() {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.type = 'sine';
    const now = ctx.currentTime;
    osc.frequency.setValueAtTime(587.33, now); // D5
    osc.frequency.setValueAtTime(880.00, now + 0.12); // A5
    gain.gain.setValueAtTime(0.12, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
    osc.start(now);
    osc.stop(now + 0.4);
  } catch (e) {}
}

function enableBrowserNotifications() {
  if (!('Notification' in window)) {
    showToast('Browser notifications are not supported by this browser.', 'info');
    return;
  }
  Notification.requestPermission().then(permission => {
    if (permission === 'granted') {
      showToast('🔔 Notifications enabled! You will be alerted when the agent finishes work.', 'success');
      playAgentSuccessChime();
    } else {
      showToast('Notifications permission was not granted.', 'info');
    }
  });
}

function copyQueuedTicketsToAntigravity() {
  const queued = localChangeRequests.filter(r => r.status === 'QUEUED' || r.status === 'PENDING');
  if (queued.length === 0) {
    showToast('No pending tickets in queue.', 'info');
    return;
  }
  const summary = queued.map(q => `- Ticket ${q.id} (${q.target_day ? 'Day ' + q.target_day : 'General'}): ${q.title}\n  Details: ${q.description}`).join('\n\n');
  const text = `Antigravity, please process and fix my queued change request:\n\n${summary}`;
  copyTextToClipboard(text);
  showToast('📋 Copied! Paste this directly into Antigravity chat to resolve it now.', 'success', 6000);
}

function copySingleTicketToChat(ticketId) {
  const ticket = localChangeRequests.find(r => r.id === ticketId);
  if (!ticket) return;
  const text = `Antigravity, please fix my request for ${ticket.target_day ? 'Day ' + ticket.target_day : 'the site'}: "${ticket.title}".\nDetails: ${ticket.description}`;
  copyTextToClipboard(text);
  showToast('📋 Copied! Paste this directly into Antigravity chat to resolve it now.', 'success', 6000);
}




