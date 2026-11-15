/**
 * ORBITAL PULSE - Mission Control Client Application
 * Master orchestrator connecting WebSockets, Three.js 3D stage, radar, audio, and UI.
 */

class OrbitalPulseApp {
  constructor() {
    this.ws = null;
    this.playerId = 'player_' + Math.floor(Math.random() * 8999 + 1000);
    this.playerName = 'Commander';
    this.roomCode = null;
    this.mode = '1P';
    this.level = 1;
    this.state = null;
    this.activeStation = 'station_1';

    // Submodules
    this.scene3d = null;
    this.radar = null;
    this.urspace = null;

    // Puzzle State
    this.puzzlesCatalog = [];
    this.currentPuzzle = null;
    this.puzzleTimerInterval = null;
    this.puzzleTimeRemaining = 90;

    this.init();
  }

  async init() {
    // Initialize 3D Scene and Radar
    this.scene3d = new SpacecraftScene3D('canvas-container');
    this.radar = new TradeOffRadar('radar-svg-container');
    this.urspace = new UrspaceGuideController(this);

    // Fetch puzzles
    try {
      const pRes = await fetch('/api/puzzles');
      this.puzzlesCatalog = await pRes.json();
    } catch (e) {
      console.warn("Failed fetching puzzles", e);
    }

    this.bindDOMEvents();

    // Check URL parameters for direct room joining (?room=ABCD)
    const urlParams = new URLSearchParams(window.location.search);
    const roomParam = urlParams.get('room');
    if (roomParam) {
      document.getElementById('join-room-code').value = roomParam.toUpperCase();
      this.openModal('join-room-modal');
    } else {
      this.openModal('welcome-modal');
    }
  }

  bindDOMEvents() {
    // Welcome Modal buttons
    document.getElementById('btn-create-game').addEventListener('click', () => {
      this.closeModal('welcome-modal');
      this.openModal('create-game-modal');
    });

    document.getElementById('btn-join-game').addEventListener('click', () => {
      this.closeModal('welcome-modal');
      this.openModal('join-room-modal');
    });

    document.getElementById('btn-start-created-room').addEventListener('click', () => {
      this.handleCreateRoomSubmit();
    });

    document.getElementById('btn-submit-join').addEventListener('click', () => {
      this.handleJoinRoomSubmit();
    });

    // Top Bar Action Buttons
    document.getElementById('btn-spend-hint').addEventListener('click', () => {
      this.sendAction('use_hint');
      missionAudio.playTelemetryChime();
    });

    document.getElementById('btn-open-refill').addEventListener('click', () => {
      this.openAstroCalculusTerminal();
    });

    document.getElementById('btn-open-urspace').addEventListener('click', () => {
      // Default to first scenario tutorial
      const tuts = this.state?.scenario?.urspace_tutorials || ['tut_cubesat_sso'];
      this.urspace.openTutorial(tuts[0]);
    });

    // Station tab selectors
    ['station_1', 'station_2', 'station_3', 'station_4'].forEach(st => {
      const el = document.getElementById(`tab-${st}`);
      if (el) {
        el.addEventListener('click', () => {
          this.switchStationTab(st);
          missionAudio.playSelect();
        });
      }
    });

    // Launch / Simulate Mission Button
    document.getElementById('btn-main-action').addEventListener('click', () => {
      if (this.state?.status === 'designing' || this.state?.status === 'lobby') {
        this.sendAction('start_simulation');
        missionAudio.playThruster();
      } else if (this.state?.status === 'simulating') {
        this.sendAction('finish_mission');
        missionAudio.playSuccess();
      }
    });

    // Chat / Radio input
    document.getElementById('chat-form').addEventListener('submit', (e) => {
      e.preventDefault();
      const input = document.getElementById('chat-input');
      const text = input.value.trim();
      if (text) {
        this.sendAction('send_chat', { message: text });
        input.value = '';
      }
    });

    // View toggles on 3D canvas
    document.getElementById('btn-view-spacecraft').addEventListener('click', () => {
      this.scene3d.switchToSpacecraftView();
      missionAudio.playSelect();
    });

    document.getElementById('btn-view-orbit').addEventListener('click', () => {
      this.scene3d.switchToOrbitView(this.level);
      missionAudio.playSelect();
    });

    // Modals close buttons
    document.querySelectorAll('.btn-close-modal').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const modal = e.target.closest('.modal-overlay');
        if (modal) modal.classList.remove('active');
      });
    });

    // Puzzle Terminal events
    document.getElementById('btn-submit-puzzle').addEventListener('click', () => {
      this.submitPuzzleAnswer();
    });

    document.getElementById('btn-toggle-puzzle-hint').addEventListener('click', () => {
      const hintEl = document.getElementById('puzzle-hint-text');
      hintEl.style.display = hintEl.style.display === 'none' ? 'block' : 'none';
      missionAudio.playBlip(600, 0.05);
    });

    // Forensic Debrief Iterate Button
    document.getElementById('btn-debrief-retry').addEventListener('click', () => {
      this.closeModal('debrief-modal');
      this.sendAction('start_mission');
    });

    document.getElementById('btn-debrief-next-level').addEventListener('click', () => {
      this.closeModal('debrief-modal');
      window.location.reload();
    });
  }

  async handleCreateRoomSubmit() {
    const name = document.getElementById('create-player-name').value.trim() || 'Commander';
    const mode = document.getElementById('create-mode-select').value;
    const level = parseInt(document.getElementById('create-level-select').value, 10);
    const prefCode = document.getElementById('create-pref-code').value.trim().toUpperCase();

    this.playerName = name;
    this.mode = mode;
    this.level = level;

    try {
      const res = await fetch('/api/rooms/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ host_name: name, mode, level, preferred_code: prefCode })
      });
      const data = await res.json();
      if (data.success) {
        this.roomCode = data.room_code;
        this.closeModal('create-game-modal');
        this.connectWebSocket();
      }
    } catch (err) {
      alert("Error creating room: " + err);
    }
  }

  handleJoinRoomSubmit() {
    const name = document.getElementById('join-player-name').value.trim() || 'Specialist';
    const code = document.getElementById('join-room-code').value.trim().toUpperCase();

    if (!code) {
      alert("Please enter a 4-digit room code.");
      return;
    }

    this.playerName = name;
    this.roomCode = code;
    this.closeModal('join-room-modal');
    this.connectWebSocket();
  }

  connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/${this.roomCode}/${this.playerId}/${encodeURIComponent(this.playerName)}`;

    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      missionAudio.playTelemetryChime();
      document.getElementById('display-room-code').textContent = this.roomCode;
      this.sendAction('start_mission');
    };

    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === 'state_update') {
        this.onStateUpdate(msg.payload);
      } else if (msg.type === 'puzzle_result') {
        this.onPuzzleResult(msg.payload);
      } else if (msg.type === 'mission_debrief') {
        this.onMissionDebrief(msg.payload);
      }
    };

    this.ws.onerror = (err) => console.error("WS error", err);
    this.ws.onclose = () => console.log("WS closed");
  }

  sendAction(action, payload = {}) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ action, payload }));
    }
  }

  onStateUpdate(state) {
    this.state = state;
    this.level = state.level;
    this.mode = state.mode;

    // Update Top Bar
    document.getElementById('display-mission-name').textContent = state.scenario.name;
    document.getElementById('display-cml-badge').textContent = state.scenario.cml;

    // Timer display
    const elapsed = Math.floor(state.elapsed_seconds);
    const target = state.target_seconds;
    const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
    const secs = String(elapsed % 60).padStart(2, '0');
    document.getElementById('display-clock-val').textContent = `${mins}:${secs}`;
    document.getElementById('display-clock-target').textContent = `/ ${Math.floor(target / 60)}:00`;

    // Freeze status indicator
    const freezeIndicator = document.getElementById('display-freeze-indicator');
    if (state.is_frozen) {
      freezeIndicator.style.display = 'inline-flex';
      freezeIndicator.textContent = `❄️ CLOCK FROZEN (${state.freeze_remaining}s)`;
    } else {
      freezeIndicator.style.display = 'none';
    }

    // 5-Hint stars
    const hintCountEl = document.getElementById('display-hint-count');
    hintCountEl.textContent = `${state.unused_hints}/5`;

    // XP
    document.getElementById('display-mastery-xp').textContent = `${state.mastery_xp} XP`;

    // Update Selected Components in 3D Scene
    this.scene3d.updateModularComponents(state.selected_components, state.level);

    // Update 6-Axis Radar
    if (state.systems && state.systems.radar_metrics) {
      this.radar.render(state.systems.radar_metrics);
    }

    // Update Vital Neon Meters
    this.updateVitalGauges(state.systems);

    // Update Station Cards & Selection
    this.renderStationSelector(state);

    // Update Character Conversation Hub
    this.renderDialogueHub(state);

    // Crisis Event Popup Check
    if (state.active_crisis) {
      this.openCrisisModal(state.active_crisis);
    } else {
      this.closeModal('crisis-modal');
    }

    // Update Main Action button text
    const actionBtn = document.getElementById('btn-main-action');
    if (state.status === 'designing' || state.status === 'lobby') {
      actionBtn.textContent = '🚀 Simulate Orbit';
      actionBtn.style.background = 'linear-gradient(135deg, #0284c7, #00f0ff)';
    } else if (state.status === 'simulating') {
      actionBtn.textContent = '📊 Debrief Report';
      actionBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
      this.scene3d.switchToOrbitView(state.level);
    }
  }

  updateVitalGauges(systems) {
    if (!systems) return;

    // Mass meter
    const massPct = Math.min(100, (systems.total_mass_kg / systems.max_mass_kg) * 100);
    this.setMeter('meter-mass', massPct, `${systems.total_mass_kg} / ${systems.max_mass_kg} kg`, !systems.mass_pass);

    // Power / Battery DoD meter
    const dodPct = Math.min(100, systems.battery_dod_percent);
    this.setMeter('meter-power', dodPct, `DoD: ${systems.battery_dod_percent}% (Max ${systems.battery_max_dod_percent}%)`, !systems.power_pass);

    // Budget meter
    const costPct = Math.min(100, (systems.total_cost_m / systems.budget_cap_m) * 100);
    this.setMeter('meter-budget', costPct, `$${systems.total_cost_m}M / $${systems.budget_cap_m}M`, !systems.budget_pass);

    // Data Link
    const dataPct = Math.min(100, systems.downlink_rate_mbps > 0 ? (systems.daily_downlink_cap_gb / Math.max(0.1, systems.daily_data_gen_gb)) * 100 : 0);
    this.setMeter('meter-data', dataPct, `${systems.daily_downlink_cap_gb} / ${systems.daily_data_gen_gb} GB/day`, !systems.data_pass);

    // Thermal / Cryo
    const thermText = systems.cooling_capability_k < 100 ? `${systems.cooling_capability_k} K` : 'Nominal';
    this.setMeter('meter-thermal', systems.thermal_pass ? 90 : 20, thermText, !systems.thermal_pass);

    // Science / Bio Vitals
    const bioText = `Sci: ${systems.science_yield_pts} | Bio: ${systems.bio_health_pts}%`;
    this.setMeter('meter-bio', systems.bio_health_pts, bioText, false);

    // Bottleneck Warnings banner
    const alertBox = document.getElementById('systems-alert-box');
    if (systems.bottlenecks && systems.bottlenecks.length > 0) {
      alertBox.style.display = 'block';
      alertBox.innerHTML = `⚠️ <strong>${systems.bottlenecks[0].subsystem}:</strong> ${systems.bottlenecks[0].issue}`;
    } else {
      alertBox.style.display = 'none';
    }
  }

  setMeter(id, percentage, readoutText, isError = false) {
    const fillEl = document.getElementById(`${id}-fill`);
    const valEl = document.getElementById(`${id}-val`);
    if (fillEl && valEl) {
      fillEl.style.width = `${Math.max(5, Math.min(100, percentage))}%`;
      fillEl.className = 'meter-fill ' + (isError ? 'critical' : (percentage > 85 ? 'warning' : 'normal'));
      valEl.textContent = readoutText;
    }
  }

  renderStationSelector(state) {
    const listContainer = document.getElementById('station-components-list');
    const station = this.activeStation;
    const comps = state.available_components[station] || [];
    const currentSelected = state.selected_components[station];

    // Highlight active station tab
    ['station_1', 'station_2', 'station_3', 'station_4'].forEach(st => {
      const tabEl = document.getElementById(`tab-${st}`);
      if (tabEl) {
        tabEl.classList.toggle('active', st === station);
        const previewEl = document.getElementById(`preview-${st}`);
        if (previewEl) {
          previewEl.textContent = state.selected_components[st]?.name || 'Not equipped';
        }
      }
    });

    // Check if player owns this station
    const isOwner = (state.station_owners[station] === this.playerId) || (state.mode === '1P');
    const ownerName = state.players[state.station_owners[station]]?.name || 'Unassigned';

    let html = `
      <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:10px; display:flex; justify-content:space-between;">
        <span>Assigned: <strong style="color:var(--accent-cyan);">${isOwner ? 'You (' + this.playerName + ')' : ownerName}</strong></span>
        <span>${isOwner ? '⚡ Active Controls' : '🔒 Read-Only'}</span>
      </div>
    `;

    comps.forEach(comp => {
      // Filter by level
      if (comp.levels && !comp.levels.includes(state.level)) return;

      const isEquipped = currentSelected?.id === comp.id;
      html += `
        <div class="component-option-item ${isEquipped ? 'selected' : ''}" data-comp-id="${comp.id}" style="${!isOwner ? 'opacity:0.7;' : ''}">
          <div class="comp-opt-header">
            <span style="color:${isEquipped ? 'var(--accent-emerald)' : 'var(--text-main)'}">${comp.name}</span>
            <span style="color:var(--accent-gold); font-family:var(--font-mono);">$${comp.cost_m}M</span>
          </div>
          <div class="comp-opt-meta">
            <span>Mass: ${comp.mass_kg} kg</span>
            ${comp.power_gen_w ? `<span style="color:#38bdf8;">+${comp.power_gen_w}W Gen</span>` : ''}
            ${comp.power_draw_w || comp.power_draw_day_w ? `<span style="color:#fb7185;">-${comp.power_draw_w || comp.power_draw_day_w}W</span>` : ''}
            ${comp.downlink_rate_mbps ? `<span style="color:#a855f7;">${comp.downlink_rate_mbps} Mbps</span>` : ''}
            ${comp.science_pts ? `<span style="color:#10b981;">+${comp.science_pts} Sci</span>` : ''}
          </div>
          <div class="comp-opt-desc">${comp.description}</div>
        </div>
      `;
    });

    listContainer.innerHTML = html;

    // Attach click handlers to components
    if (isOwner) {
      listContainer.querySelectorAll('.component-option-item').forEach(el => {
        el.addEventListener('click', () => {
          const cid = el.getAttribute('data-comp-id');
          this.sendAction('select_component', { station: this.activeStation, component_id: cid });
          missionAudio.playSelect();
        });
      });
    }
  }

  switchStationTab(station) {
    this.activeStation = station;
    if (this.state) {
      this.renderStationSelector(this.state);
    }
  }

  renderDialogueHub(state) {
    if (!state.dialogue_log || state.dialogue_log.length === 0) return;

    const latest = state.dialogue_log[state.dialogue_log.length - 1];

    document.getElementById('dock-char-avatar').textContent = latest.speaker_avatar || '👩‍🚀';
    document.getElementById('dock-char-name').textContent = latest.speaker_name;
    document.getElementById('dock-char-title').textContent = latest.speaker_title;

    const bubbleEl = document.getElementById('dock-dialogue-text');
    bubbleEl.textContent = latest.message;
    if (latest.is_shout) {
      bubbleEl.className = 'dialogue-bubble-text shout-message';
      missionAudio.playAlarm();
    } else {
      bubbleEl.className = 'dialogue-bubble-text';
    }
  }

  openAstroCalculusTerminal() {
    if (this.puzzlesCatalog.length === 0) return;

    // Pick random or sequential puzzle
    const puzzle = this.puzzlesCatalog[Math.floor(Math.random() * this.puzzlesCatalog.length)];
    this.currentPuzzle = puzzle;

    document.getElementById('puzzle-title').textContent = puzzle.title;
    document.getElementById('puzzle-concept').textContent = puzzle.concept;
    document.getElementById('puzzle-question').textContent = puzzle.question;
    document.getElementById('puzzle-formula').textContent = puzzle.formula;
    document.getElementById('puzzle-unit-badge').textContent = puzzle.unit;
    document.getElementById('puzzle-hint-text').textContent = puzzle.hint;
    document.getElementById('puzzle-hint-text').style.display = 'none';
    document.getElementById('puzzle-answer-input').value = '';
    document.getElementById('puzzle-feedback-box').innerHTML = '';

    // Start 90s puzzle timer
    this.puzzleTimeRemaining = 90;
    clearInterval(this.puzzleTimerInterval);
    const timerEl = document.getElementById('puzzle-clock');
    this.puzzleTimerInterval = setInterval(() => {
      this.puzzleTimeRemaining--;
      timerEl.textContent = `${this.puzzleTimeRemaining}s`;
      if (this.puzzleTimeRemaining <= 0) {
        clearInterval(this.puzzleTimerInterval);
        this.closeModal('astro-calculus-modal');
      }
    }, 1000);

    missionAudio.playTelemetryChime();
    this.openModal('astro-calculus-modal');
  }

  submitPuzzleAnswer() {
    const val = parseFloat(document.getElementById('puzzle-answer-input').value);
    if (isNaN(val)) return;

    this.sendAction('solve_puzzle', {
      puzzle_id: this.currentPuzzle.id,
      answer: val
    });
  }

  onPuzzleResult(result) {
    const fb = document.getElementById('puzzle-feedback-box');
    if (result.is_correct) {
      clearInterval(this.puzzleTimerInterval);
      fb.innerHTML = `
        <div style="background:rgba(16, 185, 129, 0.2); border:1px solid #10b981; color:#a7f3d0; padding:12px; border-radius:8px;">
          <strong>✓ CORRECT! +1 Hint Refilled & +75 Bonus Pts!</strong><br>
          <span style="font-size:0.85rem;">${result.step_solution}</span>
        </div>
      `;
      missionAudio.playSuccess();
      setTimeout(() => this.closeModal('astro-calculus-modal'), 2200);
    } else {
      fb.innerHTML = `
        <div style="background:rgba(244, 63, 94, 0.2); border:1px solid #f43f5e; color:#fecdd3; padding:10px; border-radius:8px;">
          ✗ Incorrect answer. Check your derivatives or integration limits and try again!
        </div>
      `;
      missionAudio.playAlarm();
    }
  }

  openCrisisModal(crisis) {
    const modal = document.getElementById('crisis-modal');
    document.getElementById('crisis-title').textContent = crisis.title;
    document.getElementById('crisis-narrative').textContent = crisis.narrative;

    const optContainer = document.getElementById('crisis-options-list');
    let html = '';
    crisis.options.forEach(opt => {
      const isVoted = this.state.crisis_votes?.[this.playerId] === opt.id;
      html += `
        <div class="crisis-opt-card ${isVoted ? 'voted' : ''}" data-opt-id="${opt.id}">
          <div style="font-weight:700; color:${isVoted ? 'var(--accent-emerald)' : 'var(--text-main)'}; font-size:0.95rem;">
            ${isVoted ? '✓ ' : ''}${opt.label}
          </div>
        </div>
      `;
    });
    optContainer.innerHTML = html;

    optContainer.querySelectorAll('.crisis-opt-card').forEach(el => {
      el.addEventListener('click', () => {
        const oid = el.getAttribute('data-opt-id');
        this.sendAction('cast_crisis_vote', { option_id: oid });
        missionAudio.playSelect();
      });
    });

    this.openModal('crisis-modal');
  }

  onMissionDebrief(data) {
    const score = data.score;
    const systems = data.systems;
    const scenario = data.scenario;
    const nasaMatch = data.nasa_mission_match;

    document.getElementById('debrief-final-score').textContent = score.final_score;
    document.getElementById('debrief-rank-title').textContent = score.rank;
    document.getElementById('debrief-cml-cert').textContent = score.cml_cert;

    // Score equation breakdown matching Section 5.3
    document.getElementById('debrief-formula-breakdown').innerHTML = `
      <div style="font-family:var(--font-mono); font-size:0.8rem; line-height:1.6; color:#94a3b8;">
        <div>Base Engineering Score (S_eng): <strong style="color:var(--text-main);">${score.base_engineering_score} / 1000</strong></div>
        <div>Time Multiplier: <strong style="color:var(--accent-cyan);">${score.time_multiplier}x</strong> (Player Bonus: +${score.player_speed_bonus_pct}%, Team Bonus: +${score.team_speed_bonus_pct}%)</div>
        <div>Diagnostic Hints Left: <strong style="color:var(--accent-gold);">${score.unused_hints}</strong> (+${score.hint_bonus} pts)</div>
        <div>Calculus Puzzles Solved: <strong style="color:var(--accent-purple);">${score.solved_puzzles}</strong> (+${score.puzzle_bonus} pts)</div>
        <div>Survival Multiplier: <strong style="color:${score.survival ? 'var(--accent-emerald)' : 'var(--accent-rose)'};">${score.survival_mult}x</strong></div>
      </div>
    `;

    // Root-Cause Forensic Report
    const forensicEl = document.getElementById('debrief-forensic-report');
    if (score.survival) {
      forensicEl.innerHTML = `
        <div style="background:rgba(16, 185, 129, 0.15); border:1px solid #10b981; padding:12px; border-radius:8px;">
          <strong style="color:var(--accent-emerald);">MISSION SUCCESS & FLIGHT CERTIFIED</strong><br>
          <span style="font-size:0.85rem; color:#d1fae5;">
            All system-level trade-offs (mass, power balance, thermal cooling, data link, and crew physiology) were verified within nominal tolerances.
          </span>
        </div>
      `;
    } else {
      let issues = systems.bottlenecks.map(b => `• [${b.subsystem}]: ${b.issue}`).join('<br>');
      forensicEl.innerHTML = `
        <div style="background:rgba(244, 63, 94, 0.15); border:1px solid #f43f5e; padding:12px; border-radius:8px;">
          <strong style="color:var(--accent-rose);">CATASTROPHIC SYSTEMS FAILURE DETECTED</strong><br>
          <span style="font-size:0.85rem; color:#fecdd3;">${issues}</span>
        </div>
      `;
    }

    // NASA Mission Match Card
    if (nasaMatch) {
      document.getElementById('debrief-nasa-match').innerHTML = `
        <div class="nasa-match-card">
          <div style="font-size:0.75rem; text-transform:uppercase; color:#38bdf8; font-weight:700;">Real NASA Mission Match</div>
          <div style="font-weight:700; font-size:1.05rem; margin-top:2px;">${nasaMatch.missions.join(' & ')}</div>
          <p style="font-size:0.82rem; color:#cbd5e1; margin-top:6px; line-height:1.4;">${nasaMatch.real_world_context}</p>
        </div>
      `;
    }

    this.openModal('debrief-modal');
  }

  openModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.add('active');
  }

  closeModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.remove('active');
  }
}

// Instantiate on window load
window.addEventListener('DOMContentLoaded', () => {
  window.app = new OrbitalPulseApp();
});
