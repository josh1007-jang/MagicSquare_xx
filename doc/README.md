# MagicSquare_xx — doc

프로젝트 **요구사항·계약** 문서 모음. 구현·테스트·AI Skill의 SSOT(단일 기준)로 사용한다.

| 파일 | 버전 | 내용 |
|------|------|------|
| [`PRD.md`](PRD.md) | 0.1 | Product Requirements Document — Mom Test, R-G-I-O, ECB, API 계약, Test Loop, 범위 |

---

## PRD 역할

`PRD.md`는 아래 문서가 분산해 두었던 요구사항을 **한곳으로 통합**한다.

| 출처 | PRD에서 다루는 내용 |
|------|---------------------|
| `Report/MomTest_STEP1_MagicSquare_xx.md` | 문제 정의, 페르소나, 증거 |
| `Report/Session3_Workbook_MagicSquare_xx.md` | R-G-I-O, 성공 기준, 8계층 |
| `.cursorrules` | Entity · Control · Boundary · TDD 규칙 |
| `src/validate_lines.py`, `tests/test_validate_lines.py` | API 계약, Test Loop (TC1~TC3) |
| `Report/02.REPORT.md` | 워크북 ↔ 계약 갭 (§12) |

**충돌 시 우선순위:** `PRD.md` §7~§9 (API 계약) → `.cursorrules`

---

## PRD 목차 (빠른 참조)

| § | 제목 | 용도 |
|---|------|------|
| 1 | 개요 | 프로젝트 한 줄 설명 |
| 2 | 문제 정의 | Mom Test |
| 3~4 | R-G-I-O · 성공 기준 | SC1~SC4 |
| 5 | 범위 | In / Out Scope |
| 6~7 | ECB · Entity | 10선, 마법상수 34 |
| 8 | Control — API | `validate_lines(grid)` 계약 |
| 9 | Boundary — Test Loop | TC1~TC3, incomplete |
| 10 | TDD · 개발 프로세스 | RED / GREEN / REFACTOR |
| 12 | 워크북 ↔ 계약 갭 | 알려진 차이 |
| 13 | 마일스톤 | 현재 상태 |
| 14 | 향후 검토 | v0.2+ 후보 |

---

## API 요약

```python
from src.validate_lines import validate_lines

result = validate_lines(grid)
# {
#   "status": "pass" | "fail" | "incomplete",
#   "failed_lines": ["R1", "D1", ...],  # pass 시 []
# }
```

- **Input:** 4×4 정수 격자 (`0`=빈칸, `1`~`16`)
- **10선:** `R1`~`R4`, `C1`~`C4`, `D1`, `D2`
- **마법상수:** `34` (`MAGIC_CONSTANT`)

---

## 관련 폴더

| 폴더 | 역할 |
|------|------|
| `src/` | Control 구현 (`validate_lines`) |
| `tests/` | Boundary — Test Loop |
| `Report/` | Mom Test, 워크북, 세션 Export |
| `Prompting/` | 프롬프트·Transcript |
| `.cursor/` | TDD·Export 슬래시 커맨드, Skills |

---

## 현재 상태 (PRD §13)

| 단계 | 상태 |
|------|:----:|
| Mom Test · 워크북 · Harness · RED | ✅ |
| GREEN (`validate_lines` 구현) | 🔲 |
| REFACTOR | 🔲 |

```bash
pytest tests/test_validate_lines.py -v
```

---

## SSOT 참조 (Skills · 커맨드)

다음 파일에서 `doc/PRD.md`를 SSOT로 참조한다.

- `.cursor/skills/magic-square-tdd/SKILL.md`
- `.cursor/skills/magic-square-docs/SKILL.md`

PRD 갱신 시 §7~§9 (Entity · API · Test Loop)와 `.cursorrules`를 함께 맞춘다.
