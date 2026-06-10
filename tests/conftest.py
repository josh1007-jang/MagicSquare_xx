"""pytest 공유 픽스처."""

import pytest

# G1: 부분 마방진 — 빈칸 2개 at (2,3), (4,4) 1-indexed
G1_GRID = [
    [16, 3, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 0],
]


@pytest.fixture
def grid_g1():
    return [row[:] for row in G1_GRID]
