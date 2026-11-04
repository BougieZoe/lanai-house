/* Clean 1:100 floor plans drawn from the same coordinates as the Blender model. */
const S = 42;
const OX = 92;
const OY = 64;
const X0 = -8.65;
const Y0 = 4.55;

const px = (x) => OX + (x - X0) * S;
const py = (y) => OY + (Y0 - y) * S;

function rect(x0, x1, y0, y1, cls, extra = '') {
  return `<rect class="${cls}" x="${px(x0).toFixed(1)}" y="${py(y1).toFixed(1)}" width="${((x1-x0)*S).toFixed(1)}" height="${((y1-y0)*S).toFixed(1)}" ${extra}/>`;
}
function line(x1, y1, x2, y2, cls = 'plan-line', extra = '') {
  return `<line class="${cls}" x1="${px(x1).toFixed(1)}" y1="${py(y1).toFixed(1)}" x2="${px(x2).toFixed(1)}" y2="${py(y2).toFixed(1)}" ${extra}/>`;
}
function text(x, y, value, cls = 'plan-label', anchor = 'middle', extra = '') {
  return `<text class="${cls}" x="${px(x).toFixed(1)}" y="${py(y).toFixed(1)}" text-anchor="${anchor}" ${extra}>${value}</text>`;
}
function circle(x, y, r, cls) {
  return `<circle class="${cls}" cx="${px(x).toFixed(1)}" cy="${py(y).toFixed(1)}" r="${(r*S).toFixed(1)}"/>`;
}
function room(x0, x1, y0, y1, cls = 'plan-room') {
  return rect(x0, x1, y0, y1, cls);
}
function label(x0, x1, y0, y1, cn, en, cls = '') {
  const cx = (x0+x1)/2, cy = (y0+y1)/2;
  return `${text(cx, cy + 0.02, cn, 'plan-label')}${text(cx, cy - 0.34, en, 'plan-sub')}`;
}
function bed(x0, x1, y0, y1, head = 'left') {
  const out = [rect(x0, x1, y0, y1, 'plan-bed')];
  if (head === 'left') {
    out.push(rect(x0+0.08, x0+0.38, y0+0.12, y1-0.12, 'plan-furn-fill'));
    out.push(line(x0+0.46, y0+0.08, x0+0.46, y1-0.08, 'plan-line'));
  } else {
    out.push(rect(x1-0.38, x1-0.08, y0+0.12, y1-0.12, 'plan-furn-fill'));
    out.push(line(x1-0.46, y0+0.08, x1-0.46, y1-0.08, 'plan-line'));
  }
  return out.join('');
}
function table(x, y, w, d, chairs = 6) {
  const out = [rect(x-w/2, x+w/2, y-d/2, y+d/2, 'plan-furn-fill')];
  const spots = [
    [x-w/2-0.22, y-d/4], [x+w/2+0.22, y-d/4], [x-w/2-0.22, y+d/4], [x+w/2+0.22, y+d/4],
    [x-w/4, y-d/2-0.22], [x+w/4, y-d/2-0.22], [x-w/4, y+d/2+0.22], [x+w/4, y+d/2+0.22]
  ];
  for (let i=0;i<chairs;i++) {
    const [cx, cy] = spots[i];
    out.push(rect(cx-0.14, cx+0.14, cy-0.14, cy+0.14, 'plan-furn'));
  }
  return out.join('');
}
function sofa(x0, x1, y0, y1, side='right') {
  const out = [rect(x0,x1,y0,y1,'plan-furn-fill')];
  if (side === 'right') out.push(line(x1-0.18, y0+0.06, x1-0.18, y1-0.06, 'plan-line'));
  else out.push(line(x0+0.18, y0+0.06, x0+0.18, y1-0.06, 'plan-line'));
  return out.join('');
}
function bathIcon(x0,x1,y0,y1) {
  return `${rect(x0,x1,y0,y1,'plan-furn')}${rect(x0+0.10,x1-0.10,y0+0.10,y1-0.10,'plan-furn')}`;
}
function stairs(x0,x1,y0,y1,n=9) {
  const out = [];
  for (let i=0;i<=n;i++) {
    const yy = y0 + (y1-y0)*i/n;
    out.push(line(x0, yy, x1, yy, 'plan-stairs'));
  }
  out.push(`<path class="plan-line" d="M ${px((x0+x1)/2)} ${py(y0+0.2)} L ${px((x0+x1)/2)} ${py(y1-0.25)}" marker-end="url(#arrow)"/>`);
  return out.join('');
}
function dimH(x0, x1, y, value) {
  return `<line class="plan-dim" x1="${px(x0)}" y1="${py(y)}" x2="${px(x1)}" y2="${py(y)}" stroke="#b06a49" stroke-width=".7" marker-start="url(#tick)" marker-end="url(#tick)"/>
  <text class="plan-dim" x="${(px(x0)+px(x1))/2}" y="${py(y)-5}" text-anchor="middle">${value}</text>`;
}
function dimV(y0, y1, x, value) {
  return `<line class="plan-dim" x1="${px(x)}" y1="${py(y0)}" x2="${px(x)}" y2="${py(y1)}" stroke="#b06a49" stroke-width=".7" marker-start="url(#tick)" marker-end="url(#tick)"/>
  <text class="plan-dim" x="${px(x)+8}" y="${(py(y0)+py(y1))/2}" text-anchor="start">${value}</text>`;
}
function windowH(x0, x1, y) {
  return `<line x1="${px(x0)}" y1="${py(y)}" x2="${px(x1)}" y2="${py(y)}" stroke="#f7f1e5" stroke-width="5"/><line x1="${px(x0)}" y1="${py(y)-1.5}" x2="${px(x1)}" y2="${py(y)-1.5}" stroke="#8a8578" stroke-width=".8"/><line x1="${px(x0)}" y1="${py(y)+1.5}" x2="${px(x1)}" y2="${py(y)+1.5}" stroke="#8a8578" stroke-width=".8"/>`;
}
function windowV(y0, y1, x) {
  return `<line x1="${px(x)}" y1="${py(y0)}" x2="${px(x)}" y2="${py(y1)}" stroke="#f7f1e5" stroke-width="5"/><line x1="${px(x)-1.5}" y1="${py(y0)}" x2="${px(x)-1.5}" y2="${py(y1)}" stroke="#8a8578" stroke-width=".8"/><line x1="${px(x)+1.5}" y1="${py(y0)}" x2="${px(x)+1.5}" y2="${py(y1)}" stroke="#8a8578" stroke-width=".8"/>`;
}
function tree(x, y, r) {
  return `${circle(x,y,r,'plan-tree')}${line(x,y,x,y-0.1,'plan-line')}`;
}

function defs() {
  return `<defs>
    <marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7z" fill="#b4552d"/></marker>
    <marker id="tick" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M3 0v6" stroke="#b06a49" stroke-width=".7"/></marker>
    <pattern id="hatch" width="7" height="7" patternTransform="rotate(45)" patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="7" stroke="#b9ad9b" stroke-width=".7"/></pattern>
  </defs>`;
}

function shell() {
  return `${room(-5,5.4,-4.2,3.8,'plan-room')}${room(-8.4,-5,-2.6,3.4,'plan-room')}
  <rect x="${px(-5)}" y="${py(3.8)}" width="${10.4*S}" height="${8*S}" fill="none" stroke="#343a32" stroke-width="3.2"/>
  <rect x="${px(-8.4)}" y="${py(3.4)}" width="${3.4*S}" height="${6*S}" fill="none" stroke="#343a32" stroke-width="3.2"/>`;
}

function north() {
  return `<g transform="translate(${px(6.0)},${py(4.1)})">
    <circle r="18" fill="none" stroke="#b4552d" stroke-width=".8"/>
    <path d="M0 -12 L4 6 L0 2 L-4 6 Z" fill="#b4552d"/>
    <text class="plan-north-text" y="-23" text-anchor="middle">N</text>
  </g>`;
}

function gfPlan() {
  const out = [defs(), shell()];
  // context
  out.push(rect(-3.35,4.95,3.8,5.25,'plan-deck'));
  out.push(rect(0.25,2.95,-5.72,-4.2,'plan-deck'));
  out.push(rect(-8.15,-6.55,0.95,3.25,'plan-deck'));
  // rooms
  out.push(room(-4.85,-2.95,-4.1,-0.25,'plan-room deck'));
  out.push(room(-2.95,0.95,-4.1,-0.8));
  out.push(room(-2.95,2.0,-0.8,1.55));
  out.push(room(-2.7,0.95,1.55,3.55));
  out.push(room(-4.85,-3.70,0,1.35,'plan-room wet'));
  out.push(room(-4.85,-2.95,1.55,3.55,'plan-room dark'));
  out.push(room(0.95,3.45,-4.1,-2.40));
  out.push(room(3.45,4.95,-2.8,1.8,'plan-room dark'));
  out.push(room(3.45,4.95,1.9,3.55,'plan-room wet'));
  out.push(room(-8.25,-5.15,-2.45,0.95));
  out.push(room(-6.55,-5.15,1.0,2.68,'plan-room wet'));
  // furniture
  out.push(sofa(0.15,0.92,-3.10,-1.05,'right'));
  out.push(rect(-1.3,-0.1,-2.8,-1.7,'plan-furn'));
  out.push(table(-0.2,0.50,1.7,1.05,6));
  out.push(rect(-2.7,-2.12,1.6,3.48,'plan-furn-fill'));
  out.push(rect(-1.55,-0.18,2.02,2.72,'plan-furn-fill'));
  out.push(rect(-2.62,-2.14,0.98,1.55,'plan-furn'));
  out.push(rect(-4.3,-3.45,-2.35,-1.7,'plan-furn'));
  out.push(rect(2.58,3.27,-3.95,-2.75,'plan-furn-fill'));
  out.push(rect(1.10,2.05,-3.80,-3.10,'plan-furn'));
  out.push(bed(-8.10,-6.25,-1.90,-0.10,'left'));
  out.push(rect(-7.65,-6.05,-2.52,-2.05,'plan-furn'));
  out.push(bathIcon(-4.75,-3.82,0.15,1.28));
  out.push(bathIcon(-6.45,-5.90,1.10,1.95));
  out.push(stairs(3.55,4.88,-2.65,1.7,13));
  // labels
  out.push(label(-2.95,0.95,-4.10,-0.80,'客厅','LIVING'));
  out.push(label(-2.95,2.0,-0.80,1.55,'餐厅','DINING'));
  out.push(label(-2.7,0.95,1.55,3.55,'厨房','KITCHEN'));
  out.push(label(-4.85,-2.95,-4.10,-0.25,'茶室','TATAMI'));
  out.push(label(-4.85,-3.70,0,1.35,'盥洗','WC'));
  out.push(label(-4.85,-2.95,1.55,3.55,'家政','LAUNDRY'));
  out.push(label(0.95,3.45,-4.10,-2.40,'玄关','ENTRY'));
  out.push(label(3.45,4.95,-2.8,1.8,'楼梯','STAIR'));
  out.push(label(3.45,4.95,1.9,3.55,'卫生间','WC'));
  out.push(label(-8.25,-5.15,-2.45,0.95,'客房','GUEST'));
  out.push(label(-6.55,-5.15,1.0,2.68,'卫浴','BATH'));
  out.push(label(-8.15,-6.55,0.95,3.25,'花园门厅','GARDEN'));
  out.push(label(-3.35,4.95,3.8,5.25,'后檐廊','ENGawa'));
  out.push(label(0.25,2.95,-5.72,-4.2,'门廊','PORCH'));
  // windows
  out.push(windowH(-4.05,-1.25,-4.2));
  out.push(windowH(1.02,2.16,-4.2));
  out.push(windowH(3.15,4.62,-4.2));
  out.push(windowH(-2.72,3.18,3.8));
  out.push(windowH(-7.95,-5.65,-2.6));
  out.push(windowH(-7.95,-5.85,3.4));
  out.push(windowV(-3.86,-2.84,-5.0));
  out.push(windowV(-1.45,0.92,5.4));
  // doors, simple openings
  out.push(`<line x1="${px(1.02)}" y1="${py(-4.2)}" x2="${px(2.16)}" y2="${py(-4.2)}" stroke="#b4552d" stroke-width="3.2"/>`);
  out.push(`<line x1="${px(-5)}" y1="${py(-1.78)}" x2="${px(-5)}" y2="${py(-0.98)}" stroke="#b4552d" stroke-width="3.2"/>`);
  // dimensions
  out.push(dimH(-8.4,5.4,-6.25,'13.40 m'));
  out.push(dimV(-4.2,3.8,6.35,'8.00 m'));
  out.push(dimH(-8.4,-5.0,-3.35,'3.40 m'));
  // landscape hints
  out.push(tree(-10.9,-5.8,1.0));
  out.push(tree(7.6,2.3,1.1));
  out.push(tree(-10.5,4.2,0.8));
  out.push(`<text x="${px(-12.5)}" y="${py(-14.4)}" class="plan-sub" text-anchor="middle">STREET / 南</text>`);
  out.push(`<text x="${px(0.2)}" y="${py(-8.4)}" class="plan-sub" text-anchor="middle">ENTRY PATH</text>`);
  out.push(north());
  out.push(`<text x="${px(-8.0)}" y="${py(4.6)}" class="plan-sub" text-anchor="start">1F · 生活层</text>`);
  return `<svg viewBox="0 0 780 550" role="img" aria-label="一层平面图">${out.join('')}</svg>`;
}

function f2Plan() {
  const out = [defs(), shell()];
  out.push(rect(-3.35,4.95,3.8,5.25,'plan-deck'));
  out.push(rect(-4.48,-1.56,-5.72,-4.2,'plan-deck'));
  out.push(room(-4.85,-0.95,-4.1,0.1));
  out.push(room(-4.85,-0.95,0.1,3.70));
  out.push(room(0.0,3.45,-4.1,-0.58));
  out.push(room(0.10,2.38,1.35,3.52,'plan-room wet'));
  out.push(room(-0.95,3.45,-0.58,1.35));
  out.push(room(2.45,3.45,2.10,3.45,'plan-room dark'));
  out.push(room(3.45,4.95,-2.8,1.8,'plan-room dark'));
  out.push(bed(-4.55,-2.55,-2.55,-0.75,'left'));
  out.push(rect(-4.25,-3.55,-3.9,-3.25,'plan-furn'));
  out.push(rect(-4.85,-2.35,-0.62,-0.02,'plan-furn-fill'));
  out.push(sofa(-4.62,-2.70,1.05,1.95,'left'));
  out.push(sofa(-4.62,-2.70,2.30,3.20,'left'));
  out.push(rect(-2.55,-1.05,3.10,3.55,'plan-furn'));
  out.push(rect(2.90,3.35,-3.90,-1.00,'plan-furn-fill'));
  out.push(rect(0.15,0.95,-2.55,-1.05,'plan-furn-fill'));
  out.push(bathIcon(0.18,1.50,2.50,3.35));
  out.push(bathIcon(1.75,2.25,1.55,2.40));
  out.push(rect(0.15,1.35,0.82,1.12,'plan-furn-fill'));
  out.push(rect(2.50,3.40,2.15,3.40,'plan-furn-fill'));
  out.push(stairs(3.55,4.88,-2.65,1.70,13));
  out.push(`<path d="M ${px(3.45)} ${py(1.8)} L ${px(3.45)} ${py(-2.8)} L ${px(4.95)} ${py(-2.8)}" fill="none" stroke="#343a32" stroke-width="1.2" stroke-dasharray="4 3"/>`);
  out.push(label(-4.85,-0.95,-4.10,0.10,'主卧','MASTER'));
  out.push(label(-4.85,-0.95,0.10,3.70,'儿童房','KIDS'));
  out.push(label(0.0,3.45,-4.10,-0.58,'书房 / 客房','STUDY'));
  out.push(label(0.10,2.38,1.35,3.52,'浴室','BATH'));
  out.push(label(-0.95,3.45,-0.58,1.35,'过厅','HALL'));
  out.push(label(2.45,3.45,2.10,3.45,'储物','STORAGE'));
  out.push(label(3.45,4.95,-2.8,1.8,'挑空','VOID'));
  out.push(label(-4.48,-1.56,-5.72,-4.2,'南阳台','BALCONY'));
  out.push(label(-3.35,4.95,3.8,5.25,'后檐台','REAR DECK'));
  out.push(windowH(-4.42,-1.62,-4.2));
  out.push(windowH(-0.52,0.92,-4.2));
  out.push(windowH(2.38,4.58,-4.2));
  out.push(windowH(-4.22,-2.38,3.8));
  out.push(windowH(0.42,1.82,3.8));
  out.push(windowV(-3.56,-2.90,-5.0));
  out.push(windowV(-2.72,-1.10,5.4));
  out.push(dimH(-8.4,5.4,-6.25,'13.40 m'));
  out.push(dimV(-4.2,3.8,6.35,'8.00 m'));
  out.push(dimH(-4.48,-1.56,-6.25,'2.92 m'));
  out.push(tree(-10.9,-5.8,1.0));
  out.push(tree(7.6,2.3,1.1));
  out.push(north());
  out.push(`<text x="${px(-8.0)}" y="${py(4.6)}" class="plan-sub" text-anchor="start">2F · 卧室层</text>`);
  out.push(`<rect x="${px(-8.3)}" y="${py(3.2)}" width="${(3.3*S).toFixed(1)}" height="${(5.7*S).toFixed(1)}" fill="url(#hatch)" opacity=".45"/>`);
  out.push(label(-8.2,-5.1,0.0,3.1,'低层屋面','LOW ROOF'));
  return `<svg viewBox="0 0 780 550" role="img" aria-label="二层平面图">${out.join('')}</svg>`;
}

export const plans = { gf: gfPlan, f2: f2Plan };

// Canonical Chinese label -> i18n key. Used by the viewer when switching languages.
export const PLAN_KEY = {
  '客厅': 'living', '餐厅': 'dining', '厨房': 'kitchen', '茶室': 'tatami',
  '盥洗': 'powder', '家政': 'laundry', '玄关': 'entry', '楼梯': 'stair',
  '卫生间': 'wc', '客房': 'guest', '卫浴': 'bath', '花园门厅': 'gardenHall',
  '后檐廊': 'engawa', '门廊': 'porch', '主卧': 'master', '儿童房': 'kids',
  '书房 / 客房': 'study', '浴室': 'bath2', '过厅': 'hall', '储物': 'storage',
  '挑空': 'void', '南阳台': 'balcony', '后檐台': 'rearDeck', '低层屋面': 'lowRoof',
};
