# REFACTOR Smell — 코드 냄새 진단

**추가 입력 없이 즉시 실행.** 사용자가 `/refactor-smell` 만 입력했다.
진단 대상은 `src/validate_lines.py` 및 최근 GREEN 구현을 **저장소에서 자동 읽는다**. 추가 질문·확인 요청 금지.

SSOT: `.cursorrules`, `docs/PRD.md`(있을 때), `Report/Session3_Workbook_MagicSquare_xx.md`

---

## 필수 선언 (응답 첫 줄)

```
Phase: REFACTOR | Target: validate_lines | Track: smell
```

---

## ARRR 절차

1. **Arrange**
   - `pytest tests/test_validate_lines.py -v` → **ALL PASS** 여부 확인 (RED면 smell 진단만 하고 리팩터는 보류)
   - `src/validate_lines.py` 전문을 읽는다
2. **Red** *(안전선)*
   - 리팩터 **전** smell 목록만 작성한다 — **코드 수정 없음**
3. **Run**
   - smell 항목마다 **증거(줄·패턴)** 와 **제안 방향**(이름·추출·중복 제거)을 1줄로 연결한다
   - 우선순위: `critical`(동작·10선 누락 위험) > `major`(중복·매직넘버) > `minor`(명명·주석)
4. **Report**
   - 아래 smell 표와 다음 커맨드를 채팅에 출력한다

---

## pytest 예시 (전제 확인)

```bash
pytest tests/test_validate_lines.py -v
```

```
4 passed — smell 진단 진행
# 또는
2 failed — GREEN 미완, /green-minimal 권장
```

---

## smell 표 형식 (채팅)

| 우선순위 | smell | 위치 | 제안 (방향만) |
|----------|-------|------|----------------|
| critical/major/minor | 예: D1/D2 합 로직 중복 | `validate_lines.py:L..` | `_line_sum` 추출 |
| ... | ... | ... | ... |

흔한 smell 체크리스트 (`validate_lines` 맥락):

- [ ] R1~R4·C1~C4·D1·D2 검사 **중복 블록**
- [ ] `34` 리터럴 반복 (`MAGIC_CONSTANT` 미사용)
- [ ] `failed_lines` 조립 일관성 (ID 문자열 규칙)
- [ ] `incomplete` 선판별 vs 합 검사 순서 혼란
- [ ] 불필요한 분기·dead code
- [ ] Boundary 밖 공개 API 변경 유혹 (dict 키 추가 등)

---

## 완료 보고 형식 (채팅)

```
Phase: REFACTOR | Target: validate_lines | Track: smell

- pytest: <N passed | M failed>
- smell N건: critical=<a> major=<b> minor=<c>
- 최우선 1건: <한 줄>
- 다음 권장: /refactor-safe
- 변경 파일: 없음 (진단만)
```

---

## 금지

- `src/`·`tests/` **수정** (이 커맨드는 진단만)
- smell 없이 리팩터 착수
- 동작 변경·10선 생략을 동반하는 "정리"
- 사용자에게 smell 항목 **추가 질문**
- RED 상태에서 assert·테스트 변경 제안
