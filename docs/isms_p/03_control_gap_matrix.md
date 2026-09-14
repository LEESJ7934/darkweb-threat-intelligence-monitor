# ISMS-P 통제항목 모의 GAP Matrix

> 실제 인증심사 결과가 아니라 프로젝트 범위의 자체진단입니다. 101개 전체 항목 중 시스템과 직접 연관된 21개를 선별했습니다.

| 항목 | 항목명 | 판정 | 현재 상태/증적 | GAP | 개선 방향 |
|---|---|---|---|---|---|
| 1.1.4 | 범위 설정 | PARTIAL | architecture/project story 존재 | 인증범위 형식의 문서 부족 | `00_scope.md` 작성 |
| 1.2.1 | 정보자산 식별 | GAP→PARTIAL | 기능별 파일은 있으나 자산대장 없음 | 중요도·데이터유형 연결 부족 | `01_asset_inventory.md` 작성 |
| 1.2.2 | 현황 및 흐름분석 | PARTIAL | architecture 존재 | trust boundary와 데이터 이동 분석 부족 | `02_data_flow.md` 작성 |
| 1.2.3 | 위험 평가 | GAP→PARTIAL | `alert/risk.py`는 사건 위험도 분류 | 조직 정보보호 Risk Register 부재 | 별도 5x5 위험평가 작성 |
| 1.2.4 | 보호대책 선정 | GAP→PARTIAL | 개별 통제는 존재 | 위험-대책-담당-잔여위험 연결 부재 | treatment plan 작성 |
| 1.3.1 | 보호대책 구현 | PARTIAL | redaction/auth/retention/audit/ELK | 위험평가와 구현 근거 연결 약함 | evidence index 연결 |
| 1.3.3 | 운영현황 관리 | PARTIAL | runtime/governance checker | 정기 수행 주기·책임자 기록 부재 | 운영 checklist/검토 기록 유지 |
| 1.4.2 | 관리체계 점검 | GAP | 기능 테스트는 수행 | 관리체계 관점 정기 자체점검 부재 | 본 GAP matrix를 정기 검토 baseline으로 사용 |
| 1.4.3 | 관리체계 개선 | PARTIAL | Day별 개선·회귀 기록 | corrective action tracking 형식 부족 | treatment 상태/잔여위험 기록 |
| 2.5.1 | 사용자 계정 관리 | PARTIAL | Django auth | 일반 사용자 간 역할구분 부족 | Analyst/Security Admin 최소 RBAC |
| 2.5.3 | 사용자 인증 | PARTIAL | 로그인/CSRF/secure-cookie opt-in | MFA/login throttling 미구현 | 운영 도입 시 강화 필요 |
| 2.5.5 | 특수 계정 및 권한관리 | GAP→PARTIAL | staff account 사용 가능 | 관리자 용도 명시·화면 분리 부족 | Security Admin-only audit review |
| 2.5.6 | 접근권한 검토 | GAP | Django 계정 존재 | 권한 부여·변경 정기검토 절차 없음 | 향후 account/permission review 절차 |
| 2.9.3 | 백업 및 복구관리 | GAP | destructive protection 존재 | 실제 backup/restore 시험 증적 없음 | 정기 backup/restore test 필요 |
| 2.9.4 | 로그 및 접속기록 관리 | PARTIAL | JSON audit, hash, rotation | 중앙수집·변조방지 미구현 | 운영환경 central/WORM sink 검토 |
| 2.9.5 | 로그 및 접속기록 점검 | GAP→PARTIAL | audit 생성만 존재 | 정기 review 기준/도구 부재 | 30일 aggregate Audit Review 추가 |
| 2.9.6 | 시간 동기화 | PARTIAL | UTC aware timestamp 사용 | NTP 운영증적 없음 | 운영 배포 시 time sync 점검 |
| 2.10.1 | 보안시스템 운영 | PARTIAL | ELK 운영절차·검증 도구 | 정책변경 승인/담당체계 부족 | 운영 변경관리 필요 |
| 2.11.1 | 사고 예방 및 대응체계 구축 | PARTIAL | `incident_response.md` | 실제 조직 연락망/훈련 없음 | tabletop 및 연락체계 필요 |
| 2.11.3 | 이상행위 분석 및 모니터링 | PARTIAL | risk alert/ELK | 인프라 전체 이상행위 모니터링 아님 | 범위 명시, 운영 SIEM 연계 고려 |
| 3.4.1 | 개인정보 파기 | CONDITIONAL/PARTIAL | retention dry-run/apply safety | 법적 보유기간·legal hold 판단 아님 | 적용성/법정기간 별도 검토 |

## 이번 구현에서 닫는 핵심 GAP

1. **2.5.1 / 2.5.5**: 일반 Analyst와 `is_staff=True` Security Admin의 governance 기능 접근을 분리합니다.
2. **2.9.5**: `audit.jsonl` 및 rotation 파일을 최근 30일 기준으로 읽어 `login_failure`, 접근거부, error, retention error, malformed record를 aggregate review합니다.

나머지 GAP은 구현되지 않았다고 명시적으로 남겨 과대평가를 피합니다.
