# 정보자산 목록

| ID | 정보자산 | 유형 | 주요 정보/기능 | 중요도 | 개인정보 관점 | 주요 통제 |
|---|---|---|---|---|---|---|
| A-01 | Darkweb Sources | 외부 정보원 | 게시글 metadata source | Medium | 우발적 개인정보 포함 가능 | source lifecycle |
| A-02 | Selenium/Tor Crawler | Application | 수집 요청·HTML 처리 | High | 원문 과수집 주의 | allowlist, source registry |
| A-03 | Parser/Normalizer | Application | metadata 정규화 | High | 최소수집 대상 | bounded metadata, redaction |
| A-04 | Scheduler | Application | crawler 실행 제어 | Medium | 직접 저장 없음 | ACTIVE source only |
| A-05 | `leaked_data` | Database | 사건 현재 상태 | High | incidental PII 가능 | allowlist, retention |
| A-06 | `leak_history` | Database | field-level 변경 이력 | High | incidental PII 가능 | history sanitization, retention |
| A-07 | `alert_log` | Database | 알림 처리·전송 상태 | High | 최소화된 event metadata | dedupe, redaction, retention |
| A-08 | Django Dashboard | Application | 분석가 조회 화면 | High | 사건 metadata 표시 | authentication, RBAC, no-cache |
| A-09 | Django Auth DB | Database | 계정/비밀번호 hash | High | 계정정보 | Django auth, CSRF |
| A-10 | Telegram Integration | External Service | 임계치 이상 alert 전달 | Medium | 제한된 metadata 외부전송 | redaction, threshold, dedupe |
| A-11 | Elasticsearch | Search/Data | 분석용 read model | High | allowlist metadata | strict projection/mapping |
| A-12 | Kibana | Analysis UI | 검색·dashboard | High | 분석정보 노출 가능 | loopback/local lab, minimized fields |
| A-13 | Audit Log | Security Log | 로그인·접근·retention 추적 | High | pseudonymous identifiers | hash, rotation, review |
| A-14 | `.env` / Credentials | Secret | Mongo/Telegram/Django secret | Critical | 인증정보 | gitignore, secret scan, redaction |
| A-15 | Docker/Host Runtime | Infrastructure | 서비스 실행환경 | High | 운영데이터 접근 가능 | runtime check, local exposure control |

## 개인정보 관련 가정

이 프로젝트는 개인정보 수집 자체를 목적으로 하지 않습니다. 그러나 외부 게시글의 `description` 등 metadata에 개인정보가 우발적으로 포함될 가능성을 완전히 배제하는 DLP를 구현한 것은 아니므로 `Intended PII: No / Incidental PII possibility: Yes`로 평가합니다.

자산 중요도는 포트폴리오용 상대평가이며 실제 조직의 BIA/자산평가 결과를 의미하지 않습니다.
