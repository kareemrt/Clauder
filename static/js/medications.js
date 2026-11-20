async function loadMedications() {
  const activeOnly = document.getElementById('active-only').checked;
  const container = document.getElementById('medications-list');
  container.innerHTML = '<p class="loading-text">Loading...</p>';
  try {
    const meds = await API.get('/api/medications/?active_only=' + activeOnly);
    if (!meds.length) {
      container.innerHTML = '<p class="empty-state">No medications found.<br>Add your first medication to get started.</p>';
      return;
    }
    container.innerHTML = meds.map(m => `
      <div class="med-card ${m.is_active ? '' : 'inactive'}">
        <div class="med-card-header">
          <span class="med-card-name">${m.name}</span>
          <span class="active-badge ${m.is_active ? 'active' : 'inactive'}">
            ${m.is_active ? 'Active' : 'Inactive'}
          </span>
        </div>
        <div class="med-card-dosage">${m.dosage}</div>
        <div class="med-card-frequency">${m.frequency} · ${m.times_per_day}×/day</div>
        ${m.instructions ? `<div class="med-card-frequency" style="font-style:italic">${m.instructions}</div>` : ''}
        <div class="med-card-frequency" style="font-size:0.8rem">Started ${formatDate(m.start_date)}</div>
        <div class="med-card-actions">
          <button class="btn btn-sm btn-secondary" onclick="editMedication(${m.id})">Edit</button>
          <button class="btn btn-sm btn-${m.is_active ? 'secondary' : 'primary'}"
            onclick="toggleActive(${m.id}, ${!m.is_active})">
            ${m.is_active ? 'Deactivate' : 'Activate'}
          </button>
          <button class="btn btn-sm btn-danger" onclick="deleteMedication(${m.id}, '${m.name}')">Delete</button>
        </div>
      </div>
    `).join('');
  } catch (e) {
    container.innerHTML = '<p class="loading-text">Failed to load medications.</p>';
  }
}

function showAddMedModal() {
  document.getElementById('med-modal-title').textContent = 'Add Medication';
  document.getElementById('med-id').value = '';
  document.getElementById('med-form').reset();
  document.getElementById('med-modal').classList.remove('hidden');
}

async function editMedication(id) {
  try {
    const med = await API.get('/api/medications/' + id);
    document.getElementById('med-modal-title').textContent = 'Edit Medication';
    document.getElementById('med-id').value = med.id;
    document.getElementById('med-name').value = med.name;
    document.getElementById('med-dosage').value = med.dosage;
    document.getElementById('med-times').value = med.times_per_day;
    document.getElementById('med-frequency').value = med.frequency;
    document.getElementById('med-instructions').value = med.instructions || '';
    if (med.end_date) {
      document.getElementById('med-end-date').value = med.end_date.slice(0, 10);
    }
    document.getElementById('med-modal').classList.remove('hidden');
  } catch (e) {
    showToast('Failed to load medication', 'error');
  }
}

function closeMedModal() {
  document.getElementById('med-modal').classList.add('hidden');
}

async function saveMedication(e) {
  e.preventDefault();
  const id = document.getElementById('med-id').value;
  const payload = {
    name: document.getElementById('med-name').value.trim(),
    dosage: document.getElementById('med-dosage').value.trim(),
    times_per_day: parseInt(document.getElementById('med-times').value),
    frequency: document.getElementById('med-frequency').value.trim(),
    instructions: document.getElementById('med-instructions').value.trim() || null,
    end_date: document.getElementById('med-end-date').value
      ? new Date(document.getElementById('med-end-date').value).toISOString()
      : null,
  };
  try {
    if (id) {
      await API.patch('/api/medications/' + id, payload);
      showToast('Medication updated!', 'success');
    } else {
      await API.post('/api/medications/', payload);
      showToast('Medication added!', 'success');
    }
    closeMedModal();
    loadMedications();
  } catch (err) {
    showToast('Failed to save: ' + err.message, 'error');
  }
}

async function toggleActive(id, active) {
  try {
    await API.patch('/api/medications/' + id, { is_active: active });
    showToast(active ? 'Medication activated' : 'Medication deactivated', 'success');
    loadMedications();
  } catch (e) {
    showToast('Failed to update medication', 'error');
  }
}

async function deleteMedication(id, name) {
  if (!confirm(`Delete "${name}"? This will also remove all associated dose logs.`)) return;
  try {
    await API.del('/api/medications/' + id);
    showToast('Medication deleted', 'success');
    loadMedications();
  } catch (e) {
    showToast('Failed to delete medication', 'error');
  }
}

loadMedications();
