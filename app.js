/**
 * Live Travel OS Reactive Controller
 * Handles dual-view switching (App View <-> Google Doc View),
 * phase filtering, search, day accordions, document preview modals,
 * and price radar alerts.
 */

let currentPhase = 'all';
let currentFilter = 'all';
let searchQuery = '';
let currentView = 'app';
let itineraryData = null;

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

function initApp() {
  renderHeaderMetrics();
  renderDays();
  setupEventListeners();
}

function renderHeaderMetrics() {
  if (!itineraryData) return;
  const days = itineraryData.days || [];
  const confirmed = days.filter(d => d.status.includes('CONFIRMED')).length;
  const vetted = days.length - confirmed;

  document.getElementById('metric-total-days').innerText = days.length;
  document.getElementById('metric-confirmed').innerText = confirmed;
  document.getElementById('metric-vetted').innerText = vetted;
}

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
  renderDays();
}

function toggleDay(dayNum) {
  const content = document.getElementById(`day-content-${dayNum}`);
  const icon = document.getElementById(`day-icon-${dayNum}`);
  if (content.classList.contains('hidden')) {
    content.classList.remove('hidden');
    icon.classList.add('rotate-180');
  } else {
    content.classList.add('hidden');
    icon.classList.remove('rotate-180');
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
    filtered = filtered.filter(d => d.status.includes('CONFIRMED'));
  } else if (currentFilter === 'vetted') {
    filtered = filtered.filter(d => d.status.includes('VETTED'));
  }

  // Filter by Search Query
  if (searchQuery.trim() !== '') {
    const q = searchQuery.toLowerCase();
    filtered = filtered.filter(d => {
      const matchDest = d.destination.toLowerCase().includes(q);
      const matchFlow = JSON.stringify(d.curated_daily_flow || {}).toLowerCase().includes(q);
      const matchHotels = JSON.stringify(d.accommodation_matrix || []).toLowerCase().includes(q);
      const matchDocs = JSON.stringify(d.attached_documents || []).toLowerCase().includes(q);
      return matchDest || matchFlow || matchHotels || matchDocs;
    });
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="glass-card rounded-2xl p-8 text-center text-slate-400">
        <p class="text-lg">No itinerary days match your current filter.</p>
        <button onclick="resetFilters()" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">Reset Filters</button>
      </div>
    `;
    return;
  }

  filtered.forEach(day => {
    const isConfirmed = day.status.includes('CONFIRMED');
    const badgeClass = isConfirmed ? 'badge-confirmed' : 'badge-vetted';
    const isPhase1 = day.phase.includes('Vietnam') || day.day_number <= 13;
    const phaseColor = isPhase1 ? 'text-amber-400 border-amber-500/30' : 'text-pink-400 border-pink-500/30';
    const bedIcon = isPhase1 ? '🛏️ Twin Beds (Guys Trip)' : '👑 Romantic King (Couple Trip)';

    let hotelsHtml = '';
    (day.accommodation_matrix || []).forEach(h => {
      hotelsHtml += `
        <div class="bg-slate-900/60 rounded-xl p-3 border border-slate-700/60 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between">
              <a href="${h.booking_url}" target="_blank" class="font-semibold text-blue-400 hover:underline text-sm flex items-center gap-1">
                ${h.hotel_name} <span class="text-xs">↗</span>
              </a>
              <span class="text-xs px-2 py-0.5 rounded bg-blue-900/50 text-blue-300 font-bold">⭐ ${h.critic_score}/10</span>
            </div>
            <p class="text-xs text-slate-300 mt-1"><b>Room:</b> ${h.room_spec}</p>
            <p class="text-xs text-slate-400 mt-1 italic">${h.critic_notes}</p>
          </div>
          <div class="mt-3 pt-2 border-t border-slate-800 flex justify-between items-center text-xs">
            <span class="text-emerald-400 font-medium">${h.price_per_night}</span>
            <a href="${h.booking_url}" target="_blank" class="px-2.5 py-1 bg-blue-600/80 hover:bg-blue-600 text-white rounded text-xs transition">View Deal</a>
          </div>
        </div>
      `;
    });

    let docsHtml = '';
    (day.attached_documents || []).forEach(doc => {
      docsHtml += `
        <button onclick="openDocModal('${doc.doc_id}')" class="doc-pill text-xs px-2.5 py-1 rounded-lg flex items-center gap-1.5 cursor-pointer">
          <span>📎</span>
          <span class="font-medium text-slate-200">${doc.title}</span>
          <span class="text-slate-400 text-[11px]">(${doc.ref})</span>
        </button>
      `;
    });

    let mapsHtml = '';
    (day.google_maps_links || []).forEach(m => {
      mapsHtml += `
        <a href="${m.url}" target="_blank" class="inline-flex items-center gap-1 px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition">
          <span>📍</span> ${m.label} <span class="text-[10px] text-slate-400">↗</span>
        </a>
      `;
    });

    // Special banner for transition day or luggage drop
    let specialBanner = '';
    if (day.day_number === 2) {
      specialBanner = `
        <div class="bg-amber-950/40 border-l-4 border-amber-500 p-3 rounded-r-lg mb-3 text-xs text-amber-200 flex items-start gap-2">
          <span class="text-lg">🧳</span>
          <div>
            <b>BKK Airport Suitcase Drop (Floor B Basement):</b> Deposit checked suitcase at AIRPORTELs Suvarnabhumi basement before 11:55 flight. 55L clamshell backpack only for Vietnam!
          </div>
        </div>
      `;
    } else if (day.day_number === 14) {
      specialBanner = `
        <div class="bg-purple-950/40 border-l-4 border-purple-500 p-3 rounded-r-lg mb-3 text-xs text-purple-200 flex items-start gap-2">
          <span class="text-lg">✈️</span>
          <div>
            <b>Transition Hub:</b> Friend departs BKK. Retrieve checked suitcase at AIRPORTELs Floor B. Reunite with Girlfriend. Take direct flight BKK -> USM!
            <button onclick="openPriceRadarModal()" class="ml-2 underline text-blue-300 font-bold hover:text-white">View BKK->USM Price Radar</button>
          </div>
        </div>
      `;
    }

    const card = document.createElement('div');
    card.className = 'glass-card rounded-2xl overflow-hidden transition-all duration-200';
    card.innerHTML = `
      <!-- Card Header (Always Visible) -->
      <div onclick="toggleDay(${day.day_number})" class="p-4 sm:p-5 flex items-center justify-between cursor-pointer hover:bg-slate-800/40 select-none">
        <div class="flex items-center gap-3 sm:gap-4 flex-wrap sm:flex-nowrap">
          <div class="flex items-center justify-center w-10 h-10 rounded-xl bg-blue-600/20 text-blue-400 font-bold text-sm border border-blue-500/30 shrink-0">
            D${day.day_number}
          </div>
          <div>
            <div class="flex items-center gap-2 flex-wrap">
              <h3 class="font-bold text-base sm:text-lg text-white">${day.destination}</h3>
              <span class="text-xs px-2.5 py-0.5 rounded-full font-semibold ${badgeClass}">${day.status}</span>
              <span class="text-xs px-2 py-0.5 rounded-full border ${phaseColor} hidden sm:inline-block">${day.phase_short || day.phase}</span>
            </div>
            <div class="text-xs text-slate-400 mt-1 flex items-center gap-3 flex-wrap">
              <span>📅 ${day.day_of_week}, ${day.date}</span>
              <span>🌤️ ${day.weather_radar.temp_range}, ${day.weather_radar.condition}</span>
              <span class="text-slate-300 font-medium">${bedIcon}</span>
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
      <div id="day-content-${day.day_number}" class="day-content-block p-4 sm:p-6 border-t border-slate-700/60 bg-slate-900/40">
        ${specialBanner}

        <!-- Weather & Attire Radar -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4 text-xs">
          <div class="bg-slate-800/60 rounded-xl p-3 border border-slate-700/50">
            <div class="font-bold text-slate-300 mb-1 flex items-center gap-1.5">
              <span>🌦️</span> Weather & Attire Radar
            </div>
            <div class="text-slate-400">
              <b>Forecast:</b> ${day.weather_radar.temp_range} • Rain: ${day.weather_radar.precipitation_pct} • Humidity: ${day.weather_radar.humidity}<br>
              <span class="text-sky-300 font-medium">👔 Attire: ${day.weather_radar.attire_advice}</span>
            </div>
          </div>

          <div class="bg-slate-800/60 rounded-xl p-3 border border-slate-700/50">
            <div class="font-bold text-slate-300 mb-1 flex items-center gap-1.5">
              <span>🚗</span> Door-to-Door Logistics
            </div>
            <div class="text-slate-400">
              <span class="text-slate-200">${day.door_to_door_logistics.primary_transit}</span><br>
              <span class="text-slate-400 text-[11px]">Dep: ${day.door_to_door_logistics.departure_time} | Arr: ${day.door_to_door_logistics.arrival_time} | Buffer: ${day.door_to_door_logistics.buffer_time}</span>
            </div>
          </div>
        </div>

        <!-- Attached Documents (Requested by user) -->
        ${docsHtml ? `
          <div class="mb-4">
            <div class="text-xs font-bold text-slate-300 mb-1.5 flex items-center gap-1">
              <span>📎</span> Mail Vouchers & Attached Passes for this Day:
            </div>
            <div class="flex flex-wrap gap-2">
              ${docsHtml}
            </div>
          </div>
        ` : ''}

        <!-- Curated Daily Flow -->
        <div class="bg-slate-800/40 rounded-xl p-3.5 border border-slate-700/50 mb-4 text-xs">
          <div class="font-bold text-slate-200 mb-2 flex items-center gap-1.5">
            <span>🗺️</span> Curated Daily Flow (Geographically Sequenced)
          </div>
          <div class="space-y-1.5 text-slate-300">
            <p><span class="text-amber-300 font-semibold">🌅 Morning:</span> ${day.curated_daily_flow.morning}</p>
            <p><span class="text-sky-300 font-semibold">☀️ Afternoon:</span> ${day.curated_daily_flow.afternoon}</p>
            <p><span class="text-purple-300 font-semibold">🌙 Evening:</span> ${day.curated_daily_flow.evening}</p>
          </div>
        </div>

        <!-- Accommodation Matrix -->
        ${hotelsHtml ? `
          <div class="mb-4">
            <div class="text-xs font-bold text-slate-300 mb-2 flex items-center justify-between">
              <span class="flex items-center gap-1.5">🏨 Vetted Accommodations (Critic Passed $\\ge$ 8.5)</span>
              <span class="text-[11px] text-slate-400">${isPhase1 ? 'Enforced: Twin Beds' : 'Enforced: King / Ocean View'}</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              ${hotelsHtml}
            </div>
          </div>
        ` : ''}

        <!-- Essential Checklist & Google Maps -->
        <div class="pt-3 border-t border-slate-800 flex flex-col md:flex-row justify-between gap-3 text-xs text-slate-400">
          <div>
            <span class="font-bold text-slate-300">✓ Day Checklist:</span>
            <ul class="list-disc list-inside mt-1 space-y-0.5">
              ${(day.essential_checklist || []).map(c => `<li>${c}</li>`).join('')}
            </ul>
          </div>
          <div>
            <span class="font-bold text-slate-300">📍 Maps Navigation:</span>
            <div class="flex flex-wrap gap-1.5 mt-1">
              ${mapsHtml}
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
  document.getElementById('search-input').value = '';
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
}

// Modal Document Preview
function openDocModal(docId) {
  const registry = window.TRAVEL_OS_DATA?.confirmed_items || [];
  const item = registry.find(r => r.id === docId);
  const modal = document.getElementById('doc-modal');
  const title = document.getElementById('modal-doc-title');
  const body = document.getElementById('modal-doc-body');

  if (!item) {
    // Fallback search in days
    let found = null;
    (window.TRAVEL_OS_DATA?.days || []).forEach(d => {
      (d.attached_documents || []).forEach(doc => {
        if (doc.doc_id === docId) found = doc;
      });
    });
    if (found) {
      title.innerText = found.title;
      body.innerHTML = `
        <div class="p-4 bg-slate-900 rounded-xl border border-slate-700 text-sm">
          <p class="text-slate-300"><b>Document Reference:</b> ${found.ref}</p>
          <p class="text-slate-300"><b>Category:</b> ${found.category}</p>
          <p class="text-emerald-400 font-bold mt-2">Status: ${found.badge || 'CONFIRMED'}</p>
        </div>
      `;
      modal.classList.remove('hidden');
      return;
    }
  }

  title.innerText = item?.title || 'Travel Document Details';
  body.innerHTML = `
    <div class="space-y-3 text-sm">
      <div class="p-3 bg-blue-950/40 rounded-xl border border-blue-700/40">
        <span class="text-xs text-blue-300 uppercase tracking-wider font-bold">Verified Reference</span>
        <p class="text-lg font-mono text-white font-bold mt-0.5">${item?.reference_code || 'VERIFIED'}</p>
      </div>
      <div class="grid grid-cols-2 gap-2 text-xs">
        <div class="bg-slate-900 p-2.5 rounded-lg border border-slate-700/60">
          <span class="text-slate-400">Date:</span>
          <p class="font-semibold text-slate-200">${item?.date || 'Sep 2026'}</p>
        </div>
        <div class="bg-slate-900 p-2.5 rounded-lg border border-slate-700/60">
          <span class="text-slate-400">Category:</span>
          <p class="font-semibold text-slate-200">${item?.file_category || 'Travel Pass'}</p>
        </div>
      </div>
      <div class="bg-slate-900 p-3 rounded-lg border border-slate-700/60 text-xs text-slate-300">
        <p class="font-semibold text-slate-200 mb-1">Logistics & Instructions:</p>
        <p>${item?.details || 'Present digital or printed voucher at counter upon arrival.'}</p>
      </div>
      <div class="p-3 rounded-lg bg-emerald-950/30 border border-emerald-500/30 flex items-center justify-between text-xs">
        <span class="text-emerald-300 font-medium">Digital Pass File:</span>
        <span class="font-mono text-slate-300">${item?.file_name || 'pass.pdf'}</span>
      </div>
    </div>
  `;
  modal.classList.remove('hidden');
}

function closeDocModal() {
  document.getElementById('doc-modal').classList.add('hidden');
}

// BKK -> USM Price Radar Modal
function openPriceRadarModal() {
  const modal = document.getElementById('price-radar-modal');
  modal.classList.remove('hidden');
}

function closePriceRadarModal() {
  document.getElementById('price-radar-modal').classList.add('hidden');
}

// Luggage Locker Modal
function openLuggageModal() {
  const modal = document.getElementById('luggage-modal');
  modal.classList.remove('hidden');
}

function closeLuggageModal() {
  document.getElementById('luggage-modal').classList.add('hidden');
}
