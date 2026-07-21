"""Fork-only immutable acceptance oracle for the sub-950 optimization campaign."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parent
TESTS = ROOT / "tests"
sys.path.insert(0, str(TESTS))

from submission_tests import do_kernel_test  # noqa: E402


EXPECTED_ORACLE_HASHES = {
    "frozen_problem.py": "fadb0f0858e2259f5759077a5544b9906dad3ceee80d37b4f0aa77da730c93c9",
    "submission_tests.py": "11c57cc999da93acb41201191073cd657ddffa87635359b3157c6e177c18ea0a",
}


def test_upstream_oracles_are_unchanged() -> None:
    for name, expected in EXPECTED_ORACLE_HASHES.items():
        actual = sha256((TESTS / name).read_bytes()).hexdigest()
        assert actual == expected, f"tests/{name} differs from upstream"


@pytest.mark.parametrize("sample", range(4))
def test_kernel_is_correct_and_strictly_below_950_cycles(sample: int) -> None:
    del sample
    measured = do_kernel_test(forest_height=10, rounds=16, batch_size=256)
    assert measured < 950, f"kernel took {measured} cycles; target is strictly below 950"
