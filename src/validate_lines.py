"""4×4 마방진 10선 검증 — Control 진입점.

Entity: 4×4 격자, 0=빈칸, 1~16, 마법상수 34,
        검증 선 R1~R4 · C1~C4 · D1 · D2 (10개 전수).
"""

MAGIC_CONSTANT = 34

LINE_IDS = (
    "R1", "R2", "R3", "R4",
    "C1", "C2", "C3", "C4",
    "D1", "D2",
)


def validate_lines(grid: list[list[int]]) -> dict:
    """10선 합을 검증한다.

    Args:
        grid: 4×4 정수 2차원 리스트 (0=빈칸, 1~16=채워진 칸).

    Returns:
        {
            "status": "pass" | "fail" | "incomplete",
            "failed_lines": ["R1", "D1", ...],  # pass 시 []
        }
    """
    raise NotImplementedError
