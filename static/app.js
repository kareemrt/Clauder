let currentFilter = 'all';
let allItems = [];

// Tab navigation
document.querySelectorAll('.nav-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const tab = btn.dataset.tab;
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(`${tab}Tab`).classList.add('active');
    if (tab === 'recipes') loadExpiringForRecipes();
    if (tab === 'impact') loadImpact();
  });
});

document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    renderItems();
  });
});

document.getElementById('addItemBtn').addEventListener('click', openModal);

// Set default expiry date to 7 days from now
function setDefaultExpiry() {
  const d = new Date();
  d.setDate(d.getDate() + 7);
  document.getElementById('itemExpiry').value = d.toISOString().split('T')[0];
}

function openModal() {
  setDefaultExpiry();
  document.getElementById('modalOverlay').classList.add('open');
  document.getElementById('itemName').focus();
}

function closeModal() {
  document.getElementById('modalOverlay').classList.remove('open');
  document.getElementById('addItemForm').reset();
}

document.getElementById('modalOverlay').addEventListener('click', (e) => {
  if (e.target === e.currentTarget) closeModal();
});

async function fetchItems() {
  const res = await fetch('/api/items?status=active');
  allItems = await res.json();
  renderItems();
  checkAlerts();
  loadStats();
}

function renderItems() {
  const grid = document.getElementById('itemsGrid');
  let items = [...allItems];

  if (currentFilter === 'urgent') {
    items = items.filter(i => i.urgency === 'critical' || i.urgency === 'warning' || i.urgency === 'expired');
  } else if (currentFilter === 'good') {
    items = items.filter(i => i.urgency === 'good');
  }

  if (!items.length) {
    grid.innerHTML = `<div class="empty-state" style="grid-column: 1/-1">
      ${currentFilter === 'urgent' ? '✅ No items expiring soon!' : '📦 Your pantry is empty. Add your first item!'}
    </div>`;
    return;
  }

  const categoryIcons = {
    vegetables: '🥦', fruits: '🍎', meat: '🥩', dairy: '🥛',
    grains: '🌾', leftovers: '🍱', other: '📦'
  };

  grid.innerHTML = items.map(item => {
    const days = item.days_until_expiry;
    const daysText = days < 0 ? 'Expired' : days === 0 ? 'Expires today' : days === 1 ? 'Expires tomorrow' : `${days} days left`;

    return `<div class="item-card urgency-${item.urgency}" id="card-${item.id}">
      <div class="item-header">
        <span class="item-name">${categoryIcons[item.category] || '📦'} ${escHtml(item.name)}</span>
        <span class="item-category">${item.category}</span>
      </div>
      <div class="item-expiry">
        <span class="expiry-badge ${item.urgency}">${daysText}</span>
        <span style="color: var(--text-dim); font-size: 12px">${item.quantity} ${item.unit}</span>
      </div>
      <div class="item-actions">
        <button class="btn btn-warning btn-sm" onclick="markItem(${item.id}, 'used')">✓ Used</button>
        <button class="btn btn-danger btn-sm" onclick="markItem(${item.id}, 'wasted')">✗ Wasted</button>
        <button class="btn btn-ghost btn-sm" onclick="deleteItem(${item.id})">🗑</button>
      </div>
    </div>`;
  }).join('');
}

function checkAlerts() {
  const critical = allItems.filter(i => i.urgency === 'critical' || i.urgency === 'expired');
  if (critical.length > 0) {
    const names = critical.slice(0, 3).map(i => i.name).join(', ');
    document.getElementById('alertText').textContent =
      `${critical.length} item${critical.length > 1 ? 's' : ''} need${critical.length === 1 ? 's' : ''} attention: ${names}${critical.length > 3 ? '...' : ''} — Generate recipes to use them up!`;
    document.getElementById('alertBanner').style.display = '';
  }
}

async function loadStats() {
  const res = await fetch('/api/stats');
  const s = await res.json();
  document.getElementById('statActive').textContent = s.active_items;
  document.getElementById('statExpiring').textContent = s.expiring_soon;
  document.getElementById('statSaved').textContent = s.items_saved;
  document.getElementById('statRate').textContent = s.rescue_rate + '%';
}

async function markItem(id, status) {
  const card = document.getElementById(`card-${id}`);
  if (card) card.style.opacity = '0.5';

  await fetch(`/api/items/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status })
  });
  await fetchItems();
}

async function deleteItem(id) {
  await fetch(`/api/items/${id}`, { method: 'DELETE' });
  await fetchItems();
}

async function submitItem(e) {
  e.preventDefault();
  const btn = e.target.querySelector('[type="submit"]');
  btn.disabled = true;
  btn.textContent = 'Adding...';

  await fetch('/api/items', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: document.getElementById('itemName').value,
      quantity: document.getElementById('itemQty').value,
      unit: document.getElementById('itemUnit').value,
      expiry_date: document.getElementById('itemExpiry').value,
      category: document.getElementById('itemCategory').value,
    })
  });

  closeModal();
  await fetchItems();
}

// Recipes
let selectedIngredients = new Set();

async function loadExpiringForRecipes() {
  const container = document.getElementById('expiringSelect');
  const res = await fetch('/api/items?status=active');
  const items = await res.json();
  const expiring = items.filter(i => i.days_until_expiry <= 7).sort((a, b) => a.days_until_expiry - b.days_until_expiry);

  if (!expiring.length) {
    container.innerHTML = '<p class="loading-sm">No items expiring within 7 days. Add some pantry items first!</p>';
    return;
  }

  selectedIngredients = new Set(expiring.filter(i => i.days_until_expiry <= 3).map(i => i.id));

  container.innerHTML = expiring.map(item => {
    const urgency = item.urgency === 'good' ? 'good' : item.urgency;
    const selected = selectedIngredients.has(item.id) ? 'selected' : '';
    const days = item.days_until_expiry;
    const label = days <= 0 ? 'Expired' : days === 1 ? '1 day' : `${days} days`;
    return `<div class="ingredient-chip ${selected}" id="chip-${item.id}" onclick="toggleChip(${item.id})">
      <span class="chip-urgency ${urgency}"></span>
      ${escHtml(item.name)} <span style="color: var(--text-dim); font-size: 11px">${label}</span>
    </div>`;
  }).join('');
}

function toggleChip(id) {
  const chip = document.getElementById(`chip-${id}`);
  if (selectedIngredients.has(id)) {
    selectedIngredients.delete(id);
    chip.classList.remove('selected');
  } else {
    selectedIngredients.add(id);
    chip.classList.add('selected');
  }
}

async function generateRecipes() {
  if (!selectedIngredients.size) {
    alert('Please select at least one ingredient');
    return;
  }

  const btn = document.getElementById('generateBtn');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Generating with Claude...';

  const output = document.getElementById('recipesOutput');
  output.style.display = 'none';

  const res = await fetch('/api/recipes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ item_ids: [...selectedIngredients] })
  });

  btn.disabled = false;
  btn.innerHTML = '<span class="btn-icon">🍳</span> Generate Recipes';

  if (!res.ok) {
    output.innerHTML = '<p style="color: var(--danger)">Failed to generate recipes. Please try again.</p>';
    output.style.display = 'block';
    return;
  }

  const data = await res.json();
  renderRecipes(data.recipes || []);
}

function renderRecipes(recipes) {
  const output = document.getElementById('recipesOutput');
  if (!recipes.length) {
    output.innerHTML = '<p class="empty-state">No recipes generated.</p>';
    output.style.display = 'block';
    return;
  }

  output.innerHTML = `<h2 style="font-size:18px; font-weight:700; margin-bottom:16px; color: var(--text-muted)">
    ✨ ${recipes.length} Recipe${recipes.length > 1 ? 's' : ''} Generated
  </h2>` + recipes.map((r, i) => `
    <div class="recipe-card">
      <div class="recipe-title">${escHtml(r.name)}</div>
      <div class="recipe-desc">${escHtml(r.description)}</div>
      <div class="recipe-time">⏱ ${escHtml(r.time)}</div>
      ${r.uses_expiring && r.uses_expiring.length ? `
        <div class="recipe-section-title">Uses from your pantry</div>
        <div class="recipe-tags">${r.uses_expiring.map(ing => `<span class="recipe-tag">✓ ${escHtml(ing)}</span>`).join('')}</div>
      ` : ''}
      <div class="recipe-section-title">Steps</div>
      <ol class="recipe-steps">
        ${(r.steps || []).map((step, j) => `<li><span class="step-num">${j + 1}</span>${escHtml(step)}</li>`).join('')}
      </ol>
    </div>
  `).join('');

  output.style.display = 'block';
  output.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Impact
async function loadImpact() {
  const res = await fetch('/api/stats');
  const s = await res.json();

  document.getElementById('impactSavings').textContent = '$' + s.estimated_savings_usd.toFixed(0);
  document.getElementById('impactCo2').textContent = s.co2_saved_kg + ' kg';
  document.getElementById('impactRate').textContent = s.rescue_rate + '%';

  loadHistory();
}

async function loadHistory() {
  const [usedRes, wastedRes] = await Promise.all([
    fetch('/api/items?status=used'),
    fetch('/api/items?status=wasted')
  ]);
  const used = await usedRes.json();
  const wasted = await wastedRes.json();

  const all = [
    ...used.map(i => ({ ...i, outcome: 'used' })),
    ...wasted.map(i => ({ ...i, outcome: 'wasted' }))
  ].sort((a, b) => new Date(b.expiry_date) - new Date(a.expiry_date)).slice(0, 20);

  const container = document.getElementById('historyList');
  if (!all.length) {
    container.innerHTML = '<p class="empty-state">No history yet. Mark items as used or wasted to track your impact.</p>';
    return;
  }

  container.innerHTML = all.map(item => `
    <div class="history-item">
      <span class="history-outcome ${item.outcome}">${item.outcome === 'used' ? '✓ Used' : '✗ Wasted'}</span>
      <span>${escHtml(item.name)} — ${item.quantity} ${item.unit}</span>
      <span class="history-date">${item.expiry_date}</span>
    </div>
  `).join('');
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// Init
fetchItems();
