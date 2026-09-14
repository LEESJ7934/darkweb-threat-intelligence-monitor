# ISMS-P 모의진단 Evidence Index

| 통제 | Evidence | 무엇을 증명하는가 | 증명하지 못하는 것 |
|---|---|---|---|
| 1.1.4 | `docs/isms_p/00_scope.md` | 프로젝트 진단 범위·제외범위 | 실제 인증범위 승인 |
| 1.2.1 | `docs/isms_p/01_asset_inventory.md` | 자산 식별·상대 중요도 | 실제 조직 CMDB/BIA |
| 1.2.2 | `docs/isms_p/02_data_flow.md`, `docs/architecture.md` | 데이터 이동·trust boundary | 전체 조직 네트워크 DFD |
| 1.2.3 | `docs/isms_p/04_risk_register.md` | 별도 정보보호 위험평가 | 실제 경영진 위험수용 |
| 1.2.4 | `docs/isms_p/05_risk_treatment_plan.md` | 위험-처리-잔여위험 연결 | 예산/공식 일정 승인 |
| 2.5.1/2.5.5 | `governance/django_controls.py`, `views.py`, Django governance tests | Analyst/Admin 최소 권한분리 | MFA/SSO/정기 account recertification |
| 2.9.4 | `governance/audit.py`, `logs/audit.jsonl`(runtime) | allowlisted audit, pseudonym, rotation | 중앙수집/변조방지 |
| 2.9.5 | `governance/audit_review.py`, `scripts/review_audit.py`, `governance_review.html`, tests | 주기적 aggregate review 기준·도구 | 실제 조직의 월간 승인 기록 |
| 2.10.1 | `elk/operations.md`, `scripts/check_elk_pipeline.py` | ELK 운영·검증 절차 | 조직 변경관리 승인체계 |
| 2.11.1 | `governance/incident_response.md` | 프로젝트 대응 절차 | 실제 연락망/법적 신고 판단 |
| 2.11.3 | `alert/service.py`, `alert/risk.py`, `elk/` | 위협 metadata 모니터링·alert | 전체 인프라 SIEM coverage |
| 3.4.1 | `governance/retention.py`, `scripts/apply_retention.py` | safe retention/dry-run | 법적 보유기간 적정성 |

## 테스트 증적

- `tests/test_governance.py`: audit/retention/redaction/source lifecycle 및 Audit Review 단위 테스트
- `DjangoProject/mongoDbConnect/tests_governance.py`: 로그인·CSRF·RBAC·Security Admin Audit Review 테스트
- 기존 최종 E2E 로그/스크린샷은 실제 Mongo/Telegram/ELK/Django 통합 증적으로 별도 보관
