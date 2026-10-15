# 다크웹 위협 인텔리전스 모니터
**Darkweb Threat Intelligence Monitor**

다크웹 유출 게시글의 **필요한 메타데이터만 수집**하고, 동일 사건의 재관찰과 내용 변경을 구분해 **알림·조회·분석·운영 보안 통제**로 연결한 프로젝트입니다. 게시글의 유출 주장은 검증된 침해 사실과 구분하며, 유출 원문 파일이나 계정·비밀번호를 수집·재사용하지 않습니다.

## 1. 프로젝트 개요

초기 수집·저장·조회 중심 구조에서 다음 과제를 식별했습니다.

- 같은 게시글이 다시 수집될 때 **중복과 재관찰**을 구분하기 어려움
- 게시글 내용이 바뀌면 **변경 전후 근거**를 추적하기 어려움
- 중요하지 않은 변경까지 알림으로 보내 **알림 피로**가 발생할 수 있음
- 데이터 조회·외부전송 과정에서 **불필요한 정보 노출** 가능성
- 접근권한·감사로그·보유기간 등 **운영 보안 통제**의 부족

공동 프로젝트의 수집·저장·조회·알림 기반을 개선하고, 이후 프로젝트 범위에서 운영 통제 및 ISMS-P 자체진단 산출물을 보완했습니다. 세부 수행 이력은 [프로젝트 설명](docs/project_story.md)에 정리했습니다.

## 2. 전체 데이터 흐름

```text
다크웹 게시글
  → Selenium / Tor 수집
  → Parser / Normalizer 및 메타데이터 최소화
  → MongoDB 저장 (현재 상태 / 변경 이력)
  → 사건 식별·변경 감지 및 위험도 분류
  → Telegram 알림
  → Django 조회 / Elasticsearch·Kibana 분석
  → 접근통제·감사·보유기간 등 운영 통제
```

## 3. 핵심 기능과 정보보호 관점

| 영역 | 주요 구현·설계 | 정보보호 관점 |
|---|---|---|
| 수집·정규화 | Selenium/Tor, 필드 allowlist, redaction | 불필요한 수집·민감정보 노출 제한 |
| 사건 식별 | `event_key`, `content_fingerprint`, `leak_history` | 중복 식별, 변경 이력 및 추적 근거 |
| 알림 | NEW/UPDATED 구분, 위험도 분류, Telegram | 주요 이벤트 선별, 전송 상태 확인 |
| 조회 | Django 로그인, Analyst/Security Admin 역할 분리 | 비인가 접근 및 관리자 권한 제한 |
| 분석 | MongoDB → Monstache → Elasticsearch/Kibana | 분석용 필드 최소화, 조회 범위 관리 |
| 운영 | 감사로그·30일 검토 도구, retention DRY RUN | 로그 점검, 보유기간 및 안전한 삭제 검토 |

- `leaked_data`: 사건 현재 상태 / `leak_history`: 변경 이력 / `alert_log`: 알림·전송 상태
- 현재 자동 스케줄 대상은 **Bitlock 1개**입니다. 나머지 source parser는 오프라인 재현·테스트용으로 보관하며, 실제 위협 조직의 활동 종료를 뜻하지 않습니다.
- 프로젝트의 위험도 분류는 **수집 게시글의 우선 검토 수준**을 의미하며 실제 침해나 피해를 확정하지 않습니다.
- 상세 설계·트레이드오프는 [architecture.md](docs/architecture.md), 기능별 통제·증거·한계는 [control_matrix.md](governance/control_matrix.md)에 있습니다.

## 4. ISMS-P 통제항목 기반 자체 모의진단

시스템 구현 이후, **Scope → Asset → Data Flow → GAP → Risk → Treatment → Evidence → Final Assessment** 순서로 자체진단을 정리했습니다.

- **진단 범위:** 프로젝트에서 코드·설정·테스트 등으로 확인 가능한 **21개 관련 통제항목** 선별. 조직의 인사·물리보안 등은 제외
- **위험평가:** 별도 정보보호 위험 시나리오 **12개**를 등록하고 발생 가능성×영향도로 우선순위 평가
- **대표 GAP ① 접근권한:** 일반 Analyst와 Security Admin의 governance 기능 권한 구분 부족 → 최소 역할 분리
- **대표 GAP ② 로그 점검:** 감사로그는 존재하지만 정기 검토 기준·도구 부족 → 최근 30일 집계형 Audit Review 추가
- **재평가:** 개선 기능이 있더라도 MFA·정기 권한 검토·조직 승인 기록 등 미구현 요소가 있어 관련 항목을 **PARTIAL**로 유지
- **증적 관리:** 코드·설정·테스트 결과를 통제항목에 연결하고, **증명할 수 없는 영역**도 명시

| 순서 | 산출물 | 핵심 내용 |
|---|---|---|
| 00 | [Scope](docs/isms_p/00_scope.md) | 진단 대상과 제외 범위 |
| 01 | [Asset Inventory](docs/isms_p/01_asset_inventory.md) | 15개 정보자산·중요도 |
| 02 | [Data Flow](docs/isms_p/02_data_flow.md) | 데이터 이동·신뢰 경계 |
| 03 | [GAP Matrix](docs/isms_p/03_control_gap_matrix.md) | 관련 21개 통제의 현재 상태·GAP |
| 04 | [Risk Register](docs/isms_p/04_risk_register.md) | 12개 시스템 운영 위험 |
| 05 | [Treatment Plan](docs/isms_p/05_risk_treatment_plan.md) | 위험 처리·잔여위험 |
| 06 | [Evidence Index](docs/isms_p/06_evidence_index.md) | 근거자료와 증명 한계 |
| 07 | [Final Assessment](docs/isms_p/07_final_assessment.md) | 개선 후 재평가·남은 GAP |

## 5. 검증과 한계

기존 프로젝트 문서에 기록된 검증 결과에는 **Django 테스트 81 PASS**, 설정·비밀정보 검사 PASS, MongoDB→ELK 동기화와 Django 로그인 흐름의 E2E PASS가 포함됩니다. 이 표기는 **기존 검증 기록**이며 이 문서 정리 과정에서 새로 실행한 결과는 아닙니다. 이전 Django 77 PASS 기록과의 시점 구분은 [검증 문서](docs/validation.md)에 명시했습니다.

중요한 한계:
- 모든 소스의 실시간 가용성, 향후 selector 동작, 완전한 개인정보·비밀정보 탐지를 보장하지 않습니다.
- MongoDB/ELK 정기 백업·복원 시험, 중앙 감사로그 무결성, MFA·정기 권한 검토, 조직 차원의 사고대응 훈련은 보완 과제입니다.
- 보유기간 기본값(`leaked_data`·`leak_history` 각 365일, `alert_log` 180일)은 **프로젝트 설정값**이며 법정 보유기간이 아닙니다.
- 프로젝트는 유출 원문 다운로드·자격증명 재사용·피해 시스템 접근·CAPTCHA 우회를 수행하지 않습니다.

## 6. 실행·기술 참고

주요 구성: Python 3.12, Django 5.2, MongoDB, Selenium, Tor SOCKS proxy, Docker Desktop, Elasticsearch 8.15.3, Kibana 8.15.3, Monstache 6.7.7, Telegram Bot API.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python scripts/check_secrets.py
python scripts/check_runtime_config.py
```

실제 인증정보는 `.env`에만 저장하고 Git에 커밋하지 않습니다. 정식 Django 진입점은 `DjangoProject/manage.py`입니다.

- [검증 시나리오와 기록](docs/validation.md)
- [ELK 구성 및 재현 절차](elk/operations.md)
- [Kibana 대시보드 명세](elk/kibana_dashboard_spec.md)
- [데이터 처리·운영 정책](governance/data_handling.md)
- [프로젝트 사고 대응 절차](governance/incident_response.md)
- [기술 구조와 설계 판단](docs/architecture.md)
