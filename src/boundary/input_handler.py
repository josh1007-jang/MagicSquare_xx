"""Boundary — G1 격자 입력 조립 및 검증 (UI ↔ Control)."""

from dataclasses import dataclass

from src.find_blank_coords import find_blank_coords
from src.validate_lines import validate_lines

# tests/conftest.py G1_GRID 와 동일
G1_GRID = [
    [16, 3, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 0],
]


@dataclass(frozen=True)
class ValidationOutcome:
    """InputHandler.validate → validate_lines 결과."""

    status: str
    failed_lines: list[str]
    message: str | None = None


class InputHandler:
    """4×4 격자 입력 파싱 · validate_lines 위임."""

    def __init__(self, base_grid: list[list[int]] | None = None) -> None:
        self._base = [row[:] for row in (base_grid or G1_GRID)]
        self._blank_coords = find_blank_coords(self._base)

    @property
    def blank_coords(self) -> list[tuple[int, int]]:
        return list(self._blank_coords)

    @property
    def initial_grid(self) -> list[list[int]]:
        return [row[:] for row in self._base]

    def is_blank(self, row_1: int, col_1: int) -> bool:
        return (row_1, col_1) in self._blank_coords

    def fixed_value(self, row_1: int, col_1: int) -> int:
        return self._base[row_1 - 1][col_1 - 1]

    def build_grid(
        self, entries: dict[tuple[int, int], str]
    ) -> tuple[list[list[int]] | None, str | None]:
        """빈칸 문자열을 파싱해 grid를 만든다. (grid, None) 또는 (None, 오류 메시지)."""
        grid = [row[:] for row in self._base]
        for row_1, col_1 in self._blank_coords:
            text = entries.get((row_1, col_1), "").strip()
            if not text:
                continue
            try:
                value = int(text)
            except ValueError:
                return None, f"({row_1},{col_1}): 정수를 입력하세요"
            if not 1 <= value <= 16:
                return None, f"({row_1},{col_1}): 1~16 범위의 값만 입력 가능합니다"
            grid[row_1 - 1][col_1 - 1] = value
        return grid, None

    def parse_full_grid(
        self, cells: list[list[str]]
    ) -> tuple[list[list[int]] | None, str | None]:
        """4×4 UI 문자열 격자 → 정수 grid. 빈칸·'0' → 0."""
        if len(cells) != 4 or any(len(row) != 4 for row in cells):
            return None, "4×4 격자가 필요합니다"
        grid: list[list[int]] = []
        for row_1, row in enumerate(cells, start=1):
            parsed_row: list[int] = []
            for col_1, text in enumerate(row, start=1):
                stripped = text.strip()
                if stripped == "" or stripped == "0":
                    parsed_row.append(0)
                    continue
                try:
                    value = int(stripped)
                except ValueError:
                    return None, f"({row_1},{col_1}): 정수를 입력하세요"
                if not 1 <= value <= 16:
                    return None, f"({row_1},{col_1}): 0 또는 1~16 범위"
                parsed_row.append(value)
            grid.append(parsed_row)
        return grid, None

    def validate(self, cells: list[list[str]]) -> ValidationOutcome:
        """입력 파싱 후 validate_lines 호출 (Boundary → Control)."""
        grid, err = self.parse_full_grid(cells)
        if err:
            return ValidationOutcome(status="error", failed_lines=[], message=err)
        result = validate_lines(grid)
        return ValidationOutcome(
            status=result["status"],
            failed_lines=list(result["failed_lines"]),
        )
