"""Entity — 부분 마방진 step A: row-major 첫 빈칸에 행합 34로 값 도출."""

from src.validate_lines import MAGIC_CONSTANT


def solve_step_a(grid: list[list[int]]) -> dict:
    """첫 빈칸(0) 위치에 행 합 34 제약으로 채울 값을 계산한다.

    Returns:
        {
            "status": "success",
            "coord": (row, col),  # 1-indexed
            "value": int,
        }
    """
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == 0:
                row_sum = sum(v for v in row if v != 0)
                fill_value = MAGIC_CONSTANT - row_sum
                return {
                    "status": "success",
                    "coord": (row_idx + 1, col_idx + 1),
                    "value": fill_value,
                }
    raise ValueError("no blank cell")
