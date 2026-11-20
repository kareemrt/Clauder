async function loadDashboard() {
  try {
    const summary = await API.get('/api/reports/summary');
    renderSummaryCards(summary);
    renderAdherenceChart(summary.medication_reports);
    renderSymptoms(summary.recent_symptoms);
  } catch (e) {
    showToast('Failed to load dashboard: ' + e.message, 'error');
  }
  loadTodayDoses();
}

function renderSummaryCards(summary) {
  document.getElementById('stat-active-meds').textContent = summary.active_medications;
  document.getElementById('stat-adherence').textContent = summary.overall_adherence_rate + '%';
  document.getElementById('stat-today-taken').textContent = summary.doses_taken_today;
  document.getElementById('stat-today-remaining').textContent =
    Math.max(0, summary.doses_scheduled_today - summary.doses_taken_today);
  document.querySelectorAll('.summary-card').forEach(c => c.classList.remove('loading'));
}

async function loadTodayDoses() {
  const container = document.getElementById('today-doses-list');
  try {
    const doses = await API.get('/api/doses/today');
    if (!doses.length) {
      container.innerHTML = '<p class="empty-state">No doses scheduled for today.<br>Add medications to get started.</p>';
      return;
    }
    container.innerHTML = doses.map(d => `
      <div class="dose-item ${d.was_taken ? 'taken' : ''}" id="dose-${d.id}">
        <div class="dose-info">
          <div class="dose-name">Medication #${d.medication_id}</div>
          <div class="dose-time">Scheduled: ${formatDateTime(d.scheduled_time)}</div>
          ${d.taken_at ? `<div class="dose-time">Taken at: ${formatDateTime(d.taken_at)}</div>` : ''}
        </div>
        <span class="dose-status ${d.was_taken ? 'taken' : 'pending'}">
          ${d.was_taken ? '✓ Taken' : 'Pending'}
        </span>
        ${!d.was_taken ? `<button class="btn btn-sm btn-primary" onclick="markTaken(${d.id})">Take</button>` : ''}
      </div>
    `).join('');
  } catch (e) {
    container.innerHTML = '<p class="loading-text">Failed to load doses.</p>';
  }
}

async function markTaken(doseId) {
  try {
    await API.post(`/api/doses/${doseId}/take`, {});
    showToast('Dose marked as taken!', 'success');
    loadTodayDoses();
    loadDashboard();
  } catch (e) {
    showToast('Failed to update dose: ' + e.message, 'error');
  }
}

function renderAdherenceChart(reports) {
  const container = document.getElementById('adherence-chart');
  if (!reports.length) {
    container.innerHTML = '<p class="empty-state">No medication data yet. Add medications to see adherence.</p>';
    return;
  }
  container.innerHTML = reports.map(r => {
    const pct = r.adherence_rate;
    const fillClass = pct >= 80 ? '' : pct >= 50 ? 'medium' : 'low';
    return `
      <div class="adherence-row">
        <span class="adherence-name" title="${r.medication_name}">${r.medication_name}</span>
        <div class="adherence-bar-bg">
          <div class="adherence-bar-fill ${fillClass}" style="width: ${pct}%"></div>
        </div>
        <span class="adherence-pct">${pct}%</span>
      </div>
    `;
  }).join('');
}

function renderSymptoms(symptoms) {
  const container = document.getElementById('symptoms-list');
  if (!symptoms.length) {
    container.innerHTML = '<p class="empty-state">No symptoms logged recently.</p>';
    return;
  }
  container.innerHTML = symptoms.map(s => `
    <div class="symptom-item">
      <div>
        <div class="symptom-name">${s.symptom}</div>
        <div class="symptom-meta">${formatDateTime(s.logged_at)} ${s.notes ? '· ' + s.notes : ''}</div>
      </div>
      <span class="severity-badge severity-${severityClass(s.severity)}">${s.severity}</span>
    </div>
  `).join('');
}

async function logSymptom(e) {
  e.preventDefault();
  const name = document.getElementById('symptom-name').value.trim();
  const severity = parseInt(document.getElementById('symptom-severity').value);
  const notes = document.getElementById('symptom-notes').value.trim();
  try {
    await API.post('/api/symptoms/', { symptom: name, severity, notes: notes || null });
    showToast('Symptom logged!', 'success');
    e.target.reset();
    document.getElementById('severity-label').textContent = '5';
    loadDashboard();
  } catch (err) {
    showToast('Failed to log symptom: ' + err.message, 'error');
  }
}

async function showLogDoseModal() {
  try {
    const meds = await API.get('/api/medications/?active_only=true');
    const select = document.getElementById('dose-medication');
    select.innerHTML = meds.map(m => `<option value="${m.id}">${m.name} (${m.dosage})</option>`).join('');
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    document.getElementById('dose-time').value = now.toISOString().slice(0, 16);
  } catch (e) {
    showToast('Failed to load medications', 'error');
    return;
  }
  document.getElementById('dose-modal').classList.remove('hidden');
}

function closeDoseModal() {
  document.getElementById('dose-modal').classList.add('hidden');
}

async function logDose(e) {
  e.preventDefault();
  const payload = {
    medication_id: parseInt(document.getElementById('dose-medication').value),
    scheduled_time: new Date(document.getElementById('dose-time').value).toISOString(),
    was_taken: document.getElementById('dose-taken').value === 'true',
    notes: document.getElementById('dose-notes').value || null,
  };
  if (payload.was_taken) payload.taken_at = new Date().toISOString();
  try {
    await API.post('/api/doses/', payload);
    showToast('Dose logged!', 'success');
    closeDoseModal();
    loadDashboard();
  } catch (err) {
    showToast('Failed to log dose: ' + err.message, 'error');
  }
}

loadDashboard();
