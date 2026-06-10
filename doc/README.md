# MagicSquare_xx — doc

프로젝트 **요구사항·계약** 문서 모음. 구현·테스트·AI Skill의 SSOT(단일 기준)로 사용한다.

| 파일 | 버전 | 내용 |
|------|------|------|
| [`PRD.md`](PRD.md) | 0.2 | Product Requirements Document — Mom Test, R-G-I-O, ECB, Control·Entity API, Test Loop |

---

## PRD 역할

`PRD.md`는 아래 문서·코드가 분산해 두었던 요구사항을 **한곳으로 통합**한다.

| 출처 | PRD에서 다루는 내용 |
|------|---------------------|
| `Report/MomTest_STEP1_MagicSquare_xx.md` | 문제 정의, 페르소나, 증거 |
| `Report/Session3_Workbook_MagicSquare_xx.md` | R-G-I-O, 성공 기준, 8계층 |
| `.cursorrules` | Entity · Control · Boundary · TDD |
| `src/validate_lines.py`, `src/entity/validation.py` | Control·Entity 10선 |
| `src/find_blank_coords.py`, `src/solve_step_a.py` | Entity D-LOC, D-SOL step A |
| `tests/test_validate_lines.py`, `tests/entity/` | Boundary + Entity Test Loop |
| `Report/01~03.REPORT.md` | Harness, 정합성 리뷰, ARRR 1사이클 |

**충돌 시 우선순위:** `PRD.md` §7~§9 → `.cursorrules`

---

## PRD 목차 (빠른 참조)

| § | 제목 | 용도 |
|---|------|------|
| 1 | 개요 | Control + Entity ECB |
| 2 | 문제 정의 | Mom Test |
| 3~4 | R-G-I-O · 성공 기준 | SC1~SC7 |
| 5 | 범위 | In / Out (step A In) |
| 6~7 | ECB · Entity | 10선, Entity API |
| 8 | Control — API | `validate_lines`, F1~F7 |
| 9 | Test Loop | Boundary 5 + Entity 2 |
| 10 | TDD · C2C · Commands | ARRR, `/red-test-plan` |
| 11 | 프로젝트 구조 | 디렉터리 맵 |
| 12 | 워크북 ↔ 계약 갭 | 알려진 차이 |
| 13 | 마일스톤 | **7 passed** |
| 14 | 향후 검토 | v0.3+ |

---

## API 요약

### Control — `validate_lines`

```python
from src.validate_lines import validate_lines

result = validate_lines(grid)
# {"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}
```

### Entity

```python
from src.find_blank_coords import find_blank_coords
from src.solve_step_a import solve_step_a
from src.entity.validation import compute_line_sum, MAGIC_CONSTANT

find_blank_coords(grid)           # → [(2, 3), (4, 4)]  # G1, 1-indexed
solve_step_a(grid)                # → {"status":"success", "coord":(2,3), "value":11}
compute_line_sum(grid, "R1")      # → int
```

- **Input:** 4×4 정수 격자 (`0`=빈칸, `1`~`16`)
- **10선:** `R1`~`R4`, `C1`~`C4`, `D1`, `D2`
- **마법상수:** `34` (`src/entity/validation.py`)

---

## Test Loop (요약)

### Boundary — `tests/test_validate_lines.py`

| ID | 시나리오 | 기대 |
|----|----------|------|
| TC1 | 10선 모두 34 | `pass`, `[]` |
| TC2 | D1 불일치 | `fail`, `"D1" in failed_lines` |
| TC3 | D2 불일치 | `fail`, `"D2" in failed_lines` |
| incomplete | 빈칸 `0` | `incomplete` |
| R1 fail | R1 합 ≠ 34 | `fail`, `"R1" in failed_lines` |

### Entity — `tests/entity/`

| Test ID | 시나리오 | 기대 |
|---------|----------|------|
| D-LOC-01 | G1 빈칸 좌표 | `[(2,3),(4,4)]` |
| D-SOL-01 | G1 step A | `success`, `(2,3)`, `11` |

### RED 후보 (PRD §13)

- **D-LINE-C2-01** (FR-F3) — C2 열 불일치
- **D-SOL-02-step-b** — G1 `(4,4)` → `1`

---

## 관련 폴더

| 폴더 | 역할 |
|------|------|
| `src/entity/` | 10선 합 (`validation.py`) |
| `src/` | Control, D-LOC, D-SOL step A |
| `tests/` | Boundary + Entity (7 tests) |
| `Report/` | Mom Test, 워크북, Export `01`~`03` |
| `Prompting/` | Transcript, STEP 프롬프트 |
| `.cursor/` | Commands 8종, Skills |

---

## 현재 상태 (PRD §13)

| 단계 | 상태 |
|------|:----:|
| Mom Test · 워크북 · Harness · Skills · Commands | ✅ |
| Control GREEN (validate_lines 5 tests) | ✅ |
| Entity D-LOC-01 · D-SOL-01 | ✅ |
| REFACTOR (`entity/validation.py`) | ✅ |
| Export 03 (ARRR 1사이클) | ✅ |

```bash
python -m pytest tests/ -v
# → 7 passed in ~0.03s
```

---

## SSOT 참조 (Skills · 커맨드)

- `.cursor/skills/magic-square-tdd/SKILL.md`
- `.cursor/skills/magic-square-docs/SKILL.md`
- `.cursor/commands/red-test-plan.md` — C2C Ask (RED ③)

PRD 갱신 시 §7~§9와 `.cursorrules`를 함께 맞춘다.
