"""4×4 마방진 10선 검증 — Control 진입점.

Entity: 4×4 격자, 0=빈칸, 1~16, 마법상수 34,
        검증 선 R1~R4 · C1~C4 · D1 · D2 (10개 전수).
"""

from src.entity.validation import (
    LINE_IDS,
    MAGIC_CONSTANT,
    compute_line_sum,
)

__all__ = ("MAGIC_CONSTANT", "LINE_IDS", "validate_lines")


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
    if any(value == 0 for row in grid for value in row):
        return {"status": "incomplete", "failed_lines": []}

    failed_lines = [
        line_id
        for line_id in LINE_IDS
        if compute_line_sum(grid, line_id) != MAGIC_CONSTANT
    ]

    if not failed_lines:
        return {"status": "pass", "failed_lines": []}
    return {"status": "fail", "failed_lines": failed_lines}
