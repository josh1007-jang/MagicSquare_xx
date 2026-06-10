"""D-LOC-01 — Entity: 빈칸 좌표 탐색 (1-indexed row-major)."""

from src.find_blank_coords import find_blank_coords
from tests._approval import assert_matches_golden, format_u_out_loc_01
from tests.entity.constants import BLANK, GRID_SIZE, MAGIC_CONSTANT, MAX_CELL

GOLDEN_D_LOC_01_G1 = "d_loc_01_g1_blanks.approved.txt"


def test_d_loc_01_find_blank_coords_returns_g1_blanks(grid_g1):
    # Arrange
    # grid_g1 — conftest: 빈칸 at (2,3), (4,4)

    # Act
    result = find_blank_coords(grid_g1)

    # Assert — contract + U-OUT-LOC-01 golden (Track A)
    assert result == [(2, 3), (4, 4)]
    assert_matches_golden(format_u_out_loc_01(result), GOLDEN_D_LOC_01_G1)


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: G1 격자 (0이 2개) — GRID_SIZE={GRID_SIZE}, BLANK={BLANK}, MAX_CELL={MAX_CELL}, MAGIC={MAGIC_CONSTANT}
    # When: find_blank_coords(grid_g1) 호출
    # Then: [(2,3),(4,4)] 반환 (1-index, row-major)
    result = find_blank_coords(grid_g1)
    assert result == [(2, 3), (4, 4)]
