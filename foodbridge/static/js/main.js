const CAT_ICONS = {
  prepared: '🍱', produce: '🥦', bakery: '🍞', dairy: '🥛',
  protein: '🍖', 'non-perishable': '🥫', beverages: '🧃', other: '🍽️'
};

const DONOR_ICONS = {
  restaurant: '🍽️', grocery: '🛒', bakery: '🥐', hotel: '🏨',
  catering: '🎪', farm: '🌾', institution: '🏫', individual: '👤', other: '📦'
};

function categoryIcon(cat) {
  return CAT_ICONS[cat] || '🍽️';
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr + 'T00:00:00');
  const now = new Date();
  const diff = Math.ceil((d - now) / (1000 * 60 * 60 * 24));
  const formatted = d.toLocaleDateString('en-US', {month: 'short', day: 'numeric'});
  if (diff <= 0) return `<span class="expiry urgent">Expires today</span>`;
  if (diff === 1) return `<span class="expiry urgent">Expires tomorrow</span>`;
  if (diff <= 3) return `<span class="expiry soon">Expires ${formatted}</span>`;
  return `<span class="expiry ok">Use by ${formatted}</span>`;
}

function urgencyClass(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr + 'T00:00:00');
  const diff = Math.ceil((d - new Date()) / (1000 * 60 * 60 * 24));
  if (diff <= 1) return 'card-urgent';
  if (diff <= 3) return 'card-soon';
  return '';
}

function renderListingCard(listing, showClaimBtn = false) {
  const donorIcon = DONOR_ICONS[listing.donor_type] || '📦';
  const catIcon = categoryIcon(listing.food_category);
  const urgency = urgencyClass(listing.expiry_date);
  return `
    <div class="listing-card ${urgency}">
      <div class="card-header">
        <span class="cat-badge">${catIcon} ${listing.food_category}</span>
        ${listing.expiry_date ? formatDate(listing.expiry_date) : ''}
      </div>
      <h3 class="card-title">${listing.food_name}</h3>
      <div class="card-meta">
        <span>${donorIcon} ${listing.donor_name}</span>
        <span>📦 ${listing.quantity} ${listing.unit}</span>
      </div>
      <div class="card-location">📍 ${listing.neighborhood}, ${listing.city}</div>
      ${listing.notes ? `<p class="card-notes">${listing.notes}</p>` : ''}
      ${showClaimBtn ? `<button class="btn btn-primary card-btn" onclick="openClaimModal(${listing.id})">Reserve →</button>` : ''}
    </div>
  `;
}
