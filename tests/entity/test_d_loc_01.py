"""D-LOC-01 — Entity: 빈칸 좌표 탐색 (1-indexed row-major)."""

from src.find_blank_coords import find_blank_coords


def test_d_loc_01_find_blank_coords_returns_g1_blanks(grid_g1):
    # Arrange
    # grid_g1 — conftest: 빈칸 at (2,3), (4,4)

    # Act
    result = find_blank_coords(grid_g1)

    # Assert
    assert result == [(2, 3), (4, 4)]
