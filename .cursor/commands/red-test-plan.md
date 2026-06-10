# RED Test Plan — 다음 실패 테스트 계획

**추가 입력 없이 즉시 실행.** 사용자가 `/red-test-plan` 만 입력했다.
대상·격자·기대값·우선순위는 **현재 채팅·저장소 상태**에서 자동 추출한다. 추가 질문·확인 요청 금지.

SSOT: `.cursorrules`, `docs/PRD.md`(있을 때), `Report/Session3_Workbook_MagicSquare_xx.md`

---

## 필수 선언 (응답 첫 줄)

```
Phase: RED | Target: validate_lines | Track: test-plan
```

---

## ARRR 절차

1. **Arrange**
   - `tests/test_validate_lines.py`·`src/validate_lines.py`·최근 pytest 결과를 확인한다
   - Test Loop(TC1~TC3·incomplete) 중 **아직 없거나 미커버**인 시나리오를 식별한다
   - Entity: 4×4, `0`=빈칸, 1~16, 마법상수 34, 10선 `R1~R4`·`C1~C4`·`D1`·`D2`
   - API 계약: `{"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}`
2. **Red**
   - **코드·파일 수정 없음** — 다음 RED용 **테스트 계획 1건**만 확정한다 (함수명·격자 요약·assert 초안)
3. **Run**
   - 필요 시 `pytest tests/test_validate_lines.py -v` 로 현재 RED/GREEN 상태만 확인한다 (테스트 코드 변경 금지)
4. **Report**
   - 아래 **계획 표**와 **다음 커맨드 힌트**를 채팅에 출력한다

---

## pytest 예시 (상태 확인만)

```bash
pytest tests/test_validate_lines.py -v
```

기록 예:

```
4 failed — NotImplementedError (RED 대기, TC1~TC3·incomplete 존재)
# 또는
N passed — GREEN 진행 중, 다음 RED 시나리오 선정
```

---

## 계획 표 형식 (채팅 출력)

| 항목 | 내용 |
|------|------|
| **다음 테스트 함수명** | `test_<동작_설명>` |
| **Track** | `logic` \| `boundary` \| `incomplete` |
| **Arrange (grid)** | 4×4 요약 — 빈칸·특이값 한 줄 |
| **Assert (기대)** | `status` / `failed_lines` |
| **RED 근거** | Test Loop·PRD·워크북 중 어떤 갭을 메우는지 한 줄 |
| **중복 여부** | 기존 `test_tc*`·`test_incomplete*` 와 겹치지 않음 확인 |

Test Loop 참고:

| ID | 시나리오 | 기대 |
|----|----------|------|
| TC1 | 10선 모두 합 34 | `pass`, `failed_lines == []` |
| TC2 | 행·열 OK, D1 불일치 | `fail`, `"D1" in failed_lines` |
| TC3 | 행·열 OK, D2 불일치 | `fail`, `"D2" in failed_lines` |
| — | 빈칸 `0` 존재 | `incomplete` |

---

## 완료 보고 형식 (채팅)

```
Phase: RED | Target: validate_lines | Track: test-plan

- 다음 테스트: test_<함수명>
- Track: <logic|boundary|incomplete>
- Arrange: <격자 한 줄 요약>
- Assert: status=<...> / failed_lines=<...>
- pytest 현황: <한 줄>
- 다음 권장: /red-skeleton 또는 /tdd-red
- 변경 파일: 없음 (계획만)
```

---

## 금지

- `tests/`·`src/` **파일 수정** (계획은 채팅만)
- 사용자에게 시나리오·함수명 **추가 질문**
- 한 번에 **여러 테스트** 계획 (1건만)
- assert 완화·skip·xfail **권장**
- 솔버·UI·범위 밖 기능 계획
