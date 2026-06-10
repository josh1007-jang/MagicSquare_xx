# export — 세션 보고서 + Transcript Export

**추가 입력 없이 즉시 실행.** 사용자가 `/export` 만 입력했다.
세션 주제·산출물·대화·pytest 상태는 **현재 채팅 전체**에서 자동 추출한다. 추가 질문·확인 요청 금지.

프로젝트: **MagicSquare_xx** · 설계 참고: `.cursorrules`, `Report/Session3_Workbook_MagicSquare_xx.md`

---

## 필수 선언 (응답 첫 줄)

```
Phase: EXPORT | Target: session | Track: report+transcript
```

---

## AAA 절차

1. **Arrange**
   - `Report/`, `Prompting/` 에서 `NN.*` 형식 파일의 **가장 큰 번호**를 확인하고, 다음 **2자리 번호** `NN`을 정한다. (없으면 `01`)
   - 현재 대화에서 추출: 세션 주제, Phase 이력(RED/GREEN/REFACTOR), 생성·수정 파일, User/Cursor 턴 전문
   - TDD 세션이면 `pytest tests/test_validate_lines.py -v` 를 실행해 결과(통과/실패 수, 대표 메시지)를 확보한다
2. **Act**
   - `Report/NN.REPORT.md` — 세션 요약 보고서 **생성**
   - `Prompting/NN.Export-Transcript.md` — 대화 전문 Transcript **생성**
3. **Assert**
   - 두 파일 모두 존재하고, **동일 NN** 으로 상호 링크되어 있는지 확인한다
   - 파일명이 `01.XXX` 형식(`NN.REPORT.md`, `NN.Export-Transcript.md`)인지 확인한다
   - 보고서에 pytest 결과 섹션이 포함되었는지(TDD 세션인 경우) 확인한다

---

## pytest 예시

TDD·Harness 세션 보고서에 아래를 **실행 결과 그대로** 기록한다 (통과/실패를 왜곡하지 않는다).

```bash
pytest tests/test_validate_lines.py -v
```

기록 예:

```
4 failed — NotImplementedError (RED 대기)
# 또는
4 passed — GREEN 완료
```

---

## 번호·생성 파일 (반드시 2개)

| 파일 | 설명 |
|------|------|
| `Report/NN.REPORT.md` | 세션 요약 보고서 |
| `Prompting/NN.Export-Transcript.md` | 대화 전문 Export |

**번호 규칙**

1. `Report/`, `Prompting/` 의 `NN.*` 파일만 번호 후보로 본다 (`Session3_…` 등 레거시명은 제외)
2. 최대 번호 + 1 → 다음 `NN` (2자리: `01`, `02`, …)
3. **기존 번호 파일 덮어쓰기 금지**

---

## 보고서 형식 (`Report/NN.REPORT.md`)

```markdown
# MagicSquare_xx — {세션 주제}

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_xx |
| **단계** | {RED|GREEN|REFACTOR|설계|…} |
| **보고서 생성일** | {YYYY-MM-DD} |
| **목적** | {한 줄} |

---

## 1. 요약

{이번 세션에서 한 일 3~5줄}

## 2. 핵심 결정·산출물

| 구분 | 내용 |
|------|------|
| Phase | {RED|GREEN|REFACTOR|…} |
| 변경·생성 파일 | {목록} |
| pytest | {명령 + 결과 한 줄} |
| API·계약 | {validate_lines 등 해당 시} |

## 3. 다음 단계

- {후속 작업 1~3개}

---

**관련 Transcript:** [Prompting/NN.Export-Transcript.md](../Prompting/NN.Export-Transcript.md)

*본 문서는 Report/NN.REPORT.md — {세션 주제} 세션 Export입니다.*
```

---

## Transcript 형식 (`Prompting/NN.Export-Transcript.md`)

```markdown
# MagicSquare_xx — Export Transcript

_Exported on {YYYY-MM-DD} from Cursor_

---

## User

{사용자 메시지 전문}

## Cursor

{어시스턴트 응답 전문}

{턴 반복 — 요약 금지, 대화 재구성}

---

## 생성·변경 파일

| 파일 | 작업 |
|------|------|
| {path} | {created|updated} |

**관련 보고서:** [Report/NN.REPORT.md](../Report/NN.REPORT.md)

*본 문서는 Prompting/NN.Export-Transcript.md — {세션 주제} Transcript Export입니다.*
```

---

## 완료 보고 형식 (채팅)

```
Phase: EXPORT | Target: session | Track: report+transcript

- 번호: NN
- Report: Report/NN.REPORT.md
- Transcript: Prompting/NN.Export-Transcript.md
- 세션 주제: {한 줄}
- pytest: {결과 한 줄 또는 N/A}
```

---

## 금지

- 사용자에게 세션 주제·번호·형식 **추가 질문**
- 기존 `NN.*` 파일 **덮어쓰기**
- 번호 없이 저장 (`REPORT.md` 단독명 금지)
- 보고서만 만들고 Transcript 생략 (또는 그 반대)
- **`src/` 수정** (Export는 문서만 생성)
- pytest 결과·assert 기대값 **완화·생략·왜곡** (실패를 pass로 기록하지 않음)
- `@pytest.mark.skip`, `xfail` 권장·적용 (Export 중 테스트 코드 변경 금지)
