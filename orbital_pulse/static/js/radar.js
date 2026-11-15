/**
 * ORBITAL PULSE - 6-Axis Trade-Off Radar Chart
 * Section 8: Live 6-Axis Trade-Off Radar & Vital Gauges
 * Renders dynamic SVG polygon for Mass, Power, Budget, Data Link, Thermal, Bio-Vitals.
 */

class TradeOffRadar {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.axes = [
      { key: 'mass_margin', label: 'Mass Margin' },
      { key: 'power_margin', label: 'Power Balance' },
      { key: 'budget_efficiency', label: 'Budget Effic.' },
      { key: 'data_link', label: 'Data Downlink' },
      { key: 'thermal_integrity', label: 'Thermal / Cryo' },
      { key: 'bio_yield', label: 'Bio / Science' }
    ];
    this.size = 220;
    this.center = this.size / 2;
    this.radius = 80;
    this.init();
  }

  init() {
    if (!this.container) return;
    this.render({});
  }

  getCoordinates(index, value) {
    const angle = (Math.PI * 2 / this.axes.length) * index - Math.PI / 2;
    const r = (Math.max(5, Math.min(100, value)) / 100) * this.radius;
    return {
      x: this.center + r * Math.cos(angle),
      y: this.center + r * Math.sin(angle)
    };
  }

  render(metrics = {}) {
    if (!this.container) return;

    // Grid circles
    let circlesSvg = '';
    [0.25, 0.5, 0.75, 1.0].forEach(scale => {
      circlesSvg += `<circle cx="${this.center}" cy="${this.center}" r="${this.radius * scale}" 
        fill="none" stroke="rgba(56, 189, 248, 0.15)" stroke-width="1" stroke-dasharray="3,3" />`;
    });

    // Axis lines and labels
    let axesSvg = '';
    let polygonPoints = [];

    this.axes.forEach((axis, i) => {
      const outerCoord = this.getCoordinates(i, 100);
      const labelCoord = this.getCoordinates(i, 122);
      axesSvg += `<line x1="${this.center}" y1="${this.center}" x2="${outerCoord.x}" y2="${outerCoord.y}" 
        stroke="rgba(56, 189, 248, 0.25)" stroke-width="1" />`;

      axesSvg += `<text x="${labelCoord.x}" y="${labelCoord.y + 3}" fill="#94a3b8" font-size="9" 
        font-family="system-ui" text-anchor="middle" font-weight="600">${axis.label}</text>`;

      const val = metrics[axis.key] !== undefined ? metrics[axis.key] : 50;
      const pt = this.getCoordinates(i, val);
      polygonPoints.push(`${pt.x},${pt.y}`);
    });

    const pointsStr = polygonPoints.join(' ');

    const svgHtml = `
      <svg width="${this.size}" height="${this.size}" viewBox="0 0 ${this.size} ${this.size}">
        <defs>
          <radialGradient id="radarFill" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.45" />
            <stop offset="100%" stop-color="#0ea5e9" stop-opacity="0.15" />
          </radialGradient>
        </defs>
        ${circlesSvg}
        ${axesSvg}
        <polygon points="${pointsStr}" fill="url(#radarFill)" stroke="#00f0ff" stroke-width="2" 
          filter="drop-shadow(0 0 6px rgba(0, 240, 255, 0.5))" />
      </svg>
    `;

    this.container.innerHTML = svgHtml;
  }
}
