# TDD RED — validate_lines 실패 테스트 작성

`validate_lines(grid)` 의 **새 동작**을 검증하는 실패 테스트를 `tests/` 에만 추가한다.
설계·계약은 `.cursorrules` 와 `Report/Session3_Workbook_MagicSquare_xx.md` 를 따른다.

---

## 필수 선언 (응답 첫 줄)

```
Phase: RED | Target: validate_lines | Track: <logic|boundary|incomplete>
```

- `Track`: 이번 테스트가 다루는 관심사 (예: `logic`=10선 합, `boundary`=dict 계약, `incomplete`=빈칸 0)

---

## AAA 절차

한 번에 **테스트 함수 1개**만 추가한다.

1. **Arrange** — 4×4 `grid` 와 기대 결과를 확정한다.
   - 도메인: `0`=빈칸, 1~16, 마법상수 34
   - 10선 ID: R1~R4, C1~C4, D1, D2
   - API: `{"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}`
2. **Act** — `result = validate_lines(grid)` 호출 (공개 API만).
3. **Assert** — `result["status"]`, `result["failed_lines"]` 를 **엄격히** 검증한다.
4. **Confirm RED** — `pytest` 로 **FAIL** 을 확인하고 보고한다. 통과시키려 하지 않는다.

---

## pytest 예시

```bash
# 추가한 테스트 1개만
pytest tests/test_validate_lines.py::test_<함수명> -v

# 전체 스위트 (기존 RED 포함)
pytest tests/test_validate_lines.py -v
```

기대 출력 예 (RED 성공):

```
FAILED tests/test_validate_lines.py::test_<함수명> - NotImplementedError
# 또는
FAILED ... - AssertionError: assert 'fail' == 'pass'
```

---

## 테스트 작성 예시 (AAA)

```python
def test_<동작을_설명하는_이름>():
    # Arrange
    grid = [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "pass"
    assert result["failed_lines"] == []
```

Test Loop 참고 (이미 있으면 중복 추가 금지):

| ID | 시나리오 | 기대 |
|----|----------|------|
| TC1 | 10선 모두 합 34 | `pass`, `failed_lines == []` |
| TC2 | 행·열 OK, D1 불일치 | `fail`, `"D1" in failed_lines` |
| TC3 | 행·열 OK, D2 불일치 | `fail`, `"D2" in failed_lines` |
| — | 빈칸 `0` 존재 | `incomplete` |

---

## 보고 형식

작업 후 아래 항목을 **한국어**로 간결히 보고한다.

```
Phase: RED | Target: validate_lines | Track: <...>

- 추가 테스트: test_<함수명>
- Arrange: grid 요약 (4×4, 빈칸/특이값 한 줄)
- Assert: 기대 status / failed_lines
- pytest: FAIL — <NotImplementedError | AssertionError 등 한 줄>
- 변경 파일: tests/test_validate_lines.py (tests/ 만)
```

---

## 금지

- `src/` 수정 (구현·스텁·import 변경 포함)
- assert 완화 (`==` → `in` 축소, 조건 삭제, `or` 로 우회)
- `@pytest.mark.skip`, `xfail`, 테스트 삭제로 RED 숨기기
- 한 번에 여러 테스트 함수 추가
- private 헬퍼·내부 구현 직접 테스트 (공개 API `validate_lines` 결과 dict 만)
