# Project Story — Portfolio & Interview Notes

이 문서는 저장소 기능을 과장하지 않고 **문제 → 판단 → 구현 → 검증 → 결과** 순서로 설명하기 위한 요약입니다.

## 1. 한 문장 소개

여러 다크웹 유출 게시글을 단순 저장하던 초기 프로젝트를, **사건 단위 identity·변경 이력·알림·분석·운영 통제까지 연결하는 위협 인텔리전스 모니터링 파이프라인**으로 개선했습니다.

## 2. 처음 상태에서 확인한 문제

초기 구조는 source별 crawler가 HTML을 읽어 MongoDB에 저장하고 Django에서 결과를 조회하는 데 초점이 있었습니다. 실제 운영 관점에서는 다음 문제가 남았습니다.

- 같은 사건을 다시 수집했을 때 중복과 재관찰을 구분하기 어려움
- 피해 규모나 설명이 바뀌어도 현재 상태만 남아 변경 근거가 사라짐
- 새 사건과 단순 날짜 변경을 같은 수준으로 알릴 수 있어 알림 피로가 생김
- crawler availability와 parser correctness가 한 덩어리로 취급됨
- Mongo 내부 delivery/private field까지 분석 표면에 노출될 위험이 있음
- 대시보드 접근통제, 보유기간, 감사, source lifecycle 같은 운영 통제가 부족함

## 3. 개선 흐름

```text
Crawler refactor
→ stable event identity / dedupe / history
→ NEW / UPDATED alert + retry / dedupe
→ analyst dashboard
→ MongoDB → Monstache → Elasticsearch / Kibana
→ access / retention / audit / source lifecycle governance
```

각 단계는 앞 단계의 schema와 동작을 최대한 보존하고, 새 기능 때문에 기존 기능이 깨지지 않는지 regression을 반복 확인했습니다.

## 4. 주요 설계 판단

### 기존 `_id`를 버리지 않고 `event_key`를 추가

기존 parser `_id`는 이미 저장된 문서와 fixture의 호환성에 사용되고 있었습니다. 이를 즉시 교체하지 않고 장기 사건 식별용 `event_key`를 별도로 두어 **레거시 호환성과 안정적인 사건 추적을 분리**했습니다.

### 현재 상태와 변경 이력을 분리

`leaked_data`에는 현재 상태를, `leak_history`에는 field-level before/after를 기록했습니다. 동일 변경 재처리 시 history가 중복되지 않도록 deterministic ID를 사용했습니다.

### 모든 변경을 알리지 않음

`NEW`와 `UPDATED`를 구분하고, 날짜만 변하는 등 비본질적 변경은 `SUPPRESSED`할 수 있게 했습니다. 알림에는 deterministic identity, lease, retry/attempt count를 두어 재시작 후 중복 전송을 줄였습니다.

### MongoDB와 분석 표면을 분리

MongoDB 운영에 필요한 내부 상태를 Django/Elasticsearch에 전부 노출하지 않았습니다. Monstache projection에서 allowlist를 사용하고 `message`, `claim_token`, `resume_token` 같은 alert 내부 필드는 Elasticsearch에서 제외했습니다.

### 접근 불가 source를 삭제하지 않고 lifecycle로 관리

parser와 fixture는 재현 자료로 남기되 scheduler는 `ACTIVE` source만 실행합니다. 현재 Bitlock만 ACTIVE이며 다른 source는 UNAVAILABLE 상태로 자동 실행에서 제외합니다. 이 상태는 위협 행위자의 실제 활동 여부를 의미하지 않습니다.

### retention은 자동 삭제보다 안전장치를 우선

운영 DB에 destructive test를 하지 않고 read-only checker와 DRY RUN을 기본으로 했습니다. 실제 삭제에는 `--apply`와 DB 이름 이중 확인이 필요하고, invalid/missing/future timestamp는 자동 삭제하지 않습니다.

## 5. 실제 통합 과정에서 발견한 문제

자동 테스트가 통과한 뒤에도 실제 환경에서 다음 문제를 발견했습니다.

### Elasticsearch date mapping 표현 차이

Elasticsearch 8.15.3이 기본 date format을 mapping 응답에서 생략해 strict comparator가 충돌로 오판했습니다. 생략 가능한 기본값만 호환 처리하고 나머지 mapping 검사는 유지했습니다.

### Monstache BSON datetime 호환

실제 Monstache/Otto 런타임에서 BSON datetime이 JavaScript native `Date`와 다른 Go-backed 형태로 전달돼 timestamp가 사라졌습니다. 여러 time 표현을 안전하게 ISO 문자열로 변환하도록 보완했습니다.

### Kibana Data View 이름 충돌

여러 테스트 index prefix가 공존할 때 같은 Data View display name이 충돌했습니다. prefix를 display name에 포함해 테스트 환경을 분리했습니다.

### 실제 브라우저 CSRF origin 오류

Django unit test는 통과했지만 실제 로그인 POST에서 template의 `no-referrer` 정책 때문에 Origin 검사가 실패했습니다. project 설정과 일치하도록 `same-origin`으로 수정하고 regression assertion을 추가한 뒤 로그인/로그아웃을 다시 검증했습니다.

이 경험 때문에 **mock/unit test 통과와 실제 서비스 통합 성공을 분리해서 판단**했습니다.

## 6. 검증 결과

ISMS-P 확장 전 최종 baseline에서 확인한 대표 결과입니다. 이번 확장 후 최종 PASS 수는 로컬 `.venv`에서 재검증한 뒤 갱신합니다.

- root unittest: 266 PASS
- Django `mongoDbConnect`: 77 PASS
- governance 전용 unittest: 72 PASS
- Django system check: 0 issues
- Node projection reference test: 14 PASS (Node 사용 가능 환경)
- secret/runtime/diff 검사: PASS
- MongoDB → Monstache → Elasticsearch initial sync: PASS
- 실행 중 change stream 반영: PASS
- Monstache 중단 중 변경 후 resume: PASS
- Kibana Data View 3개 / Dashboard 5개 패널 / Saved Objects export: PASS
- 실제 Mongo governance read-only check / retention DRY RUN: PASS
- 실제 Django 로그인 → 조회 → 로그아웃 → 미인증 재차단: PASS
