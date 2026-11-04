const MATERIAL_COLORS = ['#b24e32', '#e9dfcc', '#6b4a32', '#8b897f', '#4f6c5a', '#2f8f8a'];
const ROOM_KEYS = ['living', 'engawa', 'master', 'kids', 'study', 'pool'];

export function renderPanel(t) {
  const p = t.panel;
  const roomRows = ROOM_KEYS.map((key, index) => {
    const r = t.rooms[key];
    return `<button class="room-row" data-room="${key}">
      <b>${String(index + 1).padStart(2, '0')}</b>
      <span>${r.name}</span>
      <em>${r.area}</em>
    </button>`;
  }).join('');

  const swatches = p.materials.items.map(([name, sub], i) => `
    <div class="swatch"><i style="--c:${MATERIAL_COLORS[i]}"></i><span>${name}</span><small>${sub}</small></div>
  `).join('');

  const climate = p.climate.items.map(([label, text]) => `
    <li><b>${label}</b><span>${text}</span></li>
  `).join('');

  return `<div class="panel-inner">
    <button class="panel-close" type="button" data-action="close-panel" aria-label="${t.ui.panelClose}">×</button>
    <section id="top" class="intro">
      <div class="eyebrow">${p.eyebrow}</div>
      <h1>${p.titleHtml}</h1>
      <p class="lede">${p.lede}</p>
      <div class="intro-meta">${p.meta.map((m) => `<span>${m}</span>`).join('')}</div>
    </section>

    <section id="concept" class="section">
      <div class="section-head"><span>${p.concept.num}</span><h2>${p.concept.title}</h2><small>${p.concept.en}</small></div>
      <p>${p.concept.p1}</p>
      <p>${p.concept.p2}</p>
      <figure class="quote">
        <blockquote>${p.concept.quote}</blockquote>
        <figcaption>${p.concept.cite}</figcaption>
      </figure>
    </section>

    <section id="spaces" class="section">
      <div class="section-head"><span>${p.spaces.num}</span><h2>${p.spaces.title}</h2><small>${p.spaces.en}</small></div>
      <div class="room-list">${roomRows}</div>
    </section>

    <section id="materials" class="section">
      <div class="section-head"><span>${p.materials.num}</span><h2>${p.materials.title}</h2><small>${p.materials.en}</small></div>
      <div class="swatches">${swatches}</div>
      <p class="small-note">${p.materials.note}</p>
    </section>

    <section id="climate" class="section">
      <div class="section-head"><span>${p.climate.num}</span><h2>${p.climate.title}</h2><small>${p.climate.en}</small></div>
      <ul class="climate-list">${climate}</ul>
    </section>

    <section class="section credits">
      <div class="section-head"><span>${p.build.num}</span><h2>${p.build.title}</h2><small>${p.build.en}</small></div>
      <p>${p.build.p}</p>
      <p class="tiny">${p.build.disclaimer}</p>
    </section>
  </div>`;
}

export { ROOM_KEYS };
