# 중간 보고서: 타르코프 퀘스트 가이드 및 인터랙티브 맵 오버레이 시스템 구축

## 1. 개요 및 배경
본 프로젝트는 **Escape from Tarkov(타르코프)**의 퀘스트 위치 데이터와 맵 좌표 체계를 연동하여, 화면 좌측에는 **인터랙티브 맵(Interactive Map) 및 퀘스트 마커 오버레이**, 우측에는 **퀘스트 리스트 및 상세 정보 탐색기**를 제공하는 고성능 2분할 가이드 애플리케이션을 구축하는 것을 목표로 합니다.

---

## 2. 수집된 데이터 및 자산 분석
- **SVG 벡터 맵 (`primary_data/maps_svg/`)**: `Customs.svg`, `Factory.svg`, `GroundZero.svg`, `Interchange.svg`, `Labs.svg`, `Lighthouse.svg`, `Reserve.svg`, `Shoreline.svg`, `StreetsOfTarkov.svg`, `Woods.svg` 등 11개 핵심 맵의 공식 고품질 SVG 파일 수집 완료 (층/레이어별 분리 지원).
- **2D 고화질 래스터 맵 (`primary_data/maps_2d/`)**: 세관, 공장, 그라운드 제로 등 10개 맵 이미지 다운로드 완료.
- **퀘스트 및 GPS 좌표 데이터 (`primary_data/tracker_quests_json.json`, `secondary_data/processed_quests.json`)**: 250개 전체 퀘스트 및 540개 목표, 그 중 197개에 달하는 정밀 좌표(`leftPercent`, `topPercent`, `floor`) 정보 파싱 및 한국어 번역 매핑 완료.
- **인터랙티브 마커 아이콘 (`primary_data/interactive_icons/`)**: 퀘스트 아이템, 퀘스트 목표, PMC/Scav 탈출구, 스폰 지점 등 공식 아이콘 에셋 구비 완료.

---

## 3. 핵심 아키텍처 설계
1. **좌측 패널: 인터랙티브 맵 뷰어**
   - **엔진**: 고성능 반응형 SVG/Canvas 인터랙티브 맵 엔진 (Panzoom / Transform 기반의 부드러운 드래그, 휠 확대/축소, 핀치 줌 지원).
   - **맵 및 층(Floor) 전환**: Customs, Factory, Reserve, Streets 등 다층 구조 맵 지원 (Basement, Ground Level, 1F, 2F 등 층별 레이어 필터링).
   - **오버레이 마커 렌더링**: 퀘스트 목표 위치에 애니메이션 펄스 핀(Pin), 마커 호버 시 툴팁 표시, 클릭 시 퀘스트 동기화.
   - **맵 부가 기능**: 전체화면, 줌 초기화, 마커 가시성 토글(퀘스트 마커, 탈출구 등).

2. **우측 패널: 퀘스트 네비게이터 & 상세 리스트**
   - **필터링 & 검색**: 맵별(Customs, Woods 등), 상인별(Prapor, Therapist, Skier, Peacekeeper 등), 검색어(한글/영문) 실시간 필터.
   - **퀘스트 진행도 트래커**: 완료 퀘스트 체크박스(로컬 스토리지에 자동 저장되어 진행 상태 영구 보관).
   - **목표(Objectives) 목록 & 인터랙션**: 퀘스트 또는 목표 클릭 시, 좌측 맵이 해당 위치로 부드럽게 이동(Pan)하고 목표 마커를 포커스 펄스 효과로 강조.

---

## 4. 관련 스크립트 및 산출물
- [01_fetch_tarkov_data.py](file:///c:/Users/ky001/Desktop/11/code/tarkov%20quest2/scripts/01_fetch_tarkov_data.py): API 및 데이터셋 구조 탐색
- [02_download_svg_and_metadata.py](file:///c:/Users/ky001/Desktop/11/code/tarkov%20quest2/scripts/02_download_svg_and_metadata.py): SVG 맵 및 메타데이터 일괄 다운로드
- [09_download_2d_maps_and_icons.py](file:///c:/Users/ky001/Desktop/11/code/tarkov%20quest2/scripts/09_download_2d_maps_and_icons.py): 2D 래스터 맵 및 마커 아이콘 다운로드
- [10_process_quest_and_map_data.py](file:///c:/Users/ky001/Desktop/11/code/tarkov%20quest2/scripts/10_process_quest_and_map_data.py): 퀘스트/맵/상인 데이터 정제 및 한국어화
- 정제 데이터: [processed_quests.json](file:///c:/Users/ky001/Desktop/11/code/tarkov%20quest2/secondary_data/processed_quests.json)
