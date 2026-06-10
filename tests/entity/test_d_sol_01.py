"""D-SOL-01 — Entity: 부분 마방진 step A (첫 빈칸 행합으로 값 도출)."""

from src.solve_step_a import solve_step_a
from tests._approval import assert_matches_golden, format_u_out_01

GOLDEN_D_SOL_01_STEP_A = "d_sol_01_g1_step_a.approved.txt"


def test_d_sol_01_step_a_success(grid_g1):
    # Arrange
    # grid_g1 — conftest: 첫 빈칸 (2,3), MAGIC_CONSTANT=34

    # Act
    result = solve_step_a(grid_g1)

    # Assert — contract + U-OUT-01 golden
    assert result["status"] == "success"
    assert result["coord"] == (2, 3)
    assert result["value"] == 11
    assert_matches_golden(format_u_out_01(result), GOLDEN_D_SOL_01_STEP_A)
