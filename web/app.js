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
// PHASE & STATUS FILTERING
// -------------------------------------------------------------
function setPhase(phase) {
  currentPhase = phase;
  document.querySelectorAll('.tab-phase').forEach(btn => {
    if (btn.dataset.phase === phase) {
      btn.classList.add('border-blue-500', 'text-blue-400');
      btn.classList.remove('border-transparent', 'text-slate-400');
    } else {
      btn.classList.remove('border-blue-500', 'text-blue-400');
      btn.classList.add('border-transparent', 'text-slate-400');
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
      : 'px-2.5 py-1 rounded-lg text-xs bg-slate-800 text-slate-300 hover:bg-slate-700 transition';
    confBtn.className = status === 'confirmed' 
      ? 'px-2.5 py-1 rounded-lg text-xs bg-emerald-600 text-white font-semibold shadow-sm transition' 
      : 'px-2.5 py-1 rounded-lg text-xs bg-slate-800 text-emerald-400 hover:bg-emerald-950/60 transition border border-transparent hover:border-emerald-500/30';
    vetBtn.className = status === 'vetted' 
      ? 'px-2.5 py-1 rounded-lg text-xs bg-amber-600 text-white font-semibold shadow-sm transition' 
      : 'px-2.5 py-1 rounded-lg text-xs bg-slate-800 text-amber-400 hover:bg-amber-950/60 transition border border-transparent hover:border-amber-500/30';
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

function toggleAllDays(expand) {
  document.querySelectorAll('.day-content-block').forEach(el => {
    if (expand) el.classList.remove('hidden');
    else el.classList.add('hidden');
  });
  document.querySelectorAll('.day-toggle-icon').forEach(icon => {
    if (expand) icon.classList.add('rotate-180');
    else icon.classList.remove('rotate-180');
  });
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

          <!-- Taxi / Grab Driver Assist Box -->
          ${grab.dropoff || dropLocal ? `
            <div class="driver-assist-box p-3.5 sm:p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
              <div class="min-w-0 flex-1">
                <div class="text-[11px] font-bold uppercase tracking-wider text-amber-800 dark:text-amber-300 mb-0.5 flex items-center gap-1">
                  <span>🚕</span> Show Driver Destination (Grab / Taxi):
                </div>
                <div class="text-slate-900 dark:text-white font-bold text-sm truncate">${grab.dropoff || ''}</div>
                ${dropLocal ? `<div class="driver-native-text mt-0.5 select-all">${dropLocal}</div>` : ''}
              </div>
              <div class="flex flex-col sm:flex-row gap-2 w-full sm:w-auto shrink-0 mt-2 sm:mt-0">
                ${dropLocal ? `
                  <button onclick="copyToClipboard('${escapedLocal}', 'Copied destination in local script for driver!')" class="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-sm transition active:scale-95">
                    <span>📋</span> Copy Driver Script
                  </button>
                ` : ''}
                ${grab.maps_url ? `
                  <a href="${grab.maps_url}" target="_blank" class="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-sm transition">
                    <span>📍</span> Open Maps ↗
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

        <!-- Curated Daily Flow (Curated 3-Node Journey Grid) -->
        <div>
          <div class="font-bold text-slate-900 dark:text-white text-xs sm:text-sm mb-2.5 flex items-center justify-between">
            <span class="flex items-center gap-1.5">🗺️ Curated Daily Flow (Geographically Sequenced)</span>
            <span class="text-xs text-slate-500 dark:text-slate-400 font-mono">Paced &amp; Route-Optimized</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div class="flow-node-morning p-4 rounded-2xl text-xs sm:text-sm shadow-sm">
              <div class="flex items-center gap-1.5 font-extrabold text-amber-900 dark:text-amber-300 mb-1.5">
                <span>🌅</span> Morning Focus
              </div>
              <p class="text-slate-800 dark:text-slate-200 leading-relaxed">${day.curated_daily_flow.morning || 'Flexible exploration'}</p>
            </div>
            <div class="flow-node-afternoon p-4 rounded-2xl text-xs sm:text-sm shadow-sm">
              <div class="flex items-center gap-1.5 font-extrabold text-blue-900 dark:text-sky-300 mb-1.5">
                <span>☀️</span> Afternoon Highlight
              </div>
              <p class="text-slate-800 dark:text-slate-200 leading-relaxed">${day.curated_daily_flow.afternoon || 'Activity & transit'}</p>
            </div>
            <div class="flow-node-evening p-4 rounded-2xl text-xs sm:text-sm shadow-sm">
              <div class="flex items-center gap-1.5 font-extrabold text-purple-900 dark:text-purple-300 mb-1.5">
                <span>🌙</span> Evening Pacing
              </div>
              <p class="text-slate-800 dark:text-slate-200 leading-relaxed">${day.curated_daily_flow.evening || 'Dinner & unwind'}</p>
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

    // Smooth scroll to card (offset for sticky header + scrubber ~ 140px)
    const yOffset = window.innerWidth < 640 ? -110 : -140;
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
  const scrollPos = window.scrollY + 200;

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

