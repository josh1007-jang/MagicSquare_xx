# RED Skeleton — 실패 테스트 골격 추가

**추가 입력 없이 즉시 실행.** 사용자가 `/red-skeleton` 만 입력했다.
추가할 테스트 1건은 **현재 채팅·Test Loop 갭·pytest 실패**에서 자동 선정한다. 추가 질문·확인 요청 금지.

SSOT: `.cursorrules`, `docs/PRD.md`(있을 때), `Report/Session3_Workbook_MagicSquare_xx.md`

---

## 필수 선언 (응답 첫 줄)

```
Phase: RED | Target: validate_lines | Track: <logic|boundary|incomplete>
```

---

## ARRR 절차

1. **Arrange**
   - `tests/test_validate_lines.py` 에 없는 Test Loop·계약 갭 **1건**을 고른다
   - 4×4 `grid` 상수명·함수명 `test_<동작_설명>` 을 확정한다
2. **Red**
   - `tests/test_validate_lines.py` 에 **테스트 함수 1개 골격**만 추가한다
   - 골격: `# Arrange` / `# Act` / `# Assert` 주석 + `validate_lines` 호출 + **assert 1~2개**(엄격)
   - 격자가 길면 파일 상단에 `TCx_*_GRID` 상수로 분리 (기존 `TC1_PASS_GRID` 패턴 따름)
3. **Run**
   - `pytest tests/test_validate_lines.py::test_<함수명> -v` → **FAIL** 확인
4. **Report**
   - 아래 완료 보고 블록을 채팅에 출력한다

---

## pytest 예시

```bash
pytest tests/test_validate_lines.py::test_<함수명> -v
```

기대 출력 예 (RED 성공):

```
FAILED ...::test_<함수명> - NotImplementedError
# 또는
FAILED ... - AssertionError: assert 'fail' == 'pass'
```

---

## 골격 예시 (AAA 주석 + 최소 assert)

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

---

## 완료 보고 형식 (채팅)

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
- assert 생략·`pass` 만 있는 빈 테스트
- assert 완화 (`==` → `in` 축소, 조건 삭제, `or` 로 우회)
- `@pytest.mark.skip`, `xfail`, 테스트 삭제로 RED 숨기기
- 한 번에 여러 테스트 함수 추가
- private 헬퍼·내부 구현 직접 테스트 (공개 API `validate_lines` 결과 dict 만)
