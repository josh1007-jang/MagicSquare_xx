# Golden Master — 전체 스위트 GREEN 검증

**추가 입력 없이 즉시 실행.** 사용자가 `/golden-master` 만 입력했다.
골든 기준은 **Test Loop TC1~TC3 + incomplete** 및 `tests/test_validate_lines.py` 전체를 SSOT로 삼는다. 추가 질문·확인 요청 금지.

SSOT: `.cursorrules`, `docs/PRD.md`(있을 때), `Report/Session3_Workbook_MagicSquare_xx.md`

---

## 필수 선언 (응답 첫 줄)

```
Phase: GREEN | Target: validate_lines | Track: golden-master
```

---

## ARRR 절차

1. **Arrange**
   - 골든 픽스처: `TC1_PASS_GRID`, `TC2_D1_FAIL_GRID`, `TC3_D2_FAIL_GRID`, incomplete 격자 패턴
   - 기대 골든 출력 요약:

     | 시나리오 | status | failed_lines |
     |----------|--------|--------------|
     | TC1 | `pass` | `[]` |
     | TC2 | `fail` | `"D1" in ...` |
     | TC3 | `fail` | `"D2" in ...` |
     | incomplete | `incomplete` | (빈칸 0 포함 선) |

2. **Red** *(골든 대비 갭)*
   - `pytest tests/test_validate_lines.py -v` 실행
   - FAIL 이 있으면 **GREEN 최소 수정**만 `src/validate_lines.py` 에 적용 (테스트 변경 금지)
3. **Run**
   - 전체 스위트 **ALL PASS** 확인
   - TC1 격자에 대해 `validate_lines` 결과를 골든 스냅샷으로 채팅에 1회 기록 (회귀 기준선)
4. **Report**
   - 아래 완료 보고 블록을 채팅에 출력한다

---

## pytest 예시

```bash
pytest tests/test_validate_lines.py -v
```

기대 출력 (골든 달성):

```
4 passed
```

미달 시 예:

```
2 passed, 2 failed — AssertionError on test_tc3_...
```

---

## 골든 스냅샷 기록 형식 (채팅)

```
TC1_PASS_GRID → {"status": "pass", "failed_lines": []}
TC2_D1_FAIL_GRID → {"status": "fail", "failed_lines": ["D1", ...]}  # 실제 출력 그대로
TC3_D2_FAIL_GRID → {"status": "fail", "failed_lines": ["D2", ...]}
incomplete (TC1+[0,0,0]=0) → {"status": "incomplete", "failed_lines": [...]}
```

*(failed_lines 전체는 구현 출력을 왜곡 없이 기록)*

---

## 완료 보고 형식 (채팅)

```
Phase: GREEN | Target: validate_lines | Track: golden-master

- pytest: <N passed> — ALL PASS | <실패 요약>
- 골든 스냅샷: TC1~TC3·incomplete 결과 요약
- 10선 전수: 확인됨 | 갭 있음 (<누락 선>)
- 변경 파일: src/validate_lines.py (FAIL 시만) | 없음 (이미 GREEN)
- 다음 권장: /refactor-smell (ALL PASS 시)
```

---

## 금지

- `tests/` 수정으로 GREEN 맞추기 (assert 완화·픽스처 변경·skip)
- 골든 미달인데 PASS 로 보고
- 10선 검증 생략 구현 유지
- 골든 달성 후 **REFACTOR** 를 이 커맨드에서 수행 (`/refactor-safe` 사용)
