// Fetch route data from backend API and animate trucks accordingly
const canvas = document.getElementById('mapCanvas');
const ctx = canvas.getContext('2d');
const W = canvas.width, H = canvas.height;

const hub = { x: W / 2, y: H / 2, label: 'Hub' };

let data = null;
let nodes = [];
let trucks = {};
let packagesMap = new Map();

let playing = false;
let lastTime = 0;
const speed = 0.0009;

//filters
let activeTruckFilter = {type: 'all', value: null};

// Layout nodes in a circular pattern around the hub
function layoutNodes(addresses) {
  const n = addresses.length;
  const radius = Math.min(W, H) / 2 - 80;
  nodes = addresses.map((addr, i) => {
    const angle = (i / n) * Math.PI * 2;
    return { id: i, label: addr, x: hub.x + Math.cos(angle) * radius, y: hub.y + Math.sin(angle) * radius };
  });
}
// Build trucks data structure from API response
function buildTrucks(api) {
  // api.trucks: object with keys '1','2','3' and arrays of package objects
  trucks = {};
  packagesMap = new Map();
  for (const t of ['1', '2', '3']) {
    const items = api.trucks[t] || [];
    const routeNodes = items.map(p => ({ pkgId: p.id, addrIdx: p.address_index, delivery_time: p.delivery_time })).filter(x => x.addrIdx !== null);
    trucks[t] = { color: t === '1' ? '#ff6b6b' : t === '2' ? '#4ecdc4' : '#ffd166', x: hub.x, y: hub.y, route: routeNodes, idx: 0, delivered: [] };
    for (const it of items) { packagesMap.set(it.id, it); }
  }
}

function matchesTruckFilter(tKey) {
  const tr = trucks[tKey];

  if (activeTruckFilter.type === 'all' || !activeTruckFilter.type) {
    return true;
  }

  if (activeTruckFilter.type === 'byTruck') {
    return tKey === activeTruckFilter.value;
  }

  if (activeTruckFilter.type === 'byId') {
    const id = Number(activeTruckFilter.value);
    return tr.route.some(r => r.pkgId === id);
  }

  if (activeTruckFilter.type === 'byStatus') {
    const requestedStatus = (activeTruckFilter.value || '').toLowerCase();
    const truckStatus = tr.delivered.length > 0 ? 'delivered' : 'en route';
    return truckStatus.includes(requestedStatus);
  }

  return true;
}

// Draw the hub, nodes, routes, and trucks on the canvas
function draw() {
  ctx.clearRect(0, 0, W, H);
  // hub
  ctx.fillStyle = '#333';
  ctx.beginPath();
  ctx.arc(hub.x, hub.y, 8, 0, Math.PI * 2);
  ctx.fill(); 
  ctx.fillStyle = '#000';
  ctx.fillText('Hub', hub.x + 10, hub.y + 4);

  // nodes
  for (const n of nodes) { 
    ctx.fillStyle = '#036';
    ctx.beginPath();
    ctx.arc(n.x, n.y, 6, 0, Math.PI * 2);
    ctx.fill(); ctx.fillStyle = '#000';
    ctx.fillText((n.id + 1) + ': ' + n.label, n.x + 8, n.y + 4);
   }

  // routes
  for (const tKey of Object.keys(trucks)) {
    const tr = trucks[tKey];

    if (!matchesTruckFilter(tKey)) continue;

    if (tr.route.length) {
      ctx.strokeStyle = 'rgba(0,0,0,0.06)';
      ctx.beginPath();
      ctx.moveTo(hub.x, hub.y);
      for (const step of tr.route) {
        const n = nodes[step.addrIdx];
        if (n) ctx.lineTo(n.x, n.y);
      }
      ctx.stroke();
    }

    ctx.fillStyle = tr.color;
    ctx.beginPath();
    ctx.rect(tr.x - 10, tr.y - 10, 20, 14);
    ctx.fill();
    ctx.fillStyle = '#000';
    ctx.fillText('' + tKey, tr.x - 3, tr.y - 0);
  }
}


function step(dt) {
  for (const tKey of Object.keys(trucks)) {
    const tr = trucks[tKey]; const route = tr.route;
    if (tr.idx >= route.length) continue;
    const targetNode = nodes[route[tr.idx].addrIdx]; if (!targetNode) { tr.idx++; continue; }
    const dx = targetNode.x - tr.x; const dy = targetNode.y - tr.y; const dist = Math.hypot(dx, dy);
    if (dist < 3) { // arrived
      tr.delivered.push(route[tr.idx].pkgId);
      tr.idx += 1; continue;
    }
    const move = dt * speed * 60;
    tr.x += (dx / dist) * move;
    tr.y += (dy / dist) * move;
  }
}

function loop(ts) {
  if (!lastTime) lastTime = ts; const dt = ts - lastTime; lastTime = ts;
  if (playing) step(dt);
  draw();
  requestAnimationFrame(loop);
}

function renderPackagePanel(filter) {
  const panel = document.getElementById('packageList'); panel.innerHTML = '';
  for (const [id, pkg] of packagesMap.entries()) {
    if (filter && !filter(pkg)) continue;
    const div = document.createElement('div'); div.className = 'packageItem';
    const delivered = Array.from(Object.values(trucks)).some(tr => tr.delivered.includes(id));
    div.innerHTML = `<strong>ID ${id}</strong> — ${delivered ? '<span style="color:green">Delivered</span>' : 'En Route'} <br/> ${pkg.address} <br/> Delivery: ${pkg.delivery_time || 'N/A'}`;
    panel.appendChild(div);
  }
}

document.getElementById('simulateBtn').addEventListener('click', () => { playing = true; });
document.getElementById('pauseBtn').addEventListener('click', () => { playing = false; });
document.getElementById('resetBtn').addEventListener('click', () => { playing = false; lastTime = 0; for (const tKey of Object.keys(trucks)) { trucks[tKey].x = hub.x; trucks[tKey].y = hub.y; trucks[tKey].idx = 0; trucks[tKey].delivered = []; } });
//hide other trucks and packages on the simulation when filtering by truck, ID, or status
document.getElementById('queryBtn').addEventListener('click', () => {
  const view = document.getElementById('viewSelect').value;
  const filterValue = document.getElementById('queryInput').value.trim();

  if (view === 'all') {
    activeTruckFilter = { type: 'all', value: null };
    renderPackagePanel();
    return;
  }

  if (view === 'byId') {
    const id = parseInt(filterValue, 10);
    activeTruckFilter = { type: 'byId', value: String(id) };
    renderPackagePanel(pkg => pkg.id === id);
    return;
  }

  if (view === 'byTruck') {
    const truckKey = filterValue;
    activeTruckFilter = { type: 'byTruck', value: truckKey };

    if (trucks[truckKey]) {
      const ids = trucks[truckKey].route.map(r => r.pkgId);
      renderPackagePanel(pkg => ids.includes(pkg.id));
    } else {
      renderPackagePanel(() => false);
    }
    return;
  }

  if (view === 'byStatus') {
    const requestedStatus = filterValue.toLowerCase();
    activeTruckFilter = { type: 'byStatus', value: requestedStatus };

    renderPackagePanel(pkg => {
      const delivered = Array.from(Object.values(trucks)).some(tr => tr.delivered.includes(pkg.id));
      const status = delivered ? 'delivered' : 'en route';
      return status.includes(requestedStatus);
    });
  }
});

// fetch API and initialize
async function init() {
  try {
    const res = await fetch('http://localhost:8001/routes');
    data = await res.json();
    document.getElementById('mileage').textContent = (data.total_mileage || 0).toFixed(2);
    document.getElementById('date').textContent = new Date().toLocaleDateString();
    layoutNodes(data.addresses || []);
    buildTrucks(data);
    renderPackagePanel();
    requestAnimationFrame(loop);
  } catch (err) {
    document.getElementById('packageList').textContent = 'Error fetching backend API: ' + err;
  }
}

init();
