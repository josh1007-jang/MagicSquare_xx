---
name: magic-square-tdd
description: >-
  MagicSquare_xx validate_lines TDD(RED→GREEN→REFACTOR) 워크플로와 ARRR 절차,
  슬래시 커맨드 연계. Use when implementing validate_lines, writing pytest for
  10-line magic square checks, or when the user mentions TDD, RED, GREEN,
  REFACTOR, ARRR, TC1, TC2, TC3, or magic square validation.
---

# MagicSquare_xx — TDD Skill

4×4 부분 마방진 **10선 검증** (`validate_lines`) TDD 실습용 Skill.
SSOT: `.cursorrules`, `docs/PRD.md`(있을 때), `Report/Session3_Workbook_MagicSquare_xx.md`

---

## ARRR (실습 루프)

모든 TDD 커맨드는 동일한 4단계를 따른다.

| 단계 | 의미 | Phase별 실행 |
|------|------|----------------|
| **A**rrange | SSOT·pytest·격자·기대 dict·수정 파일 범위 확정 | 공통 |
| **R**ed | 실패 테스트 작성·계획 (`tests/` 만) | RED |
| **R**un | pytest 실행·구현·리팩터 적용 | RED/GREEN/REFACTOR |
| **R**eport | `Phase:` 선언 + 채팅 보고 블록 | 공통 |

응답 **첫 줄** (`.cursorrules`):

```
Phase: RED | GREEN | REFACTOR | Target: validate_lines | Track: <...>
```

---

## Entity · Control · Boundary (요약)

| 계층 | 핵심 |
|------|------|
| Entity | 4×4, `0`=빈칸, 1~16, 합 34, 10선 `R1~R4`·`C1~C4`·`D1`·`D2` 전수 |
| Control | `src/validate_lines.py` — `validate_lines(grid) -> dict` |
| Boundary | `tests/test_validate_lines.py` — 공개 API 결과 dict 만 assert |

반환 계약:

```python
{"status": "pass" | "fail" | "incomplete", "failed_lines": ["R1", "D1", ...]}
```

---

## Test Loop (최소)

| ID | 시나리오 | 기대 |
|----|----------|------|
| TC1 | 10선 모두 34 | `pass`, `failed_lines == []` |
| TC2 | 행·열 OK, D1 불일치 | `fail`, `"D1" in failed_lines` |
| TC3 | 행·열 OK, D2 불일치 | `fail`, `"D2" in failed_lines` |
| — | `0` 빈칸 존재 | `incomplete` |

---

## 슬래시 커맨드 맵

| 커맨드 | Phase | 역할 |
|--------|-------|------|
| `/red-test-plan` | RED | 다음 실패 테스트 **계획만** (파일 수정 없음) |
| `/red-skeleton` | RED | 테스트 **골격** 1개 추가 (`tests/`) |
| `/tdd-red` | RED | 완전한 실패 테스트 1개 추가 (`tests/`) |
| `/green-minimal` | GREEN | **첫 FAIL 1개** 최소 구현 (`src/`) |
| `/golden-master` | GREEN | **전체 스위트** ALL PASS + 골든 스냅샷 |
| `/refactor-smell` | REFACTOR | smell **진단만** (`src/` 수정 없음) |
| `/refactor-safe` | REFACTOR | smell **1건** 안전 정리 (`src/`, green 유지) |
| `/export` | EXPORT | 세션 Report + Transcript (`.cursor/commands/export.md`) |

권장 순서:

```
/red-test-plan → /red-skeleton 또는 /tdd-red → /green-minimal → … → /golden-master
→ /refactor-smell → /refactor-safe → /export
```

---

## Phase 규칙

| Phase | 수정 허용 | 금지 |
|-------|-----------|------|
| RED | `tests/` | `src/` 수정, assert 완화, skip, xfail |
| GREEN | `src/` | `tests/` 수정, 10선 생략, 과도한 추상화 |
| REFACTOR | `src/` (동작 불변) | API·Entity 변경, 테스트 수정 |

- 한 번에 **한 동작**(한 테스트 또는 한 smell)만.
- 대화·설명은 **한국어**.

---

## pytest (기본)

```bash
# 테스트 1개
pytest tests/test_validate_lines.py::test_<함수명> -v

# 전체
pytest tests/test_validate_lines.py -v
```

---

## 범위 밖 (하지 않음)

솔버, 빈칸 자동 채우기, UI, 배포, Rule/Command 문서 자동 생성, git commit(사용자 요청 시만).
