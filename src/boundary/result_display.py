"""Boundary — 검증 결과 ResultDisplay (PyQt6, PRD ResultDisplay 프로토타입)."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget

from src.boundary.input_handler import ValidationOutcome
from src.entity.validation import LINE_IDS


class ResultDisplay(QWidget):
    """pass / fail / incomplete + failed_lines · 10선 라벨 표시."""

    _OK_STYLE = "color: #1a7f37; font-weight: bold;"
    _FAIL_STYLE = "color: #cf222e; font-weight: bold;"
    _NEUTRAL_STYLE = "color: #57606a;"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        root = QVBoxLayout(self)

        self._status_label = QLabel("status: —")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        root.addWidget(self._status_label)

        self._failed_label = QLabel("failed_lines: —")
        self._failed_label.setWordWrap(True)
        root.addWidget(self._failed_label)

        lines_frame = QWidget()
        lines_layout = QGridLayout(lines_frame)
        lines_layout.setSpacing(4)
        self._line_labels: dict[str, QLabel] = {}
        for idx, line_id in enumerate(LINE_IDS):
            lbl = QLabel(f"{line_id}: —")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setMinimumWidth(52)
            lines_layout.addWidget(lbl, idx // 5, idx % 5)
            self._line_labels[line_id] = lbl
        root.addWidget(lines_frame)

    def show_outcome(self, outcome: ValidationOutcome) -> None:
        if outcome.status == "error":
            self._status_label.setText("status: 입력 오류")
            self._status_label.setStyleSheet(self._FAIL_STYLE)
            self._failed_label.setText(outcome.message or "")
            self._reset_lines(outcome)
            return

        self._status_label.setText(f"status: {outcome.status}")
        if outcome.status == "pass":
            self._status_label.setStyleSheet(self._OK_STYLE)
            self._failed_label.setText("failed_lines: []")
        elif outcome.status == "incomplete":
            self._status_label.setStyleSheet(self._NEUTRAL_STYLE)
            self._failed_label.setText(
                "failed_lines: [] (빈칸 0 포함 → incomplete)"
            )
        else:
            self._status_label.setStyleSheet(self._FAIL_STYLE)
            self._failed_label.setText(f"failed_lines: {outcome.failed_lines}")

        self._reset_lines(outcome)

    def _reset_lines(self, outcome: ValidationOutcome) -> None:
        failed = set(outcome.failed_lines)
        for line_id, lbl in self._line_labels.items():
            if outcome.status in ("error", "incomplete"):
                lbl.setText(f"{line_id}: —")
                lbl.setStyleSheet(self._NEUTRAL_STYLE)
            elif outcome.status == "pass":
                lbl.setText(line_id)
                lbl.setStyleSheet(
                    f"{self._OK_STYLE} background: #dafbe1; border-radius: 4px; padding: 2px;"
                )
            elif line_id in failed:
                lbl.setText(line_id)
                lbl.setStyleSheet(
                    f"{self._FAIL_STYLE} background: #ffebe9; border-radius: 4px; padding: 2px;"
                )
            else:
                lbl.setText(line_id)
                lbl.setStyleSheet(
                    f"{self._OK_STYLE} background: #dafbe1; border-radius: 4px; padding: 2px;"
                )
