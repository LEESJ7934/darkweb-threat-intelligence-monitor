# 정보보호 Risk Register

## 평가방법

- Likelihood: 1(희박) ~ 5(매우 높음)
- Impact: 1(낮음) ~ 5(매우 큼)
- Risk Score = Likelihood × Impact
- 1~4 LOW / 5~9 MEDIUM / 10~15 HIGH / 16~25 CRITICAL

이는 프로젝트용 단순 방법론이며 실제 조직의 위험수용 기준을 대신하지 않습니다.

| ID | 자산 | 위험 시나리오 | L | I | 기존 위험 | 현재 통제 | 처리 |
|---|---|---|---:|---:|---:|---|---|
| R-01 | Django Dashboard | 모든 인증사용자가 동일 governance 권한 사용 | 3 | 4 | 12 HIGH | login required | **완화: Analyst/Admin 분리** |
| R-02 | Django Auth | brute-force/MFA 부재로 계정 탈취 | 2 | 4 | 8 MEDIUM | Django auth, CSRF | OPEN: 운영 시 MFA/throttling |
| R-03 | Audit Log | 로컬 파일 변조·삭제로 추적성 저하 | 3 | 4 | 12 HIGH | hash identifier, rotation | OPEN: central/WORM sink |
| R-04 | Audit Log | 기록은 있으나 정기 검토하지 않아 이상징후 누락 | 3 | 4 | 12 HIGH | audit generation | **완화: Audit Review** |
| R-05 | MongoDB | retention 오설정·잘못된 대량삭제 | 2 | 5 | 10 HIGH | dry-run, DB double confirmation | 유지/검토 |
| R-06 | MongoDB/ES | backup/restore 미검증으로 장애 시 복구 실패 | 3 | 5 | 15 HIGH | destructive protection | OPEN: restore exercise |
| R-07 | Crawler | source 구조 변경을 공격 종료/정상으로 오판 | 4 | 3 | 12 HIGH | source lifecycle, fixture tests | 유지/수동 검토 |
| R-08 | `.env` | credential이 repository/log에 노출 | 2 | 5 | 10 HIGH | gitignore, secret scan, redaction | 유지/키회전 운영 필요 |
| R-09 | ELK | Elasticsearch/Kibana 노출 또는 내부필드 확산 | 3 | 4 | 12 HIGH | loopback lab, strict projection | OPEN: 운영 network control |
| R-10 | Telegram | 중복/불필요 alert 또는 과도한 외부전송 | 2 | 3 | 6 MEDIUM | threshold, redaction, dedupe/retry | 유지 |
| R-11 | Incident Response | 실제 사고 시 연락·보고·법률 판단 지연 | 3 | 4 | 12 HIGH | IR playbook | OPEN: 조직 절차/훈련 |
| R-12 | `description` metadata | 외부 게시글에 우발적 개인정보가 포함 | 3 | 4 | 12 HIGH | allowlist, redaction, bounded metadata | 잔여위험 인정 |

## 주의

`alert/risk.py`가 산정하는 CRITICAL/HIGH/MEDIUM 등은 **수집된 위협 사건의 위험도**입니다. 이 문서의 R-01~R-12는 **시스템 운영의 정보보호 위험**이며 서로 다른 개념입니다.
