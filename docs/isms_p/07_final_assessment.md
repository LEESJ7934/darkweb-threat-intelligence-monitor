# 모의진단 최종 평가

## 1. 최초 진단 요약

기존 시스템은 인증, audit logging, retention safety, secret redaction, source lifecycle, ELK field minimization 등 기술 통제를 갖추고 있었습니다. 그러나 이를 ISMS-P 관점의 **범위-자산-흐름-위험-통제-증적**으로 연결한 산출물이 없었고, 특히 다음 두 GAP이 명확했습니다.

- 모든 인증 사용자의 governance 기능 권한이 구분되지 않음
- audit log를 생성하지만 정기 검토하는 기준·도구가 없음

## 2. 이번 개선

### Access Control

- Analyst: dashboard/event detail 조회
- Security Admin (`is_staff=True`): Analyst 권한 + `/governance/audit-review/`
- Anonymous: 로그인으로 redirect
- Analyst의 governance review 접근: 403

### Audit Review

- 기본 최근 30일, UTC 기준
- current/rotated `audit.jsonl*` read-only 검토
- `login_failure >= 5`, `denied_access >= 5`, `error >= 1`, `retention_error >= 1`, `malformed >= 1` 시 `ATTENTION`
- raw `user_hash`/`document_hash` 및 요청 metadata를 결과에 출력하지 않음

## 3. 재평가

| 영역 | 이전 | 이후 | 잔여 한계 |
|---|---|---|---|
| 사용자/특수권한 관리 | PARTIAL/GAP | PARTIAL | Django staff 기반 최소구현, MFA/정기 권한검토 없음 |
| 로그 관리 | PARTIAL | PARTIAL | rotation은 있으나 중앙/WORM 보호 없음 |
| 로그 점검 | GAP | PARTIAL | read-only review 구현, 실제 조직 승인·자동 alert workflow 없음 |
| 위험관리 | GAP | PARTIAL | project risk register/treatment 작성, 실제 경영진 수용 아님 |
| 관리체계 점검 | GAP | PARTIAL | 모의 GAP matrix 존재, 정기 audit cycle은 향후 과제 |

## 4. 남은 주요 GAP

- MFA/login throttling 및 계정/권한 정기 검토
- audit 중앙수집·변조방지
- Mongo/ELK backup/restore 정기 시험
- 운영환경 NTP/시간동기화 증적
- 실제 incident contact/escalation/tabletop
- 개인정보 법적 적용성·보유기간·파기 기준 별도 법률검토

## 5. 포트폴리오 표현

권장 표현:

> 자체 개발한 위협정보 모니터링 시스템을 대상으로 ISMS-P 통제항목 기반 모의진단을 수행하여 정보자산·데이터 흐름을 식별하고, 위험평가와 GAP 분석을 통해 역할별 접근통제 및 감사로그 점검 체계를 개선하고 증적을 연결했습니다.

피해야 할 표현:

- "ISMS-P 인증을 획득했다"
- "실제 인증심사를 수행했다"
- "개인정보보호법 준수 시스템이다"
