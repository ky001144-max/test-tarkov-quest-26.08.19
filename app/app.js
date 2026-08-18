/**
 * Main Application Orchestrator for Tarkov Quest Guide
 */
document.addEventListener('DOMContentLoaded', async () => {
  try {
    // 1. Fetch JSON datasets
    const [mapsRes, questsRes, tradersRes] = await Promise.all([
      fetch('data/maps.json'),
      fetch('data/quests.json'),
      fetch('data/traders.json')
    ]);

    const maps = await mapsRes.json();
    const quests = await questsRes.json();
    const traders = await tradersRes.json();

    console.log(`Loaded ${maps.length} maps, ${quests.length} quests, ${traders.length} traders.`);

    // 2. Populate Map Selector
    const mapSelectEl = document.getElementById('map-select');
    maps.forEach(m => {
      const opt = document.createElement('option');
      opt.value = m.id;
      opt.textContent = `${m.name_ko} (${m.name_en})`;
      if (m.id === 'customs') opt.selected = true;
      mapSelectEl.appendChild(opt);
    });

    // 3. Populate Trader Tabs
    const traderTabsEl = document.getElementById('trader-tabs');
    traders.forEach(t => {
      if (t.id === 'unknown') return;
      const btn = document.createElement('button');
      btn.className = 'trader-tab';
      btn.dataset.trader = t.id;
      btn.innerHTML = `<span class="tab-badge">${t.name_ko}</span>`;
      traderTabsEl.appendChild(btn);
    });

    // 4. Initialize Leaflet Map Viewer
    const mapViewer = new MapViewer({
      containerId: 'map-leaflet-container',
      onMarkerClick: (quest, obj) => {
        questManager.highlightQuestCard(quest.id);
      }
    });

    // 5. Initialize Quest Manager
    const questManager = new QuestManager({
      containerId: 'quest-list-container',
      onLocateObjective: (quest, obj) => {
        if (!obj.position) return;
        
        if (obj.map_id !== mapViewer.currentMapMeta?.id) {
          // If objective is on another map, switch map first
          const targetMap = maps.find(m => m.id === obj.map_id);
          if (targetMap) {
            mapSelectEl.value = targetMap.id;
            mapViewer.loadMap(targetMap, quests).then(() => {
              questManager.setMap(targetMap.id);
              mapViewer.focusCoordinate(obj.position, obj.id);
            });
            return;
          }
        }
        // Focus coordinate on current map
        mapViewer.focusCoordinate(obj.position, obj.id);
      }
    });

    // 6. Bind Map Change
    mapSelectEl.addEventListener('change', (e) => {
      const mapId = e.target.value;
      const selectedMap = maps.find(m => m.id === mapId);
      if (selectedMap) {
        mapViewer.loadMap(selectedMap, quests);
        questManager.setMap(mapId);
      }
    });

    // 7. Bind Trader Tabs Click
    traderTabsEl.addEventListener('click', (e) => {
      const tab = e.target.closest('.trader-tab');
      if (!tab) return;
      traderTabsEl.querySelectorAll('.trader-tab').forEach(b => b.classList.remove('active'));
      tab.classList.add('active');
      const traderId = tab.dataset.trader;
      questManager.setTrader(traderId);
    });

    // 8. Initial Load: Customs
    const initialMap = maps.find(m => m.id === 'customs') || maps[0];
    questManager.setQuests(quests);
    questManager.setMap(initialMap.id);
    await mapViewer.loadMap(initialMap, quests);

  } catch (err) {
    console.error('Failed to initialize Tarkov Quest Guide application:', err);
  }
});
