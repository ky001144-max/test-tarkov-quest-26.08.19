/**
 * QuestManager - Handles Quest filtering, UI rendering, progression tracking and map sync
 */
class QuestManager {
  constructor(options) {
    this.containerEl = document.getElementById(options.containerId || 'quest-list-container');
    this.searchInputEl = document.getElementById('quest-search-input');
    this.clearSearchBtn = document.getElementById('btn-clear-search');
    this.uncompletedOnlyEl = document.getElementById('toggle-uncompleted-only');
    this.hasGpsOnlyEl = document.getElementById('toggle-has-gps-only');
    this.filteredCountEl = document.getElementById('filtered-quest-count');
    this.progressPercentEl = document.getElementById('progress-percent');
    this.progressCountEl = document.getElementById('progress-count');
    this.progressBarFillEl = document.getElementById('progress-bar-fill');

    // Data
    this.allQuests = [];
    this.completedQuestIds = new Set();

    // Filters
    this.selectedMapId = 'customs';
    this.selectedTraderId = 'all';
    this.searchQuery = '';
    this.uncompletedOnly = false;
    this.hasGpsOnly = false;

    // Callbacks
    this.onLocateObjective = options.onLocateObjective || null;

    this.loadCompletedQuests();
    this.initEvents();
  }

  loadCompletedQuests() {
    try {
      const saved = localStorage.getItem('tarkov_completed_quests');
      if (saved) {
        this.completedQuestIds = new Set(JSON.parse(saved));
      }
    } catch (e) {
      console.warn('Could not load completed quests from localStorage', e);
    }
  }

  saveCompletedQuests() {
    try {
      localStorage.setItem('tarkov_completed_quests', JSON.stringify(Array.from(this.completedQuestIds)));
    } catch (e) {
      console.warn('Could not save completed quests', e);
    }
    this.updateProgressStats();
  }

  initEvents() {
    // Search input
    this.searchInputEl?.addEventListener('input', (e) => {
      this.searchQuery = e.target.value.trim().toLowerCase();
      this.clearSearchBtn.style.display = this.searchQuery ? 'block' : 'none';
      this.render();
    });

    this.clearSearchBtn?.addEventListener('click', () => {
      this.searchInputEl.value = '';
      this.searchQuery = '';
      this.clearSearchBtn.style.display = 'none';
      this.render();
    });

    // Toggles
    this.uncompletedOnlyEl?.addEventListener('change', (e) => {
      this.uncompletedOnly = e.target.checked;
      this.render();
    });

    this.hasGpsOnlyEl?.addEventListener('change', (e) => {
      this.hasGpsOnly = e.target.checked;
      this.render();
    });
  }

  setQuests(quests) {
    this.allQuests = quests;
    this.updateProgressStats();
    this.render();
  }

  setMap(mapId) {
    this.selectedMapId = mapId;
    this.render();
  }

  setTrader(traderId) {
    this.selectedTraderId = traderId;
    this.render();
  }

  toggleQuestComplete(questId) {
    if (this.completedQuestIds.has(questId)) {
      this.completedQuestIds.delete(questId);
    } else {
      this.completedQuestIds.add(questId);
    }
    this.saveCompletedQuests();
    this.render();
  }

  updateProgressStats() {
    const total = this.allQuests.length;
    if (total === 0) return;

    const completed = this.completedQuestIds.size;
    const percent = Math.round((completed / total) * 100);

    if (this.progressPercentEl) this.progressPercentEl.textContent = `${percent}%`;
    if (this.progressCountEl) this.progressCountEl.textContent = `(${completed}/${total})`;
    if (this.progressBarFillEl) this.progressBarFillEl.style.width = `${percent}%`;
  }

  /**
   * Strictly filters quests that have at least one objective on the currently selected map
   */
  getFilteredQuests() {
    return this.allQuests.filter(quest => {
      // 1. Strict Map filter: Must have objectives on this specific map
      const hasObjectiveOnMap = quest.objectives.some(o => o.map_id === this.selectedMapId);
      if (!hasObjectiveOnMap) {
        return false;
      }

      // 2. Trader filter
      if (this.selectedTraderId !== 'all') {
        const tId = quest.trader?.id?.toLowerCase();
        if (tId !== this.selectedTraderId.toLowerCase()) return false;
      }

      // 3. Uncompleted filter
      if (this.uncompletedOnly && this.completedQuestIds.has(quest.id)) {
        return false;
      }

      // 4. GPS only filter (must have GPS on the current map)
      if (this.hasGpsOnly) {
        const hasGpsOnCurrentMap = quest.objectives.some(o => o.map_id === this.selectedMapId && o.gps);
        if (!hasGpsOnCurrentMap) return false;
      }

      // 5. Search query filter
      if (this.searchQuery) {
        const query = this.searchQuery;
        const inTitleKo = quest.title_ko.toLowerCase().includes(query);
        const inTitleEn = quest.title_en.toLowerCase().includes(query);
        const inTrader = quest.trader?.name_ko?.toLowerCase().includes(query) || quest.trader?.name_en?.toLowerCase().includes(query);
        const inObjectives = quest.objectives.some(o => 
          o.description_ko?.toLowerCase().includes(query) || 
          o.target?.toLowerCase().includes(query)
        );
        if (!inTitleKo && !inTitleEn && !inTrader && !inObjectives) {
          return false;
        }
      }

      return true;
    });
  }

  render() {
    if (!this.containerEl) return;
    const filtered = this.getFilteredQuests();

    if (this.filteredCountEl) {
      this.filteredCountEl.textContent = filtered.length;
    }

    if (filtered.length === 0) {
      this.containerEl.innerHTML = `
        <div class="empty-state">
          <i class="fa-solid fa-clipboard-question"></i>
          <span>선택한 맵에 해당하는 퀘스트가 없습니다.</span>
        </div>
      `;
      return;
    }

    this.containerEl.innerHTML = '';

    filtered.forEach(quest => {
      const isCompleted = this.completedQuestIds.has(quest.id);
      const card = document.createElement('div');
      card.className = `quest-card ${isCompleted ? 'completed' : ''}`;
      card.id = `quest-card-${quest.id}`;

      // Trader CSS class
      const traderClass = `trader-${quest.trader?.id || 'other'}`;

      // Sort objectives: Put objectives belonging to the currently selected map first
      const sortedObjectives = [...quest.objectives].sort((a, b) => {
        const aIsCurrent = a.map_id === this.selectedMapId ? 1 : 0;
        const bIsCurrent = b.map_id === this.selectedMapId ? 1 : 0;
        return bIsCurrent - aIsCurrent;
      });

      // Objectives HTML
      const objectivesHtml = sortedObjectives.map(obj => {
        const isCurrentMap = obj.map_id === this.selectedMapId;
        const hasPos = isCurrentMap && (obj.position || obj.gps);
        
        let mapBadge = '';
        if (!isCurrentMap && obj.map_name_ko) {
          mapBadge = `<span class="meta-tag" style="font-size:10px; opacity:0.8;">[${obj.map_name_ko}]</span> `;
        }

        return `
          <div class="objective-item ${hasPos ? 'has-gps' : ''}" data-obj-id="${obj.id}" style="${!isCurrentMap ? 'opacity: 0.65;' : ''}">
            <span class="objective-text">${mapBadge}${obj.description_ko}</span>
            ${hasPos ? `
              <button class="btn-locate-marker" data-obj-id="${obj.id}" title="지도에서 위치 포커스">
                <i class="fa-solid fa-crosshairs"></i> 위치
              </button>
            ` : ''}
          </div>
        `;
      }).join('');

      card.innerHTML = `
        <div class="quest-header">
          <div class="quest-header-left">
            <button class="quest-check-btn" title="${isCompleted ? '완료 취소' : '퀘스트 완료 체크'}">
              <i class="fa-${isCompleted ? 'solid fa-circle-check' : 'regular fa-circle'}"></i>
            </button>
            <div class="quest-titles">
              <span class="quest-title-ko">${quest.title_ko}</span>
              <span class="quest-title-en">${quest.title_en}</span>
            </div>
          </div>
          <span class="trader-badge ${traderClass}">${quest.trader?.name_ko || '기타'}</span>
        </div>

        <div class="quest-meta-row">
          <span class="meta-tag level"><i class="fa-solid fa-shield-halved"></i> Lv.${quest.required_level}</span>
          ${quest.exp ? `<span class="meta-tag exp"><i class="fa-solid fa-bolt"></i> +${quest.exp.toLocaleString()} EXP</span>` : ''}
          <span class="meta-tag map-tag"><i class="fa-solid fa-map-pin"></i> ${quest.objectives.length}개 목표</span>
          ${quest.wiki ? `<a href="${quest.wiki}" target="_blank" class="meta-tag" style="color: var(--accent-cyan); text-decoration: none;"><i class="fa-solid fa-arrow-up-right-from-square"></i> 위키</a>` : ''}
        </div>

        <div class="quest-objectives-list">
          ${objectivesHtml}
        </div>
      `;

      // Complete toggle event
      const checkBtn = card.querySelector('.quest-check-btn');
      checkBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.toggleQuestComplete(quest.id);
      });

      // Locate marker click
      card.querySelectorAll('.btn-locate-marker').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const objId = parseInt(btn.dataset.objId, 10);
          const obj = quest.objectives.find(o => o.id === objId);
          if (obj && (obj.position || obj.gps) && this.onLocateObjective) {
            this.onLocateObjective(quest, obj);
          }
        });
      });

      // Clicking on card auto-locates first objective with position on current map
      card.addEventListener('click', () => {
        const objWithPos = quest.objectives.find(o => o.map_id === this.selectedMapId && (o.position || o.gps));
        if (objWithPos && this.onLocateObjective) {
          this.onLocateObjective(quest, objWithPos);
        }
      });

      this.containerEl.appendChild(card);
    });
  }

  highlightQuestCard(questId) {
    const card = document.getElementById(`quest-card-${questId}`);
    if (card) {
      document.querySelectorAll('.quest-card').forEach(c => {
        c.style.borderColor = '';
        c.style.boxShadow = '';
      });
      card.style.borderColor = 'var(--accent-green)';
      card.style.boxShadow = '0 0 16px rgba(0, 230, 118, 0.4), inset 0 0 10px rgba(0, 230, 118, 0.15)';
      card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

      // Reset glow after 3 seconds
      setTimeout(() => {
        card.style.boxShadow = '';
      }, 3000);
    }
  }
}

window.QuestManager = QuestManager;
