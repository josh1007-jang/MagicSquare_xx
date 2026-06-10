"""Boundary — G1 마방진 최소 GUI 데모 (tkinter)."""

import tkinter as tk
from tkinter import ttk

from src.boundary.input_handler import InputHandler
from src.entity.validation import LINE_IDS
from src.validate_lines import validate_lines


class MagicSquareDemoApp:
    """4×4 G1 격자 표시 · 빈칸 입력 · validate_lines 검증 결과."""

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._handler = InputHandler()
        self._entries: dict[tuple[int, int], tk.Entry] = {}

        root.title("MagicSquare_xx — G1 검증 데모")
        root.resizable(False, False)

        self._build_grid()
        self._build_controls()
        self._build_result()

    def _build_grid(self) -> None:
        frame = ttk.LabelFrame(self._root, text="G1 격자 (4×4)", padding=8)
        frame.grid(row=0, column=0, padx=12, pady=12)

        for row_1 in range(1, 5):
            for col_1 in range(1, 5):
                if self._handler.is_blank(row_1, col_1):
                    entry = ttk.Entry(frame, width=4, justify="center")
                    entry.grid(row=row_1 - 1, column=col_1 - 1, padx=2, pady=2)
                    self._entries[(row_1, col_1)] = entry
                else:
                    value = self._handler.fixed_value(row_1, col_1)
                    label = tk.Label(
                        frame,
                        text=str(value),
                        width=4,
                        anchor="center",
                        relief="sunken",
                        bg="#e8e8e8",
                    )
                    label.grid(row=row_1 - 1, column=col_1 - 1, padx=2, pady=2)

        hint = ttk.Label(
            frame,
            text="회색 칸: 고정 · 흰 칸: 빈칸 (2,3), (4,4) — 1~16 입력",
            font=("", 8),
        )
        hint.grid(row=4, column=0, columnspan=4, pady=(8, 0))

    def _build_controls(self) -> None:
        btn = ttk.Button(self._root, text="검증", command=self._on_validate)
        btn.grid(row=1, column=0, pady=(0, 8))

    def _build_result(self) -> None:
        frame = ttk.LabelFrame(self._root, text="validate_lines 결과", padding=8)
        frame.grid(row=2, column=0, padx=12, pady=(0, 12), sticky="ew")

        self._status_var = tk.StringVar(value="status: —")
        ttk.Label(frame, textvariable=self._status_var, font=("", 11, "bold")).grid(
            row=0, column=0, sticky="w"
        )

        self._failed_var = tk.StringVar(value="failed_lines: —")
        ttk.Label(frame, textvariable=self._failed_var, wraplength=360).grid(
            row=1, column=0, sticky="w", pady=(4, 8)
        )

        lines_frame = ttk.Frame(frame)
        lines_frame.grid(row=2, column=0, sticky="w")
        self._line_labels: dict[str, ttk.Label] = {}
        for idx, line_id in enumerate(LINE_IDS):
            lbl = ttk.Label(lines_frame, text=f"{line_id}: —", width=8)
            lbl.grid(row=idx // 5, column=idx % 5, padx=2, pady=1, sticky="w")
            self._line_labels[line_id] = lbl

    def _on_validate(self) -> None:
        entries = {coord: entry.get() for coord, entry in self._entries.items()}
        grid, err = self._handler.build_grid(entries)
        if err:
            self._status_var.set(f"status: 입력 오류")
            self._failed_var.set(err)
            self._reset_line_display(set())
            return

        result = validate_lines(grid)
        status = result["status"]
        failed = result["failed_lines"]
        failed_set = set(failed)

        self._status_var.set(f"status: {status}")
        if status == "pass":
            self._failed_var.set("failed_lines: []")
        elif status == "incomplete":
            self._failed_var.set("failed_lines: [] (빈칸 미입력 → incomplete)")
        else:
            self._failed_var.set(f"failed_lines: {failed}")
        self._reset_line_display(failed_set)

    def _reset_line_display(self, failed_set: set[str]) -> None:
        for line_id, lbl in self._line_labels.items():
            if line_id in failed_set:
                lbl.configure(text=f"{line_id}: FAIL", foreground="red")
            else:
                lbl.configure(text=f"{line_id}: OK", foreground="green")


def main() -> None:
    root = tk.Tk()
    MagicSquareDemoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
