"""Small example module with a stable public function."""

from collections.abc import Sequence


def total(values: Sequence[int] | None = None) -> int:
    """Returns the sum of values, or zero when values is omitted."""
    return sum(values or ())
