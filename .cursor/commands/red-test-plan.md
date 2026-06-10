# RED Test Plan — C2C 설계표 · 테스트 플랜 (Ask)

**추가 입력 없이 즉시 실행.** 사용자가 `/red-test-plan` 만 입력했다.
세션 주제·Test ID·다음 RED 시나리오는 **현재 채팅·저장소·PRD**에서 자동 추출한다. 추가 질문·확인 요청 금지.

**역할:** ARRR **A**단계 (Ask = RED ③) — **C2C 설계표·테스트 플랜만** 작성. `tests/`·`src/` **파일 생성·수정 금지**.

SSOT: `.cursorrules`, `doc/PRD.md` (`docs/PRD.md` 별칭), `Report/Session3_Workbook_MagicSquare_xx.md`

형식 참고: `.cursor/commands/tdd-red.md`

---

## 필수 선언 (응답 첫 줄)

```
Phase: red | Layer: {entity|boundary} | Track: {Logic|UI}
```

| 필드 | MagicSquare_xx 기본값 | 설명 |
|------|----------------------|------|
| `Layer` | `entity` | Control·Entity 검증 (`validate_lines` 도메인·10선). API dict 계약만이면 `boundary` |
| `Track` | `Logic` | 10선 합·status·failed_lines. UI·CLI는 범위 밖 → `UI` Track 금지 |

> **Track A (boundary):** 본 커맨드 본문을 그대로 재사용하고, 필수 선언의 `Layer`만 `boundary`로 바꾼다. C2C·Track B·테스트 플랜·ECB 점검 형식은 동일.

---

## ARRR 절차 (Ask — 파일 수정 없음)

1. **Arrange (Ask)**
   - `tests/test_validate_lines.py`·`src/validate_lines.py`·`doc/PRD.md` §8.3(F1~F7)·§9 Test Loop·최근 pytest 결과 확인
   - **미커버 FR·Test Loop 갭 1건** 선정 (기존 `test_*` 와 중복 금지)
   - Entity: 4×4, `0`=빈칸, 1~16, `MAGIC_CONSTANT=34`, 10선 `R1~R4`·`C1~C4`·`D1`·`D2`
   - API: `{"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}`
2. **Red (계획만)**
   - 아래 **출력 4블록**을 채팅에 작성 (코드·파일 변경 없음)
3. **Run (상태 확인만)**
   - 필요 시 `pytest tests/test_validate_lines.py -v` 로 RED/GREEN 현황만 기록 (테스트 코드 변경 금지)
4. **Report**
   - 4블록 출력 후 완료 한 줄: **`/red-skeleton` 으로 넘길 준비됐다**

---

## C2C Rule1~3 (설계 규칙)

| Rule | 내용 |
|------|------|
| **Rule1** | PRD **FR(F1~F7) 또는 SC** 를 **1문장 인용**하고, 이번 RED의 **To-Do는 정확히 1개**만 |
| **Rule2** | Test ID는 **Given / When / Then** 3행으로 분해 (공개 API `validate_lines` 호출 기준) |
| **Rule3** | 기존 `tests/test_validate_lines.py` 의 `test_*`·`TC*_GRID` 와 **중복·assert 완화 없음** |

---

## pytest (상태 확인만)

```bash
pytest tests/test_validate_lines.py -v
```

기록 예:

```
5 failed — NotImplementedError (RED, TC1~TC3·incomplete·R1 존재)
# 또는
N passed — GREEN 진행 중, 다음 FR 갭 선정
```

---

## Test Loop · FR 참조 (자동 추출용)

| ID / FR | 시나리오 | 기존 테스트 | 기대 |
|---------|----------|-------------|------|
| TC1 / F2 | 10선 모두 합 34 | `test_tc1_all_ten_lines_pass` | `pass`, `failed_lines == []` |
| TC2 / F3,F6 | 행·열 OK, D1 불일치 | `test_tc2_rows_cols_ok_diagonal_d1_fails` | `fail`, `"D1" in failed_lines` |
| TC3 / F6 | 행·열 OK, D2 불일치 | `test_tc3_rows_cols_ok_diagonal_d2_fails` | `fail`, `"D2" in failed_lines` |
| F5 | 빈칸 `0` 존재 | `test_incomplete_when_blank_present` | `incomplete` |
| F7 | R1 행 합 ≠ 34 | `test_fail_includes_r1_when_row_sum_not_34` | `fail`, `"R1" in failed_lines` |
| F3 (갭) | C1~C4 열 불일치 | *(없으면 후보)* | `fail`, `"C1"` 등 in `failed_lines` |
| F1 | 10선 전수 (생략 감지) | TC3로 간접 | 구현 D2 생략 시 TC3 RED |

---

## 출력 4블록 (채팅 — 표 형식 필수)

에이전트는 `/red-test-plan` 실행 시 아래 **4블록을 순서대로** 채운다.

### 블록 1 — C2C (Rule1~3)

| 항목 | 내용 |
|------|------|
| **PRD FR 인용** | 예: `F3` — "합 ≠ 34인 선 ID를 `failed_lines`에 포함한다" (`doc/PRD.md` §8.3) |
| **To-Do (1개)** | 예: C2 열 합 불일치 격자에서 `fail` + `"C2" in failed_lines` 검증 테스트 추가 |
| **Test ID** | 예: `TC-C2-001` (또는 `TC4`) |
| **Given** | 4×4 격자 요약 — TC1 변형, C2 열만 합 ≠ 34 |
| **When** | `result = validate_lines(grid)` |
| **Then** | `result["status"] == "fail"` and `"C2" in result["failed_lines"]` |

### 블록 2 — Track B 표

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|-----------|--------------|-----------|----------------------|
| `<Test ID>` | `validate_lines` | `<Given 한 줄>` → `<Then 한 줄>` | 10선 전수·`MAGIC_CONSTANT=34`·공개 API dict 계약 | `NotImplementedError` 또는 `AssertionError: assert 'fail' == 'pass'` |

### 블록 3 — 테스트 플랜

| 항목 | 내용 |
|------|------|
| **파일 경로** | `tests/test_validate_lines.py` |
| **함수명** | `test_<동작_설명>` (snake_case) |
| **픽스처 / conftest** | 모듈 상수 `TCx_*_GRID` (기존 `TC1_PASS_GRID` 패턴). `conftest.py` 없음 — 필요 시 인라인 grid |
| **pytest (단일)** | `pytest tests/test_validate_lines.py::test_<함수명> -v` |
| **pytest (RED 묶음)** | `pytest tests/test_validate_lines.py -v` (전체 스위트; 신규 1건 포함 예정) |
| **RED 묶음 범위** | 기존 N failed + 신규 1건 = N+1 failed (GREEN 전까지 전부 FAIL 유지) |

### 블록 4 — ECB · Mock 점검

| 점검 | Logic Track (`Layer: entity`) | boundary Track (`Layer: boundary`) |
|------|------------------------------|-------------------------------------|
| **계층** | Boundary → Control `validate_lines` → Entity 규칙 | 동일 API, dict 키·타입·값域 계약 |
| **Domain Mock** | **금지** — `validate_lines` 실제 호출, Mock/patch/stub 대체 금지 | **금지** — 공개 API 그대로 호출 |
| **테스트 대상** | `validate_lines` 결과 dict 만 assert | `status`·`failed_lines` 키 존재·타입·허용값 |
| **private 접근** | 금지 | 금지 |

**E001~E005 emit 금지** — 아래 위반 코드가 **발생하면 안 됨** (플랜·후속 RED에서):

| Code | 위반 (emit 하면 안 됨) |
|------|------------------------|
| E001 | Logic Track에서 Domain Mock·patch·`validate_lines` 대체 |
| E002 | private 헬퍼·내부 함수 직접 테스트 |
| E003 | RED 계획에 `src/` 수정·구현·스텁 변경 포함 |
| E004 | 10선 전수 검증 FR(F1,F6) 갭인데 대각선·행·열 일부만 검증하는 시나리오 |
| E005 | skip·xfail·assert 완화·RED 숨기기 권장 |

점검 결과 한 줄: `ECB·Mock: OK (E001~E005 미발생)` 또는 해당 Code 명시 후 **플랜 수정**.

---

## 완료 보고 (채팅 마지막 줄)

```
Phase: red | Layer: <entity|boundary> | Track: <Logic|UI>

[블록 1 C2C 표]
[블록 2 Track B 표]
[블록 3 테스트 플랜 표]
[블록 4 ECB·Mock 점검 표]

- pytest 현황: <한 줄>
- 변경 파일: 없음 (계획만)
- /red-skeleton 으로 넘길 준비됐다
```

---

## 금지

- `src/` **수정** (구현·스텁·import 포함)
- **GREEN** / **REFACTOR** 단계 작업·언급을 실행 지시로 포함
- `@pytest.mark.skip`, `xfail`, assert 완화·테스트 삭제 **권장**
- `tests/`·`src/` **파일 생성·수정** (계획은 채팅만)
- 사용자에게 시나리오·함수명 **추가 질문**
- 한 번에 **여러 Test ID** 계획 (C2C To-Do **1개**만)
- 솔버·UI·배포·범위 밖 FR (F4 등) 계획
- Logic Track에서 **Domain Mock** 사용 계획

---

## 다음 커맨드

| 커맨드 | 역할 |
|--------|------|
| `/red-skeleton` | 블록 3 플랜대로 테스트 **골격** 1개 추가 (`tests/`만) |
| `/tdd-red` | 블록 3 플랜대로 완전한 실패 테스트 1개 추가 (`tests/`만) |
