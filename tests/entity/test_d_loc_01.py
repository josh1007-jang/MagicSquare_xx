"""D-LOC-01 — Entity: 빈칸 좌표 탐색 (1-indexed row-major)."""

from src.find_blank_coords import find_blank_coords
from tests.entity.constants import BLANK, GRID_SIZE, MAGIC_CONSTANT, MAX_CELL


def test_d_loc_01_find_blank_coords_returns_g1_blanks(grid_g1):
    # Arrange
    # grid_g1 — conftest: 빈칸 at (2,3), (4,4)

    # Act
    result = find_blank_coords(grid_g1)

    # Assert
    assert result == [(2, 3), (4, 4)]


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: G1 격자 (0이 2개) — GRID_SIZE={GRID_SIZE}, BLANK={BLANK}, MAX_CELL={MAX_CELL}, MAGIC={MAGIC_CONSTANT}
    # When: find_blank_coords(grid_g1) 호출
    # Then: [(2,3),(4,4)] 반환 (1-index, row-major)
    result = find_blank_coords(grid_g1)
    assert result == [(2, 3), (4, 4)]
