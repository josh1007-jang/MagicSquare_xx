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
| 5 | 범위 | In / Out (step A In, UI Out) |
| 6~7 | ECB · Entity | 10선, Entity API |
| 8 | Control — API | `validate_lines`, F1~F7 |
| 9 | Test Loop | Boundary 5 + Entity 2 |
| 10 | TDD · C2C · Commands | ARRR, Layer·Track, 8 커맨드 |
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

### UI (설계 예시 — PRD §5.2 Out of Scope)

```python
# 미구현 — `/verify-magic-square` Command 대응 (워크북 §8계층)
from src.ui.verify_magic_square import verify_magic_square  # RED 후보

verify_magic_square(grid)  # 입력 OK → validate_lines 위임
                           # 입력 NG → {"status":"error", "code":"E003"|"E004", ...}
```

---

## Test Loop (요약)

### Boundary (Logic) — `tests/test_validate_lines.py`

| ID | 테스트 함수 | 시나리오 | 기대 |
|----|-------------|----------|------|
| TC1 | `test_tc1_all_ten_lines_pass` | 10선 모두 34 | `pass`, `[]` |
| TC2 | `test_tc2_rows_cols_ok_diagonal_d1_fails` | D1 불일치 | `fail`, `"D1" in failed_lines` |
| TC3 | `test_tc3_rows_cols_ok_diagonal_d2_fails` | D2 불일치 | `fail`, `"D2" in failed_lines` |
| — | `test_incomplete_when_blank_present` | 빈칸 `0` | `incomplete` |
| — | `test_fail_includes_r1_when_row_sum_not_34` | R1 합 ≠ 34 | `fail`, `"R1" in failed_lines` |

### Entity (Logic) — `tests/entity/`

| Test ID | 테스트 함수 | Given | Then |
|---------|-------------|-------|------|
| D-LOC-01 | `test_d_loc_01_find_blank_coords_returns_g1_blanks` | `grid_g1` | `[(2,3),(4,4)]` |
| D-SOL-01 | `test_d_sol_01_step_a_success` | `grid_g1` | `success`, `(2,3)`, `11` |

### G1 격자 (`tests/conftest.py`)

```
16  3  2 13
 5 10  0  8   ← (2,3)
 9  6  7 12
 4 15 14  0   ← (4,4)
```

### RED 후보

| Track | ID | 설명 | 상태 |
|-------|-----|------|:----:|
| Logic | **D-LINE-C2-01** (FR-F3) | C2 열 불일치 → `fail`, `"C2" in failed_lines` | 🔲 |
| Logic | **D-SOL-02** step B | G1 `(4,4)` → `1` | 🔲 |
| UI | **U-IN-01** | `grid=None` → `E003`, `validate_lines` 미호출 | 🔲 설계 |
| UI | **U-IN-02** | 3×3 등 비정형 → `E004`, `validate_lines` 미호출 | 🔲 설계 |

Logic Track: `tests/test_validate_lines.py` · Entity: `tests/entity/`  
UI Track: `tests/ui/` (미생성) — C2C `/red-test-plan` **Layer: boundary · Track: UI** 설계 예시

---

## TDD · C2C (`/red-test-plan`)

| 선언 | 값 |
|------|-----|
| Phase | `red` \| `green` \| `refactor` |
| Layer | `entity` (도메인·Entity API) \| `boundary` (공개 API dict 계약) |
| Track | `Logic` (10선·좌표·step A) \| `UI` (입력 검증·Command — Out of Scope, 설계만) |

**ARRR:** Arrange (Ask) → Red → Run (pytest) → Report  
**C2C 4블록:** Rule1~3 · Track B · 테스트 플랜 · ECB·Mock (E001~E005)

| 커맨드 | Phase | 역할 |
|--------|-------|------|
| `/red-test-plan` | RED | C2C 설계표·플랜 (파일 수정 없음) |
| `/red-skeleton` | RED | 테스트 골격 1개 |
| `/tdd-red` | RED | 실패 테스트 1개 |
| `/green-minimal` | GREEN | 첫 FAIL 최소 구현 |
| `/golden-master` | GREEN | ALL PASS |
| `/refactor-smell` | REFACTOR | smell 진단 |
| `/refactor-safe` | REFACTOR | smell 1건 정리 |
| `/export` | EXPORT | Report + Transcript |

---

## 프로젝트 구조 (요약)

```
MagicSquare_xx/
├── doc/              ← PRD.md, README.md (본 파일)
├── src/
│   ├── entity/validation.py
│   ├── validate_lines.py
│   ├── find_blank_coords.py
│   └── solve_step_a.py
├── tests/
│   ├── conftest.py   ← G1_GRID, grid_g1
│   ├── test_validate_lines.py
│   └── entity/
├── Report/           ← 01~03.REPORT.md, Mom Test, 워크북
├── Prompting/
└── .cursor/          ← commands 8종, skills 2종
```

---

## 현재 상태 (PRD §13)

| 단계 | 상태 |
|------|:----:|
| Mom Test · 워크북 · Harness · Skills · Commands | ✅ |
| Control GREEN (validate_lines 5 tests) | ✅ |
| Entity D-LOC-01 · D-SOL-01 | ✅ |
| REFACTOR (`entity/validation.py`) | ✅ |
| Export 03 (ARRR 1사이클) | ✅ |
| UI Track (U-IN-01 · U-IN-02) | 🔲 설계만 |

```bash
python -m pytest tests/ -v
# → 7 passed in ~0.03s
```

---

## SSOT 참조 (Skills · 커맨드)

- `.cursor/skills/magic-square-tdd/SKILL.md`
- `.cursor/skills/magic-square-docs/SKILL.md`
- `.cursor/commands/red-test-plan.md` — C2C Ask (RED ③), Layer·Track 선언

PRD 갱신 시 §7~§9와 `.cursorrules`를 함께 맞춘다.
