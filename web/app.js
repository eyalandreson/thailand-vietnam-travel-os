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
  const partial = days.filter(d => d.status.includes('BOOKED') && !d.status.includes('CONFIRMED - BOOKED')).length;
  const unbooked = days.length - (confirmed + partial);

  document.getElementById('metric-total-days').innerText = days.length;
  document.getElementById('metric-confirmed').innerText = confirmed + partial;
  document.getElementById('metric-vetted').innerText = unbooked;
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
    filtered = filtered.filter(d => d.status.includes('BOOKED'));
  } else if (currentFilter === 'vetted') {
    filtered = filtered.filter(d => !d.status.includes('CONFIRMED - BOOKED'));
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
    let badgeClass = 'badge-vetted';
    if (day.status.includes('CONFIRMED - BOOKED')) {
      badgeClass = 'badge-confirmed';
    } else if (day.status.includes('BOOKED')) {
      badgeClass = 'badge-radar';
    }

    const isPhase1 = day.phase.includes('Vietnam') || day.day_number <= 13;
    const phaseColor = isPhase1 ? 'text-amber-400 border-amber-500/30' : 'text-pink-400 border-pink-500/30';
    const bedIcon = isPhase1 ? '🛏️ Twin Beds (Guys Trip)' : '👑 Romantic King (Couple Trip)';

    let hotelsHtml = '';
    (day.accommodation_matrix || []).forEach(h => {
      const isHotelBooked = h.status === 'CONFIRMED_BOOKED';
      const hotelBadge = isHotelBooked 
        ? `<span class="text-xs px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-300 font-bold border border-emerald-500/40">✓ CONFIRMED BOOKING</span>`
        : `<span class="text-xs px-2 py-0.5 rounded bg-amber-950/80 text-amber-300 font-semibold border border-amber-500/40">UNBOOKED RECOMMENDATION</span>`;

      hotelsHtml += `
        <div class="bg-slate-900/60 rounded-xl p-3 border border-slate-700/60 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between flex-wrap gap-1">
              <a href="${h.booking_url}" target="_blank" class="font-semibold text-blue-400 hover:underline text-sm flex items-center gap-1">
                ${h.hotel_name} <span class="text-xs">↗</span>
              </a>
              ${hotelBadge}
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
      const isVerified = Boolean(doc.file_path);
      docsHtml += `
        <button onclick="openDocModal('${doc.doc_id}')" class="doc-pill text-xs px-2.5 py-1.5 rounded-lg flex items-center gap-1.5 cursor-pointer ${isVerified ? 'bg-emerald-950/40 border-emerald-600/50 hover:border-emerald-400' : 'bg-slate-800/80 border-slate-700 hover:border-blue-400'} border transition">
          <span>${isVerified ? '📄' : '📎'}</span>
          <span class="font-medium text-slate-200">${doc.title}</span>
          <span class="text-blue-300 text-[11px] font-mono">(${doc.ref})</span>
          ${isVerified 
            ? `<span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-900/60 text-emerald-300 border border-emerald-500/50 font-semibold">✓ Download PDF</span>` 
            : `<span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-900/40 text-amber-300 border border-amber-600/40">File Pending</span>`}
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
