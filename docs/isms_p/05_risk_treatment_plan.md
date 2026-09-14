# 위험 처리 계획

| Risk | 처리전략 | 구현/계획 | 담당 역할 가정 | 상태 | 잔여위험 |
|---|---|---|---|---|---|
| R-01 | Mitigate | Analyst는 조회, Security Admin만 Audit Review | Security Admin | IMPLEMENTED | LOW~MEDIUM: Django staff 자체 관리 필요 |
| R-02 | Mitigate | 운영 배포 시 MFA/login throttling | Security Admin | OPEN | MEDIUM |
| R-03 | Mitigate | 중앙/WORM 로그 sink 또는 무결성 보호 | Security Admin | OPEN | HIGH |
| R-04 | Mitigate | 30일 read-only aggregate Audit Review | Security Admin | IMPLEMENTED | MEDIUM: 자동 알림/승인 workflow 없음 |
| R-05 | Mitigate | dry-run 기본, apply+DB명 이중확인 유지 | Operator | IMPLEMENTED | MEDIUM: 잘못된 retention 정책 가능 |
| R-06 | Mitigate | backup + restore test 절차 | Operator | OPEN | HIGH |
| R-07 | Mitigate/Accept | ACTIVE lifecycle, fixture/parser regression, 수동 검토 | Analyst | IMPLEMENTED | MEDIUM |
| R-08 | Mitigate | `.env`, secret scan, redaction, 실제 키회전 | Security Admin | PARTIAL | MEDIUM |
| R-09 | Mitigate | projection 최소화, 운영 network ACL | Security Admin | PARTIAL | MEDIUM |
| R-10 | Mitigate | material change threshold, dedupe/retry | Analyst | IMPLEMENTED | LOW~MEDIUM |
| R-11 | Mitigate | 연락망·tabletop·법무 escalation | Security Admin | OPEN | HIGH |
| R-12 | Mitigate/Accept | metadata 최소화/redaction, 필요 시 추가 DLP | Analyst | PARTIAL | MEDIUM |

## 우선순위

1. R-01/R-04: 프로젝트 코드에서 즉시 개선 가능한 통제
2. R-03/R-06/R-11: 운영환경·조직 절차가 필요한 High risk
3. R-02/R-08/R-09/R-12: 실제 배포 전 hardening 필요
