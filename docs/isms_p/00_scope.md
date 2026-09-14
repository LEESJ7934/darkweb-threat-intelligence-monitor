# ISMS-P 통제항목 기반 모의진단 범위

> 이 문서는 교육·포트폴리오 목적의 **모의 보안진단 범위 정의서**입니다. 실제 ISMS-P 인증, 법률 준수 판정 또는 인증심사 수행을 의미하지 않습니다.

## 1. 진단 목적

다크웹 위협정보 모니터링 시스템의 기존 보안·개인정보 보호 통제를 ISMS-P 관점에서 구조화하고, 자산·데이터 흐름·위험·통제·증적을 연결하여 GAP을 식별하고 개선 우선순위를 정합니다.

## 2. 진단 대상

- Darkweb source registry 및 Selenium/Tor crawler
- parser/normalizer와 MongoDB 저장 계층
- `leaked_data`, `leak_history`, `alert_log`
- risk classification 및 Telegram alert
- Django analyst dashboard 및 인증 계정
- governance audit / retention / runtime controls
- Monstache → Elasticsearch → Kibana 분석 파이프라인
- `.env` 기반 runtime secret/configuration 관리
- Docker/로컬 실행환경의 프로젝트 수준 구성

## 3. 제외 범위

- 실제 피해기업·제3자 시스템의 내부 시스템
- 유출 파일 원문 다운로드, 계정·비밀번호 사용, 침투행위
- 조직 전체 인사·물리보안·법무·경영진 승인체계
- 실제 법정 신고·통지 의무에 대한 최종 법률판단
- 실제 인증기관의 ISMS-P 인증심사

## 4. 진단 기준과 적용 방식

현재 ISMS-P 체계의 101개 인증기준 전체를 적합 판정하지 않고, 본 시스템과 직접 연결되는 21개 항목을 집중 점검합니다. 판정은 `GOOD`, `PARTIAL`, `GAP`, `CONDITIONAL`로 구분하며 코드 존재만으로 운영 통제가 완성되었다고 보지 않습니다.

- `GOOD`: 프로젝트 범위에서 구현·테스트·증적이 비교적 명확함
- `PARTIAL`: 일부 구현은 있으나 운영절차·역할·증적 등 보완 필요
- `GAP`: 현재 증거로 요구사항 충족을 설명하기 어려움
- `CONDITIONAL`: 개인정보 처리 여부·법적 적용성 등 별도 판단이 필요한 항목

## 5. 역할 가정

- **Analyst**: 위협정보 dashboard 및 사건 상세 조회
- **Security Admin**: Analyst 권한 + governance audit review
- 운영자·개발자·법무·경영진 역할은 문서상 가정만 하며 실제 조직 통제로 주장하지 않습니다.

## 6. 핵심 산출물

`01_asset_inventory.md` → `02_data_flow.md` → `03_control_gap_matrix.md` → `04_risk_register.md` → `05_risk_treatment_plan.md` → `06_evidence_index.md` → `07_final_assessment.md`
