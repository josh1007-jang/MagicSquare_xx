"""Boundary — Test Loop (TC1~TC3) + incomplete 계약."""

from src.validate_lines import validate_lines

# TC1: 10선 모두 합 34
TC1_PASS_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# TC2: 행·열 합 34, D1 불일치 (인터뷰 재현 — 대각선 하나만 틀린 착각 방지)
TC2_D1_FAIL_GRID = [
    [8, 8, 9, 9],
    [8, 8, 9, 9],
    [8, 8, 9, 9],
    [10, 10, 7, 7],
]

# TC3: 행·열 합 34, D2 불일치 (대각선 검증 생략 시 Rule 위반 감지)
TC3_D2_FAIL_GRID = [
    [1, 12, 11, 10],
    [14, 5, 6, 9],
    [7, 8, 15, 4],
    [12, 9, 2, 11],
]


def test_tc1_all_ten_lines_pass():
    result = validate_lines(TC1_PASS_GRID)
    assert result["status"] == "pass"
    assert result["failed_lines"] == []


def test_tc2_rows_cols_ok_diagonal_d1_fails():
    result = validate_lines(TC2_D1_FAIL_GRID)
    assert result["status"] == "fail"
    assert "D1" in result["failed_lines"]


def test_tc3_rows_cols_ok_diagonal_d2_fails():
    result = validate_lines(TC3_D2_FAIL_GRID)
    assert result["status"] == "fail"
    assert "D2" in result["failed_lines"]


def test_incomplete_when_blank_present():
    grid = [row[:] for row in TC1_PASS_GRID]
    grid[0][0] = 0
    result = validate_lines(grid)
    assert result["status"] == "incomplete"


def test_fail_includes_r1_when_row_sum_not_34():
    # Arrange — TC1 기반, R1 우하단 13→14 (합 35)
    grid = [row[:] for row in TC1_PASS_GRID]
    grid[0][3] = 14

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert "R1" in result["failed_lines"]
