"""Boundary — 4×4 격자 GridUI (PyQt6, PRD GridUI 프로토타입)."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLineEdit, QWidget

from src.boundary.input_handler import G1_GRID


class GridUI(QWidget):
    """4×4 QLineEdit 격자 — 초기값 grid_g1, 빈칸(0)은 공란."""

    def __init__(
        self,
        initial_grid: list[list[int]] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._cells: list[list[QLineEdit]] = []
        layout = QGridLayout(self)
        layout.setSpacing(4)

        grid = initial_grid or G1_GRID
        for row in range(4):
            row_widgets: list[QLineEdit] = []
            for col in range(4):
                edit = QLineEdit()
                edit.setMaxLength(2)
                edit.setFixedWidth(48)
                edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
                value = grid[row][col]
                if value != 0:
                    edit.setText(str(value))
                layout.addWidget(edit, row, col)
                row_widgets.append(edit)
            self._cells.append(row_widgets)

    def get_cells(self) -> list[list[str]]:
        return [[cell.text() for cell in row] for row in self._cells]
