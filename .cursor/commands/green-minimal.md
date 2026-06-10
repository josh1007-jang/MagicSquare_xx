# GREEN Minimal — 최소 구현으로 RED 해소

**추가 입력 없이 즉시 실행.** 사용자가 `/green-minimal` 만 입력했다.
통과시킬 대상은 **가장 먼저 실패하는 테스트 1개**(또는 동일 원인 묶음)를 pytest에서 자동 선정한다. 추가 질문·확인 요청 금지.

SSOT: `.cursorrules`, `docs/PRD.md`(있을 때), `Report/Session3_Workbook_MagicSquare_xx.md`

---

## 필수 선언 (응답 첫 줄)

```
Phase: GREEN | Target: validate_lines | Track: minimal
```

---

## ARRR 절차

1. **Arrange**
   - `pytest tests/test_validate_lines.py -v` 로 **첫 FAIL** 테스트를 확인한다
   - Entity: 10선 전수, `MAGIC_CONSTANT = 34`, `0` → `incomplete`
   - 수정 범위: `src/validate_lines.py` (필요 시 최소 import만)
2. **Red** *(역방향 검증)*
   - 대상 테스트의 Arrange·Assert 를 다시 읽고 **테스트를 약화하지 않는** 최소 구현 범위를 정한다
3. **Run**
   - `src/validate_lines.py` 에 **통과에 필요한 최소 코드**만 추가한다 (`NotImplementedError` 제거)
   - `pytest tests/test_validate_lines.py::test_<함수명> -v` → **PASS**
   - 전체: `pytest tests/test_validate_lines.py -v` (나머지 FAIL 은 유지 가능)
4. **Report**
   - 아래 완료 보고 블록을 채팅에 출력한다

---

## pytest 예시

```bash
# 대상 1개만 GREEN
pytest tests/test_validate_lines.py::test_tc1_all_ten_lines_pass -v

# 전체 스위트
pytest tests/test_validate_lines.py -v
```

기록 예:

```
1 passed — test_tc1_all_ten_lines_pass GREEN
3 failed — 다음 RED/GREEN 대기
```

---

## 최소 구현 원칙

| 원칙 | 내용 |
|------|------|
| 한 번에 1 실패 | 첫 FAIL 1개(또는 동일 누락으로 묶인 세트)만 통과시킨다 |
| 10선 전수 | 행·열·대각선 **하나도 생략하지 않는다** (TC3 방지) |
| YAGNI | 다음 테스트를 위해 미리 일반화·헬퍼 추출하지 않는다 |
| 계약 유지 | 반환 dict 키 `status`, `failed_lines` 만 (Boundary) |

---

## 완료 보고 형식 (채팅)

```
Phase: GREEN | Target: validate_lines | Track: minimal

- 통과시킨 테스트: test_<함수명>
- 구현 요약: <한 줄 — 예: 10선 합 검사, incomplete 선판별>
- pytest (대상): PASS
- pytest (전체): <N passed, M failed — 한 줄>
- 변경 파일: src/validate_lines.py
```

---

## 금지

- `tests/` 수정 (assert 완화·삭제·skip·xfail)
- 한 번에 **모든 테스트** 통과를 목표로 과도한 추상화
- 10선 중 일부만 검사하는 **부분 구현**(대각선 생략 등)
- 솔버·빈칸 자동 채우기·UI
- REFACTOR 성격의 대규모 구조 변경 (이름·중복 정리는 `/refactor-safe` 에서)
