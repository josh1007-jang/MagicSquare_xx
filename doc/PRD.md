# MagicSquare_xx — Product Requirements Document (PRD)

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_xx |
| **버전** | 0.2 (세션 3 — 10선 검증 + Entity 보조) |
| **작성일** | 2026-06-10 |
| **최종 갱신** | 2026-06-10 |
| **SSOT 역할** | Mom Test·워크북·`.cursorrules`·API 계약·Test Loop의 단일 요구사항 기준 |
| **관련 문서** | `Report/MomTest_STEP1_MagicSquare_xx.md`, `Report/Session3_Workbook_MagicSquare_xx.md`, `Report/01.REPORT.md`, `Report/02.REPORT.md`, `Report/03.REPORT.md`, `.cursorrules`, `doc/README.md` |

---

## 1. 개요

MagicSquare_xx는 4×4 **부분 마방진** 격자를 다루는 ECB 라이브러리이다. **Control**(`validate_lines`)은 행·열·대각선 **10개 선**의 합이 마법상수 34인지 **빠짐없이** 검증하고, **Entity** 계층은 빈칸 좌표 탐색·10선 합 계산·부분 솔버 step A 등 도메인 연산을 제공한다.

Mom Test에서 드러난 “검증 항목 하나를 빠뜨려 20분을 낭비하는” 문제를, **전수 검증 + 실패 선 식별**로 조기에 드러내는 것이 핵심 목적이다.

| 계층 | 역할 | 진입점 |
|------|------|--------|
| **Control** | 10선 검증 오케스트레이션 | `validate_lines(grid)` |
| **Entity** | 10선 합·빈칸·step A 솔버 | `compute_line_sum`, `find_blank_coords`, `solve_step_a` |
| **Boundary** | pytest 공개 API 계약 | `tests/test_validate_lines.py`, `tests/entity/` |

UI·전체 솔버·배포는 범위 밖이다.

### 1.1 프로젝트 맥락 (Mom Test 과제)

| 항목 | 내용 |
|------|------|
| 과제 | 4×4 마방진에서 빈칸 2개를 찾아 1~16으로 채워 완성 (목표 합 = 34) |
| 설계 패턴 | ECB (Entity–Control–Boundary) |
| 실습 목표 | ECB 분류, 실패 조건(Problem Recognition) 도출, TDD ARRR |

---

## 2. 문제 정의 (Mom Test)

### 2.1 페르소나

4×4 부분 마방진을 손으로/코드로 다루는 **학습자** — 빈칸 2개를 채우고 목표 합 34를 손·코드로 검증한다.

### 2.2 진짜 문제 (한 문장)

4×4 부분 마방진을 손으로 채운 뒤 행·열·대각선 합을 맞췄다고 믿었지만, **확인 항목 하나를 빼먹어 틀린 상태로 20분을 쓴 뒤에야** 잘못을 알 수 있다.

### 2.3 Mom Test 증거

| # | 인용 |
|---|------|
| 1 | "첨부한거 같이 **어려움이 있었어**" |
| 2 | "첨부한거 같이 **작업했는데 어려움이 있었어**" |
| 3 | "**빈칸 2개 넣고 행·열·대각선 합 맞췄는데 대각선 하나를 빼먹어서 20분 날렸어**" |

### 2.4 미응답 (향후 보완)

Q3: "그 20분 끝에 대각선을 빼먹었다는 걸 **언제·무엇을 보고** 알아챘나요?" — 인터뷰 종료로 미응답. 실패 메시지·UX 문구 검증 시 보완 예정 (§14).

### 2.5 표면 문제 (제품 정의 금지 · 전체 솔버/UI)

- "4×4 부분 마방진 **검증 프로그램**을 만들면 좋겠어."
- "행·열·대각선 합을 **자동으로 체크해 주는 도구**가 필요해."
- "ECB 구조로 **마방진 솔버 앱**을 만들면 실습이 쉬워질 거야."

---

## 3. 목표 · R-G-I-O

### 3.1 주제 (한 문장)

행·열·대각선 합 확인에서 **항목을 하나 빼먹어** 틀린 완성 상태를 오래 유지하는 불편을, **빠짐없는 검증**으로 조기에 드러낸다.

### 3.2 R-G-I-O

| | 내용 |
|---|------|
| **Role** | 4×4 부분 마방진 실습 학습자 |
| **Goal** | 행 4개·열 4개·대각선 2개 **총 10개 항목**을 모두 확인했을 때만 완성으로 판정하고, 하나라도 34가 아니면 **어느 항목**인지 즉시 알 수 있다 |
| **Input** | 4×4 정수 격자 (`list[list[int]]`). `0`=빈칸, 채워진 칸=`1`~`16`. 마법상수 `34`는 API 인자가 아닌 상수(`MAGIC_CONSTANT`) |
| **Output** | `validate_lines`: `status` + `failed_lines` · Entity: 좌표 리스트·step A `{status, coord, value}` |

---

## 4. 성공 기준

| # | 기준 | Mom Test 연결 | 검증 방법 |
|---|------|---------------|-----------|
| SC1 | **대각선 2개(D1, D2)** 명시·실행, 행·열만 맞고 대각선 하나만 틀린 격자에서 **fail + 실패 대각선 식별** | 증거 ③ | TC2, TC3 |
| SC2 | ECB·실습 맥락(빈칸, 합 34, 4×4) **재현 시나리오** Test Loop 포함 | 증거 ①·② | TC1~TC3, G1 |
| SC3 | **부분 검증**으로 완성 판정 불가 — 10항목 전수로 틀림 특정 | 증거 ③ "20분" | TC3 |
| SC4 | 빈칸(`0`) 1개 이상 → **`incomplete`** | — | `test_incomplete_when_blank_present` |
| SC5 | **개별 선(행) 불일치** 시 해당 선 ID를 `failed_lines`에 포함 | Goal | `test_fail_includes_r1_when_row_sum_not_34` |
| SC6 | G1 격자 **빈칸 좌표** row-major 1-indexed 반환 | Entity | D-LOC-01 |
| SC7 | G1 **첫 빈칸** row-major step A — 행합 34로 `value` 도출 | Entity | D-SOL-01 |

---

## 5. 범위

### 5.1 In Scope (PRD v0.2)

| 항목 | 설명 | 상태 |
|------|------|:----:|
| Entity 규칙 | 4×4, 0=빈칸, 1~16, 마법상수 34, 10선 | ✅ |
| Entity — 10선 합 | `src/entity/validation.py` — `_sum_cells`, `compute_line_sum` | ✅ |
| Entity — 빈칸 좌표 | `src/find_blank_coords.py` — D-LOC-01 | ✅ |
| Entity — step A 솔버 | `src/solve_step_a.py` — 첫 빈칸 행합 도출 (D-SOL-01) | ✅ |
| Control API | `src/validate_lines.py` — `validate_lines(grid)` | ✅ GREEN |
| Boundary 테스트 | `tests/test_validate_lines.py` — 5건 | ✅ |
| Entity 테스트 | `tests/entity/` — D-LOC-01, D-SOL-01 | ✅ |
| 공유 픽스처 | `tests/conftest.py` — `G1_GRID`, `grid_g1` | ✅ |
| TDD · ARRR · C2C | RED→GREEN→REFACTOR, `/red-test-plan` C2C 4블록 | ✅ |
| Harness · Skills · Commands | pytest, 8 슬래시 커맨드, 2 Skills | ✅ |
| PRD · doc · Export | `doc/`, `Report/01~03` | ✅ |

### 5.2 Out of Scope

| 항목 | 사유 |
|------|------|
| **전체 마방진 솔버** · step B 이후 · 빈칸 자동 완성 | Mom Test 표면 문제; step A만 Entity 실험 범위 |
| **UI** · CLI · 독립 앱 | 제품화 범위 밖 |
| **배포** · CI | 세션 3 범위 밖 |
| Rule · Command 문서 자동 생성 | 별도 세션 |
| 빈칸 **개수=2** 강제 검증 | `0` 1개 이상 → `incomplete`만 |
| F4: fail/incomplete 시 **선별 합 값** 반환 | API 계약 미포함 |
| 1~16 **중복·범위 밖** 검증 | Entity 규칙 언급; 테스트 범위 밖 |
| **UI Track** 테스트 | PRD Logic Track only |

---

## 6. 아키텍처 (ECB)

```
┌─────────────────────────────────────────────────────────────┐
│  Boundary                                                    │
│  tests/test_validate_lines.py  ·  tests/entity/             │
│  tests/conftest.py (G1)                                      │
└──────────────────────────┬──────────────────────────────────┘
                           │ 공개 API만 assert
┌──────────────────────────▼──────────────────────────────────┐
│  Control — src/validate_lines.py                            │
│  validate_lines(grid) → { status, failed_lines }            │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  Entity                                                      │
│  entity/validation.py  — MAGIC_CONSTANT, compute_line_sum   │
│  find_blank_coords.py    — 빈칸 (row,col) 1-indexed         │
│  solve_step_a.py         — 첫 빈칸 행합 value (step A)      │
└─────────────────────────────────────────────────────────────┘
```

### 6.1 8계층 매핑

| 계층 | 상태 | 산출물 |
|------|:----:|--------|
| Mom Test / 페르소나 | ✅ | `Report/MomTest_STEP1_*.md` |
| 주제 · R-G-I-O | ✅ | 워크북, 본 PRD |
| **Rule** | ✅ | `.cursorrules`, §7 |
| **Command** | 🔶 | TDD·Export 8종; `/verify-magic-square` 미구현 |
| **Skill** | ✅ | `magic-square-tdd`, `magic-square-docs` |
| **Test Loop** | ✅ | Boundary 5 + Entity 2 (§9) |
| Agent / 배포 | — | 범위 밖 |

### 6.2 알려진 ECB 부채

| 항목 | 내용 |
|------|------|
| `solve_step_a` → `validate_lines` import | `MAGIC_CONSTANT`를 Control에서 가져옴; Entity 공용(`entity.validation`)으로 이동 권장 |
| blank row-major 스캔 | `find_blank_coords`와 `solve_step_a` 중복 |

---

## 7. Entity — 도메인 규칙

### 7.1 격자

- 형식: 4×4 `list[list[int]]`
- `0`: 빈칸 · 채워진 칸: `1`~`16` (중복·범위 밖 = 도메인 위반, 테스트 범위 밖)

### 7.2 마법상수 · 10선

- `MAGIC_CONSTANT = 34` (`src/entity/validation.py`; `validate_lines` re-export)
- 10선: `R1~R4`, `C1~C4`, `D1`, `D2` — **전수 검사 필수**

| ID | 인덱스 |
|----|--------|
| R1~R4 | `grid[row][col]`, row=0..3 |
| C1~C4 | col=0..3 |
| D1 | `(0,0)(1,1)(2,2)(3,3)` |
| D2 | `(0,3)(1,2)(2,1)(3,0)` |

### 7.3 상태 판정 (`validate_lines`)

| 조건 | status | failed_lines |
|------|--------|--------------|
| `0` 1개 이상 | `incomplete` | `[]` (최소 계약: status만 assert) |
| 10선 모두 34 | `pass` | `[]` |
| 하나 이상 ≠ 34 | `fail` | 불일치 선 ID 목록 |

### 7.4 Entity API — `find_blank_coords`

```python
find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]
```

- `0` 위치를 **1-indexed (row, col)**, **row-major** 순

### 7.5 Entity API — `compute_line_sum`

```python
compute_line_sum(grid: list[list[int]], line_id: str) -> int
```

- 단일 선 합; `line_id` ∈ `LINE_IDS`

### 7.6 Entity API — `solve_step_a`

```python
solve_step_a(grid: list[list[int]]) -> dict
# {"status": "success", "coord": (row, col), "value": int}  # 1-indexed
```

- row-major **첫** 빈칸에 대해 **행합 34**로 `value` 계산 (격자 변경 없음)

---

## 8. Control — API 계약

### 8.1 진입점

```python
from src.validate_lines import validate_lines, MAGIC_CONSTANT, LINE_IDS

def validate_lines(grid: list[list[int]]) -> dict: ...
```

### 8.2 반환값

```python
{"status": "pass" | "fail" | "incomplete", "failed_lines": ["R1", "D1", ...]}
```

### 8.3 기능 요구사항

| ID | 요구사항 | 우선순위 | 상태 |
|----|----------|:--------:|:----:|
| F1 | 10선 합 **전수** 계산·검증 | P0 | ✅ |
| F2 | 10선 모두 34 → `pass`, `[]` | P0 | ✅ |
| F3 | 합 ≠ 34 선 ID → `failed_lines` | P0 | ✅ (R1; C1~C4 후보 RED) |
| F4 | fail/incomplete 시 **합 값** 반환 | P2 | ❌ 범위 밖 |
| F5 | `0` 존재 → `incomplete` | P0 | ✅ |
| F6 | D1·D2 **생략 금지** | P0 | ✅ |
| F7 | 행 불일치 → 행 ID 포함 | P0 | ✅ (R1) |

### 8.4 Entity 기능 (Test ID)

| ID | 요구사항 | 상태 |
|----|----------|:----:|
| D-LOC-01 | G1 → `[(2,3),(4,4)]` | ✅ |
| D-SOL-01 | G1 step A → `(2,3)`, `11` | ✅ |
| D-LINE-C2-01 | C2 열 fail + `"C2" in failed_lines` | 🔲 RED 후보 |

---

## 9. Boundary · Entity — Test Loop

### 9.1 Boundary — `tests/test_validate_lines.py`

| ID | 테스트 함수 | 기대 |
|----|-------------|------|
| TC1 | `test_tc1_all_ten_lines_pass` | `pass`, `[]` |
| TC2 | `test_tc2_rows_cols_ok_diagonal_d1_fails` | `fail`, `"D1" in failed_lines` |
| TC3 | `test_tc3_rows_cols_ok_diagonal_d2_fails` | `fail`, `"D2" in failed_lines` |
| — | `test_incomplete_when_blank_present` | `incomplete` |
| — | `test_fail_includes_r1_when_row_sum_not_34` | `fail`, `"R1" in failed_lines` |

### 9.2 Entity — `tests/entity/`

| Test ID | 테스트 함수 | Given | Then |
|---------|-------------|-------|------|
| D-LOC-01 | `test_d_loc_01_find_blank_coords_returns_g1_blanks` | `grid_g1` | `[(2,3),(4,4)]` |
| D-SOL-01 | `test_d_sol_01_step_a_success` | `grid_g1` | `success`, `(2,3)`, `11` |

### 9.3 G1 격자 (`tests/conftest.py`)

```
16  3  2 13
 5 10  0  8   ← (2,3)
 9  6  7 12
 4 15 14  0   ← (4,4)
```

### 9.4 TC1~TC3 픽스처

**TC1_PASS_GRID** — 표준 4×4 마방진 (G1의 빈칸 채운 완성형과 동일).

**TC2_D1_FAIL_GRID** · **TC3_D2_FAIL_GRID** — `Report/01.REPORT.md` 설계 노트 참조.

### 9.5 pytest

```bash
python -m pytest tests/ -v
# → 7 passed
```

---

## 10. TDD · 개발 프로세스

### 10.1 Phase 규칙

| Phase | 수정 허용 | 금지 |
|-------|-----------|------|
| **RED** | `tests/` | `src/` |
| **GREEN** | `src/` | `tests/` 수정·10선 생략 |
| **REFACTOR** | `src/` (동작 불변) | API·Entity 변경 |

### 10.2 ARRR · C2C (`/red-test-plan`)

1. **Arrange (Ask)** — PRD FR·Test Loop 갭·pytest
2. **Red** — C2C 4블록 (Rule1~3, Track B, 플랜, ECB·Mock)
3. **Run** — pytest
4. **Report** — `/export` · `/red-skeleton` 준비

필수 선언: `Phase: red | Layer: {entity|boundary} | Track: {Logic|UI}`

### 10.3 슬래시 커맨드

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

### 10.4 Skills

- `.cursor/skills/magic-square-tdd/SKILL.md`
- `.cursor/skills/magic-square-docs/SKILL.md`

SSOT: 본 PRD, `.cursorrules`, `doc/PRD.md` (Skills 내 `docs/` 별칭 → `doc/` 통일 권장)

---

## 11. 프로젝트 구조

```
MagicSquare_xx/
├── doc/
│   ├── PRD.md
│   └── README.md
├── src/
│   ├── entity/
│   │   └── validation.py       ← MAGIC_CONSTANT, compute_line_sum
│   ├── validate_lines.py       ← Control
│   ├── find_blank_coords.py    ← Entity D-LOC
│   └── solve_step_a.py         ← Entity D-SOL step A
├── tests/
│   ├── conftest.py             ← G1_GRID, grid_g1
│   ├── test_validate_lines.py  ← Boundary (5)
│   └── entity/
│       ├── test_d_loc_01.py
│       └── test_d_sol_01.py
├── Report/                     ← 01~03.REPORT.md, Mom Test, 워크북
├── Prompting/                  ← Export Transcript, STEP 프롬프트
├── .cursorrules
├── .cursor/commands/           ← 8 commands
├── .cursor/skills/
└── pyproject.toml
```

---

## 12. 워크북 ↔ 계약 갭

| 구분 | 워크북 | PRD v0.2 (채택) |
|------|--------|-----------------|
| Input | 목표 합 34 | `MAGIC_CONSTANT` 상수 |
| Input | 빈칸 2개 | `0` 1개 이상 → `incomplete` |
| Output | 10항목별 합 | fail 시 선 ID만 |
| Output | 실패 합 값 | F4 — 범위 밖 |
| 솔버 | 표면 문제 | **step A만** Entity In Scope |
| TC3 | 부분 검증 API | 10선 전검; D2 생략 **구현** 감지 |

---

## 13. 마일스톤 · 현재 상태

| 단계 | 상태 |
|------|:----:|
| Mom Test · 워크북 · Harness · Skills · Commands | ✅ |
| Export 01 · 02 · 03 | ✅ |
| Boundary RED → GREEN (5 tests) | ✅ |
| Entity D-LOC-01 · D-SOL-01 | ✅ |
| REFACTOR — `entity/validation.py` extract | ✅ |
| **pytest 전체** | ✅ **7 passed** |

```bash
python -m pytest tests/ -v
# → 7 passed in ~0.03s
```

**다음 RED 후보:** D-LINE-C2-01 (FR-F3) · D-SOL-02 step B · C1~C4 열 fail 확대

---

## 14. 향후 검토 (v0.3+)

- [ ] Mom Test Q3 보완 → 실패 메시지·UX
- [ ] F4: `failed_line_sums` 확장
- [ ] `MAGIC_CONSTANT` Entity 단일 SSOT (`solve_step_a` import 정리)
- [ ] blank 스캔 공통화 (`find_blank_coords` 재사용)
- [ ] `TC1_PASS_GRID` ↔ `G1_GRID` conftest 통합
- [ ] PRD §5.2 vs Entity step A 범위 문서 정합 유지

---

## 15. 용어

| 용어 | 정의 |
|------|------|
| 부분 마방진 | 빈칸(`0`)이 남은 4×4 격자 |
| G1 | 빈칸 `(2,3)`, `(4,4)` — TC1 변형 |
| 10선 | 행 4 + 열 4 + 대각선 2 |
| Test Loop | Boundary 5 + Entity 2 |
| C2C | Contract-to-Code — FR → To-Do → Given/When/Then |
| ARRR | Arrange → Red → Run → Report |
| ECB | Entity–Control–Boundary |

---

*본 PRD는 MagicSquare_xx의 SSOT이다. 충돌 시 **§7~§9 API·Test Loop 계약** → `.cursorrules` 순.*
