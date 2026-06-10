# REFACTOR Safe — green 유지 구조 정리

**추가 입력 없이 즉시 실행.** 사용자가 `/refactor-safe` 만 입력했다.
리팩터 대상은 **최근 smell 진단·중복·명명** 이슈를 저장소에서 자동 선정한다. 추가 질문·확인 요청 금지.

SSOT: `.cursorrules`, `docs/PRD.md`(있을 때), `Report/Session3_Workbook_MagicSquare_xx.md`

---

## 필수 선언 (응답 첫 줄)

```
Phase: REFACTOR | Target: validate_lines | Track: safe
```

---

## ARRR 절차

1. **Arrange**
   - `pytest tests/test_validate_lines.py -v` → **ALL PASS** 확인 (미달 시 `/green-minimal` 먼저)
   - `src/validate_lines.py` 에서 **한 가지 smell** 만 해소 범위로 고른다
2. **Red** *(안전선)*
   - **동작·공개 API·10선 전수** 불변을 명시한다
   - 수정 범위: `src/validate_lines.py` 만 (private 헬퍼 추가 허용)
3. **Run**
   - 리팩터 적용 → `pytest tests/test_validate_lines.py -v` → **ALL PASS** 유지
   - 실패 시 **즉시 롤백** 후 원인 1줄 보고
4. **Report**
   - 아래 완료 보고 블록을 채팅에 출력한다

---

## pytest 예시

```bash
# 리팩터 전·후 동일하게 ALL PASS
pytest tests/test_validate_lines.py -v
```

```
4 passed — REFACTOR safe 완료
```

---

## 안전 리팩터 허용·금지

| 허용 | 금지 |
|------|------|
| private 헬퍼 추출 (`_sum_row`, `_collect_lines` 등) | `validate_lines` 시그니처·반환 dict 키 변경 |
| `MAGIC_CONSTANT`·`LINE_IDS` 활용 정리 | 10선 중 일부 검사 제거 |
| 중복 제거·변수·함수 이름 개선 | 테스트 assert 완화 |
| docstring·주석 정리 (비즈니스 규칙만) | 새 기능(솔버·UI·추가 status) |

---

## 완료 보고 형식 (채팅)

```
Phase: REFACTOR | Target: validate_lines | Track: safe

- 리팩터 요약: <한 줄 — 예: 행/열 합 계산 헬퍼 추출>
- pytest (전): <N passed>
- pytest (후): <N passed> — ALL PASS 유지
- 변경 파일: src/validate_lines.py
- 남은 smell: <있으면 한 줄, 없으면 "없음">
```

---

## 금지

- `tests/` 수정
- 한 번에 **여러 smell** 대규모 개편 (1 smell 1 사이클)
- GREEN 깨진 채로 완료 보고
- 공개 API·Entity 규칙 변경
- `@pytest.mark.skip`, `xfail` 적용
