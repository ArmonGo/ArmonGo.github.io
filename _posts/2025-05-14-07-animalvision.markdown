---
layout: post
title:  "Animal vision"
date:   2025-08-21 00:00:00
excerpt: "Look through the eyes of various animals"
image:
  feature: vision.jpg
  hero_top_position: -200px
---

<style>
  :root {
    color-scheme: light dark;
    --bg: #fafafa;
    --fg: #0f172a; /* slate-900 */
    --muted: #64748b; /* slate-500 */
    --line: rgba(15, 23, 42, 0.12);
    --accent: #111827; /* nearly black */
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #0b0f1a; /* deep slate */
      --fg: #e5e7eb; /* neutral-200 */
      --muted: #94a3b8; /* slate-400 */
      --line: rgba(226, 232, 240, 0.24);
      --accent: #e5e7eb;
    }
  }

  * { box-sizing: border-box; }
  html, body { height: 100%; }
  body {
    margin: 0; 
    background: var(--bg);
    color: var(--fg);
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Inter, "Helvetica Neue", Arial, "Apple Color Emoji", "Segoe UI Emoji";
    line-height: 1.5;
  }

  .wrap {
    max-width: 1080px;
    margin: 7vh auto 12vh;
    padding: 0 24px;
  }

  header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 16px;
    margin-bottom: 28px;
  }
  h1 {
    font-size: clamp(20px, 3.2vw, 34px);
    font-weight: 600;
    letter-spacing: 0.01em;
    margin: 0;
  }
  .sub {
    color: var(--muted);
    font-size: 0.95rem;
  }

  .controls {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px 14px;
    margin: 20px 0 10px;
  }

  .file {
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border: 1px solid var(--line);
    border-radius: 12px;
    background: transparent;
    cursor: pointer;
    user-select: none;
  }
  .file input { position: absolute; inset: 0; opacity: 0; cursor: pointer; }

  select, button {
    appearance: none;
    border: 1px solid var(--line);
    background: transparent;
    color: var(--fg);
    padding: 10px 14px;
    border-radius: 12px;
    font: inherit;
  }
  select { min-width: 160px; }

  button.ghost { border-style: dashed; }
  button:hover, select:hover, .file:hover { border-color: var(--fg); }
  button:active { transform: translateY(1px); }

  .grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 22px;
    margin-top: 22px;
  }
  @media (min-width: 860px) {
    .grid { grid-template-columns: 1fr 1fr; }
  }

  figure { margin: 0; }
  figcaption { color: var(--muted); font-size: 0.9rem; margin-bottom: 8px; }

  canvas {
    width: 100%;
    height: auto;
    display: block;
    border-radius: 12px;
    border: 2px solid var(--line);
    background:
      linear-gradient(45deg, rgba(127,127,127,.05) 25%, transparent 25%),
      linear-gradient(-45deg, rgba(127,127,127,.05) 25%, transparent 25%),
      linear-gradient(45deg, transparent 75%, rgba(127,127,127,.05) 75%),
      linear-gradient(-45deg, transparent 75%, rgba(127,127,127,.05) 75%);
    background-size: 20px 20px;
    background-position: 0 0, 0 10px, 10px -10px, -10px 0;
  }

  footer { margin-top: 28px; display: flex; gap: 12px; flex-wrap: wrap; }
  .muted { color: var(--muted); font-size: 0.9rem; }
</style>


<div class="wrap">
  <header>
    <div>
      <h1>Animal Vision Filters</h1>
      <div class="sub">See the world through their eyes</div>
    </div>
  </header>

  <div class="controls">
    <label class="file" title="Choose an image">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="7 10 12 5 17 10"/>
        <line x1="12" y1="5" x2="12" y2="21"/>
      </svg>
      <span>Upload image</span>
      <input type="file" id="imageInput" accept="image/*" />
    </label>

    <select id="filterSelect" aria-label="Pick a filter">
      <option value="dog">Dog</option>
      <option value="cat">Cat</option>
      <option value="bee">Bee</option>
      <option value="bird">Bird</option>
      <option value="horse">Horse</option>
      <option value="goldfish">Goldfish</option>
      <option value="snake">Snake</option>
      <option value="mantis">Mantis shrimp</option>
      <option value="spider">Jumping spider</option>
      <option value="octopus">Octopus</option>
      <option value="anableps">Four-eyed fish</option>
      <option value="shark">Shark</option>
    </select>

    <button class="ghost" id="applyBtn">Apply</button>
    <button id="downloadBtn">Download</button>
  </div>

  <div class="grid">
    <figure>
      <figcaption>Original</figcaption>
      <canvas id="inputCanvas"></canvas>
    </figure>
    <figure>
      <figcaption>Filtered</figcaption>
      <canvas id="outputCanvas"></canvas>
    </figure>
  </div>

  <footer>
    <div class="muted">Tip: try different filters and compare side by side.</div>
  </footer>
</div>

<script>
// Download current output
const outCanvas = document.getElementById('outputCanvas');
const dlBtn = document.getElementById('downloadBtn');
dlBtn.addEventListener('click', () => {
  if (!outCanvas.width || !outCanvas.height) return;
  const link = document.createElement('a');
  link.download = 'animal_view.png';
  link.href = outCanvas.toDataURL('image/png');
  link.click();
});
</script>

<script>
// =======================
// Animal Vision Filters (same logic, tidied)
// =======================
function clamp(v, min=0, max=255) { return Math.max(min, Math.min(max, v)); }

// Cat view
function catView(imageData) {
  const data = imageData.data;
  for (let i = 0; i < data.length; i += 4) {
    let r = data[i], g = data[i+1], b = data[i+2];
    let grayRG = (r + g) / 2;
    data[i] = clamp(grayRG * 1.3);
    data[i+1] = clamp(grayRG * 1.3);
    data[i+2] = clamp(b * 1.3);
  }
  return imageData;
}

// Horse view
function horseView(imageData) {
  const data = imageData.data;
  for (let i = 0; i < data.length; i += 4) {
    let r = data[i], g = data[i+1], b = data[i+2];
    let grayRG = (r + g) / 2;
    data[i] = clamp(grayRG);
    data[i+1] = clamp(grayRG);
    data[i+2] = clamp(b);
  }
  return imageData;
}

// Goldfish view
function goldfishView(imageData) {
  const data = imageData.data;
  for (let i = 0; i < data.length; i += 4) {
    let r = data[i]*0.7, g = data[i+1]*1.2, b = data[i+2]*1.3;
    let uv = Math.sqrt(data[i+2]/255)*255*0.3;
    data[i] = clamp(r + uv);
    data[i+1] = clamp(g);
    data[i+2] = clamp(b);
  }
  return imageData;
}

// Dog view
function dogView(imageData) {
  const data = imageData.data;
  for (let i = 0; i < data.length; i += 4) {
    let r = data[i], g = data[i+1], b = data[i+2];
    let grayRG = (r + g) / 2;
    data[i] = grayRG;
    data[i+1] = grayRG;
    data[i+2] = b;
  }
  return imageData;
}

// Bee view
function beeView(imageData) {
  const data = imageData.data;
  for (let i = 0; i < data.length; i += 4) {
    let r = Math.sqrt(data[i+2]/255)*255; // fake UV
    data[i] = clamp(r);
    // g, b unchanged
  }
  return imageData;
}

// Bird view
function birdView(imageData) {
  const data = imageData.data;
  for (let i = 0; i < data.length; i += 4) {
    let r = data[i], g = data[i+1], b = data[i+2];
    let maxV = Math.max(r,g,b), minV = Math.min(r,g,b);
    let s = maxV - minV; // saturation proxy
    r = clamp(r + s*0.5);
    g = clamp(g + s*0.5);
    b = clamp(b + s*0.5);
    r = clamp(r * 1.2); g = clamp(g * 1.2); b = clamp(b * 1.2);
    let uv = Math.sqrt(data[i+2]/255)*255*0.3;
    data[i] = clamp(r + uv);
    data[i+1] = g;
    data[i+2] = b;
  }
  return imageData;
}

// Snake view (thermal / jet)
function snakeView(imageData) {
  const data = imageData.data;
  function jetColormap(v) {
    v = v/255;
    let r = Math.min(1, Math.max(0, 1.5 - Math.abs(4*v-3)));
    let g = Math.min(1, Math.max(0, 1.5 - Math.abs(4*v-2)));
    let b = Math.min(1, Math.max(0, 1.5 - Math.abs(4*v-1)));
    return [r*255, g*255, b*255];
  }
  for (let i = 0; i < data.length; i += 4) {
    let gray = 0.2989*data[i] + 0.587*data[i+1] + 0.114*data[i+2];
    let [jr,jg,jb] = jetColormap(gray);
    data[i] = jr; data[i+1] = jg; data[i+2] = jb;
  }
  return imageData;
}

// Mantis shrimp — posterize + saturation + slight blue sheen
function mantisShrimpView(imageData){
  const d=imageData.data;
  const Q=v=>Math.round(v/42)*42; // ~6 bands
  for(let i=0;i<d.length;i+=4){
    let r=Q(d[i]), g=Q(d[i+1]), b=Q(d[i+2]);
    const m=(r+g+b)/3;
    r=clamp(m+(r-m)*1.6); g=clamp(m+(g-m)*1.6); b=clamp(m+(b-m)*1.6);
    const sheen=((r+g+b)/3)/255*30;
    d[i]=clamp(r); d[i+1]=clamp(g); d[i+2]=clamp(b+sheen);
  }
  return imageData;
}

// Jumping spider — UV+green, center emphasis (pseudo-fovea)
function jumpingSpiderView(imageData){
  const d=imageData.data, w=imageData.width, h=imageData.height;
  const cx=w/2, cy=h/2, maxR=Math.hypot(cx,cy);
  for(let i=0;i<d.length;i+=4){
    const p=i/4, x=p%w, y=(p-x)/w;
    const uv=Math.sqrt(d[i+2]/255)*255; // fake UV from blue
    let R=clamp(d[i]*0.3), G=d[i+1], B=clamp(uv);
    const dist=Math.hypot(x-cx,y-cy)/maxR;
    const gain=1.2 - dist*0.6; // 1.2 center → 0.6 edge
    d[i]=clamp(R*gain); d[i+1]=clamp(G*gain); d[i+2]=clamp(B*gain);
  }
  return imageData;
}

// Octopus — high-contrast monochrome
function octopusView(imageData){
  const d=imageData.data;
  for(let i=0;i<d.length;i+=4){
    let g=0.3*d[i]+0.59*d[i+1]+0.11*d[i+2];
    g=clamp((g-128)*1.3+128);
    d[i]=d[i+1]=d[i+2]=g;
  }
  return imageData;
}

// Four-eyed fish (Anableps) — split horizon
function anablepsView(imageData){
  const d=imageData.data, w=imageData.width, h=imageData.height, mid=h/2;
  for(let i=0;i<d.length;i+=4){
    const p=i/4, y=Math.floor(p/w);
    let r=d[i], g=d[i+1], b=d[i+2];
    if(y<mid){ d[i]=clamp(r*1.05); d[i+1]=g; d[i+2]=clamp(b*0.95); } // air
    else { d[i]=clamp(r*0.3); d[i+1]=clamp(g*1.1); d[i+2]=clamp(b*1.2); } // water
  }
  return imageData;
}

// Shark — blue-green weighted near-mono
function sharkView(imageData){
  const d=imageData.data;
  for(let i=0;i<d.length;i+=4){
    const g=(d[i+1]*0.6 + d[i+2]*0.4);
    const v=clamp((g-20)*1.1+20);
    d[i]=v; d[i+1]=v; d[i+2]=v;
  }
  return imageData;
}

const filters = { dog: dogView, 
                cat: catView, bee: beeView, 
                bird: birdView, horse: horseView, goldfish: goldfishView, snake: snakeView ,  mantis: mantisShrimpView,
                spider: jumpingSpiderView,
                octopus: octopusView,
                anableps: anablepsView,
                shark: sharkView};

// =======================
// Canvas Setup
// =======================
const inputCanvas = document.getElementById('inputCanvas');
const outputCanvas = document.getElementById('outputCanvas');
const inputCtx = inputCanvas.getContext('2d');
const outputCtx = outputCanvas.getContext('2d');

const img = new Image();

const fileInput = document.getElementById('imageInput');
fileInput.addEventListener('change', (e) => {
  const file = e.target.files && e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => { img.src = ev.target.result; };
  reader.readAsDataURL(file);
});

img.onload = () => {
  const w = img.naturalWidth;
  const h = img.naturalHeight;
  inputCanvas.width = w; inputCanvas.height = h;
  outputCanvas.width = w; outputCanvas.height = h;
  inputCtx.drawImage(img, 0, 0);
};

// =======================
// Apply Filter
// =======================
function applyFilter() {
  if (!inputCanvas.width || !inputCanvas.height) return;
  const filterName = document.getElementById('filterSelect').value;
  const fn = filters[filterName];
  if (!fn) return;
  const imgData = inputCtx.getImageData(0, 0, inputCanvas.width, inputCanvas.height);
  const outputData = fn(imgData);
  outputCtx.putImageData(outputData, 0, 0);
}

document.getElementById('applyBtn').addEventListener('click', applyFilter);
</script>