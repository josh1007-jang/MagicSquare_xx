"""Entity — 4×4 격자에서 빈칸 좌표 탐색."""

from src.entity.constants import BLANK


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    """빈칸(0) 위치를 1-indexed (row, col) row-major 순으로 반환한다."""
    coords = []
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == BLANK:
                coords.append((row_idx + 1, col_idx + 1))
    return coords
