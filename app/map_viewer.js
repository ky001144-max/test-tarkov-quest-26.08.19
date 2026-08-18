/**
 * MapViewer - Official Tarkov.dev Leaflet Map Engine
 * Replicates exact CRS, Affine Transformation, and 3D Marker Projection
 */
class MapViewer {
  constructor(options) {
    this.containerId = options.containerId || 'map-leaflet-container';
    this.mapScaleTextEl = document.getElementById('map-scale-text');
    this.markerNumEl = document.getElementById('marker-num');
    this.mapNameTextEl = document.getElementById('map-name-text');
    this.floorButtonsEl = document.getElementById('floor-buttons');

    // Leaflet State
    this.map = null;
    this.mapOverlay = null;
    this.markersLayer = null;
    this.currentMapMeta = null;
    this.currentFloor = 'Ground_Level';
    this.markersVisible = true;
    this.markerEntries = [];

    // Callbacks
    this.onMarkerClick = options.onMarkerClick || null;

    this.initControls();
  }

  initControls() {
    // Floating Controls
    document.getElementById('btn-zoom-in')?.addEventListener('click', () => {
      if (this.map) this.map.zoomIn();
    });
    document.getElementById('btn-zoom-out')?.addEventListener('click', () => {
      if (this.map) this.map.zoomOut();
    });
    document.getElementById('btn-zoom-reset')?.addEventListener('click', () => {
      this.resetView();
    });

    // Toggle Markers
    const toggleBtn = document.getElementById('btn-toggle-markers');
    toggleBtn?.addEventListener('click', () => {
      this.markersVisible = !this.markersVisible;
      if (this.markersLayer) {
        if (this.markersVisible) {
          this.map.addLayer(this.markersLayer);
        } else {
          this.map.removeLayer(this.markersLayer);
        }
      }
      toggleBtn.classList.toggle('active', this.markersVisible);
    });
  }

  /**
   * Official tarkov.dev Coordinate Reference System (CRS) generator
   */
  getCRS(mapData) {
    let scaleX = 1;
    let scaleY = 1;
    let marginX = 0;
    let marginY = 0;

    if (mapData && mapData.transform) {
      scaleX = mapData.transform[0];
      scaleY = mapData.transform[2] * -1;
      marginX = mapData.transform[1];
      marginY = mapData.transform[3];
    }

    return L.extend({}, L.CRS.Simple, {
      transformation: new L.Transformation(scaleX, marginX, scaleY, marginY),
      projection: L.extend({}, L.Projection.LonLat, {
        project: (latLng) => {
          return L.Projection.LonLat.project(this.applyRotation(latLng, mapData.coordinateRotation));
        },
        unproject: (point) => {
          return this.applyRotation(L.Projection.LonLat.unproject(point), mapData.coordinateRotation * -1);
        },
      }),
    });
  }

  applyRotation(latLng, rotation) {
    if (!latLng.lng && !latLng.lat) {
      return L.latLng(0, 0);
    }
    if (!rotation) {
      return latLng;
    }

    const angleInRadians = (rotation * Math.PI) / 180;
    const cosAngle = Math.cos(angleInRadians);
    const sinAngle = Math.sin(angleInRadians);

    const { lng: x, lat: y } = latLng;
    const rotatedX = x * cosAngle - y * sinAngle;
    const rotatedY = x * sinAngle + y * cosAngle;
    return L.latLng(rotatedY, rotatedX);
  }

  pos(position) {
    return [position.z, position.x];
  }

  /**
   * Load Map using official Tarkov.dev Leaflet configuration
   */
  async loadMap(mapMeta, quests = []) {
    this.currentMapMeta = mapMeta;

    if (this.mapNameTextEl) {
      this.mapNameTextEl.textContent = `${mapMeta.name_ko} (${mapMeta.name_en})`;
    }

    // Clean up existing map instance
    if (this.map) {
      this.map.remove();
      this.map = null;
    }

    const crs = this.getCRS(mapMeta);

    // Initialize Leaflet Map
    this.map = L.map(this.containerId, {
      crs: crs,
      zoomControl: false,
      attributionControl: false,
      minZoom: -4,
      maxZoom: 5,
      zoomSnap: 0.1,
      wheelPxPerZoomLevel: 100
    });

    this.markersLayer = L.layerGroup().addTo(this.map);

    // Calculate map bounds in Leaflet coordinate space
    const bounds = [
      this.pos({ x: mapMeta.bounds[0][0], z: mapMeta.bounds[0][1] }),
      this.pos({ x: mapMeta.bounds[1][0], z: mapMeta.bounds[1][1] })
    ];

    // Load official SVG Map as ImageOverlay
    this.mapOverlay = L.imageOverlay(`maps/${mapMeta.svg}`, bounds).addTo(this.map);

    this.map.fitBounds(bounds, { animate: false, padding: [20, 20] });

    // Update scale status on zoom
    this.map.on('zoomend', () => {
      if (this.mapScaleTextEl) {
        this.mapScaleTextEl.textContent = `줌 레벨: ${this.map.getZoom().toFixed(1)}`;
      }
    });

    this.renderMarkers(quests);
  }

  resetView() {
    if (this.map && this.currentMapMeta) {
      const bounds = [
        this.pos({ x: this.currentMapMeta.bounds[0][0], z: this.currentMapMeta.bounds[0][1] }),
        this.pos({ x: this.currentMapMeta.bounds[1][0], z: this.currentMapMeta.bounds[1][1] })
      ];
      this.map.fitBounds(bounds, { animate: true, padding: [20, 20] });
    }
  }

  /**
   * Render Quest Markers using official position coordinates
   */
  renderMarkers(quests) {
    if (!this.markersLayer) return;
    this.markersLayer.clearLayers();
    this.markerEntries = [];

    let markerCount = 0;

    quests.forEach(quest => {
      quest.objectives.forEach(obj => {
        if (obj.map_id === this.currentMapMeta.id && obj.position) {
          markerCount++;

          const markerPos = this.pos(obj.position);

          // Icon Type
          let iconClass = 'fa-solid fa-location-dot';
          if (obj.type === 'pickup') iconClass = 'fa-solid fa-box';
          else if (obj.type === 'place' || obj.type === 'mark') iconClass = 'fa-solid fa-crosshairs';
          else if (obj.type === 'locate') iconClass = 'fa-solid fa-eye';
          else if (obj.type === 'key') iconClass = 'fa-solid fa-key';

          const isCluster = Boolean(obj.is_cluster && obj.spawn_count > 1);
          const clusterBadge = isCluster ? `<div class="leaflet-marker-badge" style="position: absolute; top: -6px; right: -8px; background: #e67e22; color: #fff; border-radius: 10px; font-size: 10px; font-weight: bold; padding: 1px 5px; border: 1.5px solid #111; box-shadow: 0 2px 4px rgba(0,0,0,0.5);">${obj.spawn_count}</div>` : '';

          const customIcon = L.divIcon({
            className: 'leaflet-quest-marker-wrapper',
            html: `
              <div class="leaflet-quest-marker ${isCluster ? 'is-cluster-marker' : ''}" id="marker-obj-${obj.id}" style="position: relative;">
                <div class="leaflet-marker-inner" style="${isCluster ? 'background: linear-gradient(135deg, #e67e22, #d35400); border-color: #f39c12;' : ''}">
                  <i class="${iconClass}"></i>
                </div>
                ${clusterBadge}
                <div class="leaflet-marker-tip" style="${isCluster ? 'border-top-color: #d35400;' : ''}"></div>
              </div>
            `,
            iconSize: [28, 36],
            iconAnchor: [14, 36],
            popupAnchor: [0, -36]
          });

          const marker = L.marker(markerPos, { icon: customIcon });

          const clusterHeader = isCluster ? `
            <div style="background: rgba(230, 126, 34, 0.2); border-left: 3px solid #e67e22; padding: 4px 8px; border-radius: 4px; margin-bottom: 6px; font-size: 11px; color: #f39c12; font-weight: bold;">
              <i class="fa-solid fa-layer-group"></i> 다중 스폰 구역 (총 ${obj.spawn_count}개 후보지 중심점)
            </div>
          ` : '';

          const hintHtml = obj.hint ? `<div style="color: var(--accent-cyan); font-weight: 600; margin-top: 4px; font-size: 11px;"><i class="fa-solid fa-compass"></i> 위치 안내: ${obj.hint}</div>` : '';

          const popupContent = `
            <div style="min-width: 220px;">
              ${clusterHeader}
              <div style="font-weight: 700; color: var(--accent-gold); font-size: 13px;">${quest.title_ko}</div>
              <div style="font-size: 11px; color: #8fa0b3; margin-bottom: 4px;">${quest.title_en} | ${quest.trader.name_ko}</div>
              <div style="font-size: 12px; color: #fff; margin-top: 4px;">${obj.description_ko}</div>
              ${hintHtml}
            </div>
          `;

          marker.bindPopup(popupContent);

          marker.on('click', () => {
            if (this.onMarkerClick) {
              this.onMarkerClick(quest, obj);
            }
          });

          this.markersLayer.addLayer(marker);

          this.markerEntries.push({
            quest,
            obj,
            marker,
            position: obj.position
          });
        }
      });
    });

    if (this.markerNumEl) {
      this.markerNumEl.textContent = markerCount;
    }
  }

  /**
   * Smoothly focus camera on marker position and trigger highlight
   */
  focusCoordinate(position, objectiveId = null) {
    if (!this.map || !position) return;

    const latLng = this.pos(position);
    this.map.flyTo(latLng, Math.max(this.map.getZoom(), 1.5), {
      animate: true,
      duration: 0.6
    });

    // Find and open popup
    const entry = this.markerEntries.find(e => e.obj.id === objectiveId || (e.position.x === position.x && e.position.z === position.z));
    if (entry && entry.marker) {
      setTimeout(() => {
        entry.marker.openPopup();
      }, 650);
    }
  }
}

window.MapViewer = MapViewer;
