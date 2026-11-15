/**
 * ORBITAL PULSE - Urspace Guide Controller
 * Section 3.4: Interactive Self-Tutorial System & Micro-Sliders
 */

class UrspaceGuideController {
  constructor(appRef) {
    this.app = appRef;
    this.modalEl = document.getElementById('urspace-modal');
    this.contentEl = document.getElementById('urspace-modal-body');
    this.catalog = {};
    this.currentTutId = null;
    this.init();
  }

  async init() {
    try {
      const res = await fetch('/api/tutorials');
      this.catalog = await res.json();
    } catch (e) {
      console.warn("Failed loading tutorials catalog", e);
    }
  }

  openTutorial(tutId) {
    const tut = this.catalog[tutId];
    if (!tut) return;

    this.currentTutId = tutId;

    // Send open_tutorial action to server (which triggers the 45s clock freeze)
    this.app.sendAction('open_tutorial', { tutorial_id: tutId });
    missionAudio.playTelemetryChime();

    // Render interactive slider HTML
    const slider = tut.slider_interactive;
    let sliderHtml = '';
    if (slider) {
      sliderHtml = `
        <div class="interactive-slider-box">
          <div style="display:flex; justify-content:space-between; font-size:0.85rem; font-weight:600;">
            <span>${slider.label}</span>
            <span id="slider-unit-val" style="color:var(--accent-cyan); font-family:var(--font-mono);">${slider.default} ${slider.unit}</span>
          </div>
          <input type="range" id="tut-slider-input" min="${slider.min}" max="${slider.max}" step="${slider.step}" value="${slider.default}" />
          <div id="slider-output-readout" class="slider-val-readout">Evaluating...</div>
        </div>
      `;
    }

    const html = `
      <div style="display:flex; flex-direction:column; gap:12px;">
        <div>
          <h3 style="color:var(--accent-cyan); font-size:1.2rem;">${tut.title}</h3>
          <p style="color:var(--text-muted); font-size:0.82rem; margin-top:2px;">${tut.subtitle} • ⏱️ ${tut.read_time}</p>
        </div>
        <div style="font-size:0.88rem; line-height:1.5; color:#cbd5e1; margin-top:6px;">
          ${tut.content_markdown.replace(/\n\n/g, '<br><br>').replace(/### /g, '<h4 style="color:var(--accent-gold); margin:8px 0 4px 0;">')}
        </div>
        ${sliderHtml}
        <div style="background:rgba(16, 185, 129, 0.15); border:1px solid rgba(16, 185, 129, 0.4); padding:10px; border-radius:8px; font-size:0.82rem;">
          <strong style="color:var(--accent-emerald);">💡 Key Takeaway:</strong> ${tut.key_takeaway}
        </div>
        <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:10px;">
          <button id="btn-master-tut" class="btn-secondary" style="background:linear-gradient(135deg, #10b981, #059669); color:white; border:none;">
            ✓ Mark as Mastered (+${tut.mastery_xp} XP)
          </button>
        </div>
      </div>
    `;

    this.contentEl.innerHTML = html;
    this.modalEl.classList.add('active');

    // Attach slider listener
    if (slider) {
      const inputEl = document.getElementById('tut-slider-input');
      const unitValEl = document.getElementById('slider-unit-val');
      const readoutEl = document.getElementById('slider-output-readout');

      const evalSlider = (val) => {
        unitValEl.textContent = `${val} ${slider.unit}`;
        try {
          const fn = new Function('val', slider.calculation_js);
          const resObj = fn(Number(val));
          let template = slider.display_template;
          for (const [k, v] of Object.entries(resObj)) {
            template = template.replace(`{${k}}`, v);
          }
          readoutEl.textContent = template;
        } catch (err) {
          console.error(err);
        }
      };

      inputEl.addEventListener('input', (e) => evalSlider(e.target.value));
      evalSlider(slider.default);
    }

    // Attach Master button
    document.getElementById('btn-master-tut').addEventListener('click', () => {
      this.app.sendAction('complete_tutorial', { tutorial_id: tutId });
      missionAudio.playSuccess();
      this.close();
    });
  }

  close() {
    this.modalEl.classList.remove('active');
  }
}
