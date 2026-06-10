"""Boundary — MagicSquare_1004 PyQt6 검증 GUI 프로토타입."""

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from src.boundary.grid_ui import GridUI
from src.boundary.input_handler import InputHandler
from src.boundary.result_display import ResultDisplay


class MagicSquare1004Window(QMainWindow):
    """G1 4×4 격자 · InputHandler.validate → validate_lines · ResultDisplay."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MagicSquare_1004 — 10선 검증")
        self.setMinimumWidth(360)

        self._handler = InputHandler()
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self._grid = GridUI(self._handler.initial_grid)
        layout.addWidget(self._grid)

        validate_btn = QPushButton("검증")
        validate_btn.clicked.connect(self._on_validate)
        layout.addWidget(validate_btn)

        self._result = ResultDisplay()
        layout.addWidget(self._result)

    def _on_validate(self) -> None:
        outcome = self._handler.validate(self._grid.get_cells())
        self._result.show_outcome(outcome)


def main() -> None:
    app = QApplication(sys.argv)
    window = MagicSquare1004Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
