# MagicSquare_xx — Product Requirements Document (PRD)

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_xx |
| **버전** | 0.1 (세션 3 — 10선 검증) |
| **작성일** | 2026-06-10 |
| **최종 갱신** | 2026-06-10 |
| **SSOT 역할** | Mom Test·워크북·`.cursorrules`·API 계약·Test Loop의 단일 요구사항 기준 |
| **관련 문서** | `Report/MomTest_STEP1_MagicSquare_xx.md`, `Report/Session3_Workbook_MagicSquare_xx.md`, `Report/01.REPORT.md`, `Report/02.REPORT.md`, `.cursorrules`, `doc/README.md` |

---

## 1. 개요

MagicSquare_xx는 4×4 **부분 마방진** 격자에서 행·열·대각선 **10개 선**의 합이 마법상수 34인지 **빠짐없이** 검증하는 라이브러리이다. Mom Test에서 드러난 “검증 항목 하나를 빠뜨려 20분을 낭비하는” 문제를, **전수 검증 + 실패 선 식별**로 조기에 드러내는 것이 목적이다.

이번 범위는 **ECB 패턴의 Control 계층**(`validate_lines`)과 **Boundary**(pytest Test Loop) 구현·검증이다. 솔버, UI, 배포는 범위 밖이다.

### 1.1 프로젝트 맥락 (Mom Test 과제)

| 항목 | 내용 |
|------|------|
| 과제 | 4×4 마방진에서 빈칸 2개를 찾아 1~16으로 채워 완성 (목표 합 = 34) |
| 설계 패턴 | ECB (Entity–Control–Boundary) |
| 실습 목표 | ECB 분류, 실패 조건(Problem Recognition) 도출 |

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

### 2.5 표면 문제 (이번 범위 밖 — 제품 정의 금지)

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
| **Output** | `status` (`pass` \| `fail` \| `incomplete`) + `failed_lines` (실패·미완성 관련 선 ID 리스트) |

---

## 4. 성공 기준

| # | 기준 | Mom Test 연결 | 검증 방법 |
|---|------|---------------|-----------|
| SC1 | 검증 범위에 **대각선 2개(D1, D2)가 명시·실행**되며, 행·열만 맞고 대각선 하나만 틀린 격자에서 **fail + 실패 대각선 식별** | 증거 ③ "대각선 하나를 빼먹어서" | TC2, TC3 |
| SC2 | ECB·실습과 동일 맥락(빈칸, 합 34, 4×4)의 **재현 시나리오**가 Test Loop에 포함 | 증거 ①·② | TC1~TC3 픽스처 격자 |
| SC3 | 행·열만 확인한 **부분 검증**으로는 "완성" 판정 불가 — 10항목 전수 검증으로 틀림 특정 | 증거 ③ "20분 날렸어" | TC3 (D2 생략 시 fail 미검출 → Rule 위반) |
| SC4 | 빈칸(`0`)이 하나라도 있으면 **완성 판정 불가** → `incomplete` | — | `test_incomplete_when_blank_present` |
| SC5 | 행·열·대각선 외 **개별 선(행) 불일치** 시 해당 선 ID를 `failed_lines`에 포함 | Goal "어느 항목인지" | `test_fail_includes_r1_when_row_sum_not_34` |

---

## 5. 범위

### 5.1 In Scope (이번 PRD · 세션 3)

| 항목 | 설명 | 상태 |
|------|------|:----:|
| Entity 규칙 | 4×4 격자, 0=빈칸, 1~16, 마법상수 34, 10선 전수 검사 | ✅ 정의 |
| Control API | `src/validate_lines.py` — `validate_lines(grid)` | 🔲 스텁 |
| Boundary 테스트 | `tests/test_validate_lines.py` — TC1~TC3 + incomplete + R1 fail | ✅ RED |
| TDD 워크플로 | RED → GREEN → REFACTOR (`.cursorrules`, TDD Skill) | ✅ |
| Harness | `pyproject.toml`, pytest 설정 | ✅ |
| Cursor Skills | `magic-square-tdd`, `magic-square-docs` | ✅ |
| Cursor Commands | TDD 7종 + `/export` (§10.3) | ✅ |
| PRD · doc | `doc/PRD.md`, `doc/README.md` | ✅ |
| 세션 Export | `Report/01.REPORT.md`, `Report/02.REPORT.md` | ✅ |

### 5.2 Out of Scope (명시적 제외)

| 항목 | 사유 |
|------|------|
| 마방진 **솔버** · 빈칸 자동 채우기 | Mom Test 표면 문제 |
| **UI** · 독립 앱 · CLI | 제품화 범위 밖 |
| **배포** · CI 파이프라인 | 세션 3 범위 밖 |
| Rule · Command **문서 자동 생성** | 별도 세션 |
| 8계층 중 Agent · 전체 구현 · ECB 분류 도구 | 워크북 8계층 표 "범위 밖" |
| 빈칸 **개수=2** 강제 검증 | Input은 0 포함 여부만 검사; 개수는 도메인 가정 |
| 10선 **개별 합 값** 반환 (pass 시) | 현재 API 계약에 미포함 (향후 확장 후보) |
| 도메인 위반(1~16 범위 밖, 중복) 검증 | Entity 규칙에 언급; Boundary 테스트 범위 밖 |

---

## 6. 아키텍처 (ECB)

```
┌─────────────────────────────────────────────────────────┐
│  Boundary — tests/test_validate_lines.py                │
│  공개 API validate_lines() 결과 dict 만 assert           │
└──────────────────────────┬──────────────────────────────┘
                           │ 호출
┌──────────────────────────▼──────────────────────────────┐
│  Control — src/validate_lines.py                        │
│  validate_lines(grid) → { status, failed_lines }        │
└──────────────────────────┬──────────────────────────────┘
                           │ Entity 규칙 준수
┌──────────────────────────▼──────────────────────────────┐
│  Entity — 도메인 불변 규칙                               │
│  4×4, 0=빈칸, 1~16, 합=34, 10선 R1~R4·C1~C4·D1·D2      │
└─────────────────────────────────────────────────────────┘
```

### 6.1 8계층 매핑 (세션 3)

| 계층 | 상태 | 산출물 |
|------|:----:|--------|
| Mom Test / 페르소나 | ✅ 완료 | `Report/MomTest_STEP1_MagicSquare_xx.md`, `Report/MomTest_STEP1_Questions_MagicSquare_xx.md` |
| 주제 · R-G-I-O | ✅ 완료 | `Report/Session3_Workbook_MagicSquare_xx.md`, 본 PRD |
| **Rule** | ✅ 정의 | Entity 규칙 (`.cursorrules`, §7) |
| **Command** | 🔶 부분 | TDD·Export 슬래시 커맨드 8종 (§10.3). 워크북 예시 `/verify-magic-square`는 미구현 |
| **Skill** | ✅ | `.cursor/skills/magic-square-tdd`, `magic-square-docs` |
| **Test Loop** | ✅ 정의 | TC1~TC3 + incomplete + R1 fail (§9) |
| Agent / 구현 / 배포 | — | 범위 밖 |

---

## 7. Entity — 도메인 규칙

### 7.1 격자

- 형식: 4×4 정수 2차원 리스트 `list[list[int]]`
- `0`: 빈칸 (미완성)
- 채워진 칸: `1`~`16` (중복·범위 밖 값은 도메인 위반 — 본 세션 테스트 범위 밖)

### 7.2 마법상수

- `MAGIC_CONSTANT = 34`
- pass 판정 대상: 각 선(行)의 합이 34

### 7.3 검증 선 10개 (전수 검사 필수)

| ID | 설명 | 인덱스 |
|----|------|--------|
| R1~R4 | 행 1~4 | `grid[row][col]`, row=0..3 |
| C1~C4 | 열 1~4 | `grid[row][col]`, col=0..3 |
| D1 | 좌상→우하 대각선 | `(0,0),(1,1),(2,2),(3,3)` |
| D2 | 우상→좌하 대각선 | `(0,3),(1,2),(2,1),(3,0)` |

**규칙:** 10선 중 **하나라도 검사를 생략하면 Rule 위반**이다.

### 7.4 상태 판정 규칙

| 조건 | status | failed_lines |
|------|--------|--------------|
| 격자에 `0`이 1개 이상 | `incomplete` | 미완성 관련 선 (구현 시 정책에 따름; 최소 계약은 status만 assert) |
| 10선 모두 합 34 | `pass` | `[]` |
| 하나 이상 합 ≠ 34 | `fail` | 합이 34가 아닌 선 ID 포함 (예: `["D1"]`, `["R1"]`) |
| 행·열만 34, 대각선 1개만 ≠ 34 | `fail` | 해당 대각선 ID 포함 |

---

## 8. Control — API 계약

### 8.1 진입점

```python
# src/validate_lines.py
MAGIC_CONSTANT = 34

LINE_IDS = (
    "R1", "R2", "R3", "R4",
    "C1", "C2", "C3", "C4",
    "D1", "D2",
)

def validate_lines(grid: list[list[int]]) -> dict:
    ...
```

현재 구현: `raise NotImplementedError` (GREEN 대기).

### 8.2 반환값

```python
{
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": ["R1", "D1", ...],  # pass 시 []
}
```

### 8.3 기능 요구사항

| ID | 요구사항 | 우선순위 | 상태 |
|----|----------|:--------:|:----:|
| F1 | 4×4 격자의 10선 합을 **전수** 계산·검증한다 | P0 | 🔲 미구현 |
| F2 | 10선 모두 합 34이면 `status="pass"`, `failed_lines=[]` | P0 | 🔲 |
| F3 | 합 ≠ 34인 선 ID를 `failed_lines`에 포함한다 | P0 | 🔲 |
| F4 | `fail`/`incomplete` 시 실패 선의 **합 값**을 함께 반환한다 | P2 (향후) | ❌ 범위 밖 |
| F5 | 격자에 `0`이 있으면 `status="incomplete"` | P0 | 🔲 |
| F6 | 대각선 D1·D2 검증을 **생략하지 않는다** (TC3으로 검증) | P0 | 🔲 |
| F7 | 행(R1~R4) 불일치 시 해당 행 ID를 `failed_lines`에 포함한다 | P0 | 🔲 |

> **F4 참고:** `Report/02.REPORT.md` 리뷰에서 워크북 Output과의 갭으로 지적됨. 현재 Boundary 테스트·`.cursorrules` 계약에는 **선 ID만** 포함. F4는 후속 PRD 버전에서 `failed_line_sums` 등으로 확장 검토.

---

## 9. Boundary — Test Loop

### 9.1 테스트 파일

- 경로: `tests/test_validate_lines.py`
- 대상: 공개 API `validate_lines`만 검증 (내부 헬퍼 private)
- 현재: **5개** 테스트, 모두 RED (`NotImplementedError`)

### 9.2 시나리오

| ID | 테스트 함수 | 설명 | 격자 | 기대 |
|----|-------------|------|------|------|
| **TC1** | `test_tc1_all_ten_lines_pass` | 10선 모두 합 34 | `TC1_PASS_GRID` (표준 4×4 마방진) | `status=="pass"`, `failed_lines==[]` |
| **TC2** | `test_tc2_rows_cols_ok_diagonal_d1_fails` | 행·열 OK, **D1** 불일치 (인터뷰 재현) | `TC2_D1_FAIL_GRID` | `status=="fail"`, `"D1" in failed_lines` |
| **TC3** | `test_tc3_rows_cols_ok_diagonal_d2_fails` | 행·열 OK, **D2** 불일치 (대각선 생략 방지) | `TC3_D2_FAIL_GRID` | `status=="fail"`, `"D2" in failed_lines` |
| **—** | `test_incomplete_when_blank_present` | 빈칸 존재 | TC1에서 `[0][0]=0` | `status=="incomplete"` |
| **—** | `test_fail_includes_r1_when_row_sum_not_34` | R1 행 합 불일치 | TC1 기반, `[0][3]` 13→14 (합 35) | `status=="fail"`, `"R1" in failed_lines` |

### 9.3 픽스처 격자 (현재 코드)

**TC1_PASS_GRID** — 표준 4×4 마방진:

```
16  3  2 13
 5 10 11  8
 9  6  7 12
 4 15 14  1
```

**TC2_D1_FAIL_GRID** — 행·열 34, D1 불일치:

```
 8  8  9  9
 8  8  9  9
 8  8  9  9
10 10  7  7
```

**TC3_D2_FAIL_GRID** — 행·열 34, D2 불일치:

```
 1 12 11 10
14  5  6  9
 7  8 15  4
12  9  2 11
```

### 9.4 TC2·TC3 격자 설계 노트

행·열 합 34이면서 D1만 실패하고 1~16 중복 없는 4×4 격자는 **수학적으로 존재하지 않을 수 있음**. 따라서 테스트는 **행·열 34 + 특정 대각선 불일치** 구조로 D1/D2 검증 생략을 각각 감지한다 (`Report/01.REPORT.md`).

### 9.5 pytest 실행

```bash
# 전체
pytest tests/test_validate_lines.py -v

# 단일
pytest tests/test_validate_lines.py::test_tc1_all_ten_lines_pass -v
```

---

## 10. TDD · 개발 프로세스

### 10.1 Phase 규칙

| Phase | 수정 허용 | 금지 |
|-------|-----------|------|
| **RED** | `tests/` | `src/` 수정, assert 완화, skip, xfail |
| **GREEN** | `src/` | `tests/` 수정, 10선 생략 |
| **REFACTOR** | `src/` (동작 불변) | API·Entity 변경, 테스트 수정 |

### 10.2 ARRR 루프

1. **Arrange** — SSOT·pytest·격자·기대 dict·수정 파일 범위 확정
2. **Red** — 실패 테스트 작성 (`tests/`만)
3. **Run** — pytest 실행·구현·리팩터
4. **Report** — Phase 선언 + 세션 Export (`/export`)

### 10.3 슬래시 커맨드 (Cursor)

| 커맨드 | Phase | 역할 |
|--------|-------|------|
| `/red-test-plan` | RED | 다음 실패 테스트 계획만 (파일 수정 없음) |
| `/red-skeleton` | RED | 테스트 골격 1개 추가 (`tests/`) |
| `/tdd-red` | RED | 완전한 실패 테스트 1개 추가 (`tests/`) |
| `/green-minimal` | GREEN | 첫 FAIL 1개 최소 구현 (`src/`) |
| `/golden-master` | GREEN | 전체 스위트 ALL PASS |
| `/refactor-smell` | REFACTOR | smell 진단만 (`src/` 수정 없음) |
| `/refactor-safe` | REFACTOR | smell 1건 안전 정리 (`src/`, green 유지) |
| `/export` | EXPORT | Report + Transcript 생성 |

권장 순서:

```
/red-test-plan → /red-skeleton 또는 /tdd-red → /green-minimal → … → /golden-master
→ /refactor-smell → /refactor-safe → /export
```

### 10.4 Skills (Cursor Agent)

| Skill | 경로 | 역할 |
|-------|------|------|
| `magic-square-tdd` | `.cursor/skills/magic-square-tdd/SKILL.md` | TDD Phase·ARRR·커맨드 맵·Test Loop |
| `magic-square-docs` | `.cursor/skills/magic-square-docs/SKILL.md` | `/export`, Report·Transcript·체크리스트 템플릿 |

SSOT 참조: 본 PRD, `.cursorrules`, `Report/Session3_Workbook_MagicSquare_xx.md`

---

## 11. 프로젝트 구조

```
MagicSquare_xx/
├── doc/
│   ├── PRD.md                      ← 본 문서 (SSOT)
│   └── README.md                   ← doc 폴더 안내·API 요약
├── src/
│   └── validate_lines.py           ← Control (GREEN 대상, 현재 NotImplementedError)
├── tests/
│   └── test_validate_lines.py      ← Boundary (Test Loop, 5 tests)
├── Report/
│   ├── MomTest_STEP1_MagicSquare_xx.md
│   ├── MomTest_STEP1_Questions_MagicSquare_xx.md
│   ├── Session3_Workbook_MagicSquare_xx.md
│   ├── 01.REPORT.md                ← Harness·커서룰·TDD 커맨드 구축
│   ├── 02.REPORT.md                ← 워크북 vs validate_lines 계약 정합성 리뷰
│   └── README.md
├── Prompting/
│   ├── 01.Export-Transcript.md
│   ├── 02.Export-Transcript.md
│   ├── STEP1_*.md, STEP3_*.md      ← 세션 프롬프트·템플릿
│   └── README.md
├── .cursorrules                    ← Entity·Control·Boundary·TDD 규칙
├── .cursor/
│   ├── commands/                   ← TDD 7종 + export (8 files)
│   └── skills/
│       ├── magic-square-tdd/
│       └── magic-square-docs/
├── .gitignore
└── pyproject.toml                  ← pytest 설정 (testpaths, pythonpath)
```

---

## 12. 워크북 ↔ 계약 갭 (알려진 차이)

`Report/02.REPORT.md` 정합성 리뷰 기준. PRD v0.1은 **현재 API 계약**(`.cursorrules`, 테스트)을 SSOT로 채택한다.

| 구분 | 워크북 | PRD / 계약 (채택) |
|------|--------|-------------------|
| Input | `목표 합 = 34`를 Input 항목 | `MAGIC_CONSTANT` 상수, grid 단일 인자 |
| Input | `빈칸 2개` 조건 | `0` 1개 이상 → `incomplete` (개수 미검증) |
| Output | 10개 항목별 합 출력 | pass 시 sum 목록 없음; fail 시 선 ID만 |
| Output | 실패 시 합 값 | F4 — 향후 확장, 현재 범위 밖 |
| Output | `incomplete` 상태 | 워크북 미기술 → PRD·테스트에 포함 |
| Output | 줄 ID 규칙 | `R1~R4`, `C1~C4`, `D1`, `D2` (워크북 미정) |
| TC3 | "부분 검증" API 감지 | `validate_lines`는 항상 10선 전검; TC3는 D2 생략 **구현** 감지 |
| Test Loop | 픽스처 격자 미명시 | `tests/test_validate_lines.py`에 TC1~TC3 격자 정의 |

---

## 13. 마일스톤 · 현재 상태

| 단계 | 내용 | 상태 |
|------|------|:----:|
| STEP 1 | Mom Test 인터뷰·질문 뱅크 | ✅ |
| STEP 3 | 세션 3 워크북 (R-G-I-O, 8계층) | ✅ |
| Harness | pytest, src/tests 골격, `.cursorrules` | ✅ |
| TDD 커맨드 | 8종 슬래시 커맨드 (`.cursor/commands/`) | ✅ |
| Skills | `magic-square-tdd`, `magic-square-docs` | ✅ |
| PRD · doc | `doc/PRD.md`, `doc/README.md` | ✅ |
| Export 01 | Harness·커서룰·TDD 커맨드 세션 | ✅ |
| Export 02 | 워크북 vs 계약 정합성 리뷰 | ✅ |
| RED | TC1~TC3 + incomplete + R1 fail (5 tests) | ✅ |
| GREEN | `validate_lines` 구현 | 🔲 (`NotImplementedError`) |
| REFACTOR | 10선 검사 로직 정리 | 🔲 |

**현재 pytest:** `5 failed` — `NotImplementedError` (RED, GREEN 대기)

```bash
pytest tests/test_validate_lines.py -v
# → 5 failed in ~0.2s
```

**다음 단계:** GREEN — `src/validate_lines.py` 구현으로 5 테스트 통과 → REFACTOR → `/export`

---

## 14. 향후 검토 (PRD v0.2+)

- [ ] Mom Test Q3 보완: 틀림을 **언제·무엇을 보고** 알았는지 → 실패 메시지·UX 문구 검증
- [ ] F4: `fail`/`incomplete` 시 선별 **합 값** 반환 여부 결정
- [ ] Rule · Command 문서화 (`/verify-magic-square` 등)
- [ ] 워크북 Output 섹션을 본 PRD 계약에 맞게 갱신
- [ ] 도메인 위반(1~16 범위 밖, 중복) 검증 요구사항 추가 여부
- [ ] Skills 내 `docs/PRD.md` 참조를 `doc/PRD.md`로 통일

---

## 15. 용어

| 용어 | 정의 |
|------|------|
| 부분 마방진 | 빈칸(`0`)이 남아 있는 4×4 격자 |
| 마법상수 | 4×4 마방진에서 각 선의 목표 합 = **34** |
| 10선 | 행 4 + 열 4 + 대각선 2 |
| Test Loop | TC1~TC3 + incomplete + R1 fail pytest 시나리오 |
| ECB | Entity–Control–Boundary 패턴 |
| ARRR | Arrange → Red → Run → Report (TDD 실습 루프) |
| SSOT | Single Source of Truth — 본 PRD §7~§9 API 계약 |

---

*본 PRD는 MagicSquare_xx 세션 3의 단일 요구사항 기준(SSOT)이다. 구현·테스트·AI Skill은 본 문서와 `.cursorrules`가 충돌할 경우 **본 PRD §7~§9 API 계약**을 우선한다.*
