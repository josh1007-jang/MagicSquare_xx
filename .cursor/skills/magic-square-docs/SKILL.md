---
name: magic-square-docs
description: >-
  MagicSquare_xx 세션 Report·Transcript·TDD 체크리스트 생성. Use when exporting
  sessions, writing NN.REPORT.md, Export-Transcript, session summaries, or when
  the user mentions /export, ARRR documentation, or MagicSquare session reports.
---

# MagicSquare_xx — Docs Skill

세션 문서(Report, Transcript, 체크리스트) 작성용 Skill.
SSOT: `.cursorrules`, `docs/PRD.md`(있을 때), `.cursor/commands/export.md` (`/export`)

---

## 번호 규칙 (`/export` 와 동일)

1. `Report/`, `Prompting/` 의 `NN.*` 파일만 번호 후보 (`Session3_…` 레거시 제외)
2. 최대 번호 + 1 → 다음 `NN` (2자리: `01`, `02`, …)
3. **기존 `NN.*` 덮어쓰기 금지**

| 산출물 | 경로 |
|--------|------|
| 세션 보고서 | `Report/NN.REPORT.md` |
| Transcript | `Prompting/NN.Export-Transcript.md` |

---

## 템플릿 (복사·채움)

| 용도 | 파일 |
|------|------|
| Report | [templates/session-report-template.md](templates/session-report-template.md) |
| Transcript | [templates/export-transcript-template.md](templates/export-transcript-template.md) |
| TDD 체크리스트 | [templates/tdd-checklist-template.md](templates/tdd-checklist-template.md) |

`/export` 실행 시 Report + Transcript **2개 필수**. 체크리스트는 세션 중·종료 전 자기 점검용(선택 저장).

---

## Export AAA (`.cursor/commands/export.md`)

1. **Arrange** — 채팅에서 Phase·파일·pytest 결과 추출; 다음 `NN` 결정
2. **Act** — `Report/NN.REPORT.md`, `Prompting/NN.Export-Transcript.md` 생성
3. **Assert** — 동일 NN, 상호 링크, pytest 섹션(TDD 세션), 왜곡 없는 결과

응답 첫 줄:

```
Phase: EXPORT | Target: session | Track: report+transcript
```

---

## pytest 기록 (TDD 세션)

```bash
pytest tests/test_validate_lines.py -v
```

실패를 pass로 기록하지 않는다. 예: `4 failed — NotImplementedError (RED 대기)`

---

## 완료 보고 (채팅)

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

- 사용자에게 주제·번호 **추가 질문** (`/export` 는 즉시 실행)
- Report만 또는 Transcript만 생성
- `src/`·`tests/` 수정
- pytest·assert 기대값 왜곡
- 기존 `NN.*` 덮어쓰기
