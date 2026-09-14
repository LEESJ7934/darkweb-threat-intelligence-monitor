# 현황 및 데이터 흐름 분석

## 1. 주요 흐름

```text
[TB-01 Untrusted Darkweb Source]
              │
              ▼
       Selenium / Tor
              │
              ▼
       Parser / Normalizer
              │
       allowlist/redaction
              ▼
[TB-03]     MongoDB
          /    |      \
         /     |       \
 current    history    risk
                        │
                        ▼
                     alert_log
                        │
                        ▼
              [TB-04 Telegram API]

MongoDB ──→ [TB-05 Django Dashboard] ──→ Analyst / Security Admin
    │
    └──→ Monstache ──→ [TB-06 Elasticsearch / Kibana]

Django / Retention ──→ [TB-02 Local audit.jsonl] ──→ Security Admin Audit Review
```

## 2. Trust Boundary

| ID | 경계 | 주요 위험 | 현재 통제 |
|---|---|---|---|
| TB-01 | 외부 다크웹 → Crawler | 악성/과도한 입력, source 변동 | parser allowlist, bounded metadata, source lifecycle |
| TB-02 | Application Runtime | secret 노출, 로그 과수집 | `.env`, secret scan, audit allowlist |
| TB-03 | MongoDB | 데이터 변조·장기보유 | identity/dedupe/history, retention safety |
| TB-04 | Telegram API | 외부전송·중복전송 | redaction, risk threshold, deterministic alert |
| TB-05 | Analyst Web Boundary | 비인가 조회, 권한 과다 | auth, Analyst/Security Admin 분리, CSRF/no-cache |
| TB-06 | ELK Boundary | 내부필드 확산·분석표면 확대 | strict projection/mapping, minimized fields |

## 3. 민감 데이터 이동 원칙

- raw credential·secret·private delivery field는 분석 표면으로 전달하지 않습니다.
- MongoDB 전체 document를 Elasticsearch로 그대로 복제하지 않습니다.
- audit에는 raw username/document ID 대신 SHA-256 pseudonym을 기록합니다.
- Audit Review는 raw audit record를 다시 노출하지 않고 aggregate count만 제공합니다.
