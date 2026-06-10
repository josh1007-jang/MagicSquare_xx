"""Golden master approval — U-OUT fixed text formats (Track A/B)."""

import os
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
GOLDEN_DIR = TESTS_DIR / "golden"


def format_u_out_loc_01(coords: list[tuple[int, int]]) -> str:
    """U-OUT-LOC-01 (Track A): blank_count + row/col pairs (1-index) + err_code.

    Six lines — G1 golden assumes exactly 2 blanks.
    """
    if len(coords) != 2:
        raise ValueError("U-OUT-LOC-01 G1 golden expects exactly 2 blanks")
    (r1, c1), (r2, c2) = coords
    lines = [
        str(len(coords)),
        str(int(r1)),
        str(int(c1)),
        str(int(r2)),
        str(int(c2)),
        "-",
    ]
    return "\n".join(lines) + "\n"


def format_u_out_01(result: dict) -> str:
    """U-OUT-01: status(str) + row/col/value(1-index int) + err_code(str) + err_int(int).

    Six body lines — coordinates are 1-indexed; err_code is '-' on success.
    """
    status = result["status"]
    row, col = result["coord"]
    value = result["value"]
    err_code = result.get("err_code", "-")
    err_int = result.get("err_int", 0)
    lines = [
        status,
        str(int(row)),
        str(int(col)),
        str(int(value)),
        str(err_code),
        str(int(err_int)),
    ]
    return "\n".join(lines) + "\n"


def assert_matches_golden(actual: str, relative: str) -> None:
    """Compare actual text to tests/golden/{relative}; UPDATE_GOLDEN=1 writes baseline."""
    golden_path = GOLDEN_DIR / relative
    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual, encoding="utf-8")
        return

    if not golden_path.is_file():
        raise AssertionError(f"golden missing: {golden_path}")

    expected = golden_path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(
            f"golden mismatch: {relative}\n"
            f"--- expected ---\n{expected}"
            f"--- actual ---\n{actual}"
        )
