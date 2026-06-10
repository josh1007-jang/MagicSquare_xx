# MagicSquare_xx — TDD 세션 체크리스트

**세션:** {주제} · **날짜:** {YYYY-MM-DD}

---

## SSOT 확인

- [ ] `.cursorrules` — Entity·Control·Boundary·TDD 규칙
- [ ] `docs/PRD.md` — 요구사항 (있을 때)
- [ ] `Report/Session3_Workbook_MagicSquare_xx.md` — R-G-I-O·성공 기준

---

## ARRR · Phase

| # | 단계 | 완료 | 메모 |
|---|------|:----:|------|
| 1 | **A**rrange — 격자·기대 dict·파일 범위 | [ ] | |
| 2 | **R**ed — `tests/` 실패 테스트 | [ ] | |
| 3 | **R**un — pytest FAIL/PASS 확인 | [ ] | |
| 4 | **R**eport — `Phase:` 선언·채팅 보고 | [ ] | |

---

## Test Loop

- [ ] TC1 — 10선 pass, `failed_lines == []`
- [ ] TC2 — 행·열 OK, D1 fail
- [ ] TC3 — 행·열 OK, D2 fail (대각선 생략 방지)
- [ ] incomplete — `0` 포함 → `incomplete`

---

## Phase 게이트

### RED

- [ ] `tests/` 만 수정
- [ ] assert 완화·skip·xfail 없음
- [ ] 공개 API `validate_lines` 결과 dict 만 검증

### GREEN

- [ ] `src/validate_lines.py` 최소 구현
- [ ] 10선 전수 검사 (R1~R4, C1~C4, D1, D2)
- [ ] `tests/` 미수정

### REFACTOR

- [ ] pytest ALL PASS 유지
- [ ] 동작·API 불변
- [ ] smell 1건씩 (`/refactor-smell` → `/refactor-safe`)

---

## pytest 기록

```bash
pytest tests/test_validate_lines.py -v
```

**결과:** {N passed, M failed — 한 줄}

---

## Export (세션 종료 시)

- [ ] `/export` — `Report/NN.REPORT.md` + `Prompting/NN.Export-Transcript.md`
- [ ] 동일 NN·상호 링크·기존 NN 덮어쓰기 없음
