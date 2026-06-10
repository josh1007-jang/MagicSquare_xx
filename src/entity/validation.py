"""Entity — 10선 합 계산."""

MAGIC_CONSTANT = 34

LINE_IDS = (
    "R1", "R2", "R3", "R4",
    "C1", "C2", "C3", "C4",
    "D1", "D2",
)


def _sum_cells(grid: list[list[int]], coords: list[tuple[int, int]]) -> int:
    return sum(grid[row][col] for row, col in coords)


def compute_line_sum(grid: list[list[int]], line_id: str) -> int:
    """단일 선(R/C/D)의 칸 합을 반환한다."""
    if line_id.startswith("R"):
        row = int(line_id[1]) - 1
        coords = [(row, col) for col in range(4)]
    elif line_id.startswith("C"):
        col = int(line_id[1]) - 1
        coords = [(row, col) for row in range(4)]
    elif line_id == "D1":
        coords = [(i, i) for i in range(4)]
    elif line_id == "D2":
        coords = [(i, 3 - i) for i in range(4)]
    else:
        raise ValueError(f"unknown line_id: {line_id}")
    return _sum_cells(grid, coords)
