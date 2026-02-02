import pytest
from main import (
    BULKY_DIMENSION_THRESHOLD_CM,
    BULKY_VOLUME_THRESHOLD_CM3,
    HEAVY_THRESHOLD_KG,
    STACK,
    sort
)

STANDARD_WIDTH = BULKY_DIMENSION_THRESHOLD_CM // 2
STANDARD_HEIGHT = BULKY_DIMENSION_THRESHOLD_CM // 3
STANDARD_LENGTH = BULKY_DIMENSION_THRESHOLD_CM // 4
STANDARD_WEIGHT = HEAVY_THRESHOLD_KG // 2


def make_volume_bulky(inclusive=False):
    """Returns dict with width/height/length that hit volume threshold without hitting dimension threshold"""
    base = BULKY_VOLUME_THRESHOLD_CM3 // 3
    length = BULKY_VOLUME_THRESHOLD_CM3 - (base*base)
    if not inclusive:
        length += 1
    return {"width": base, "height": base, "length": length}



@pytest.mark.parametrize("params, expected, message", [
    # STANDARD cases
    ({}, STACK.STANDARD, "everything under threshold"),

    # SPECIAL - Heavy only
    ({"weight": HEAVY_THRESHOLD_KG}, STACK.SPECIAL, "heavy at threshold (inclusive)"),
    ({"weight": HEAVY_THRESHOLD_KG * 2}, STACK.SPECIAL, "heavy over threshold"),

    # SPECIAL - Bulky by dimension
    ({"width": BULKY_DIMENSION_THRESHOLD_CM}, STACK.SPECIAL, "width at threshold (inclusive)"),
    ({"width": BULKY_DIMENSION_THRESHOLD_CM * 2}, STACK.SPECIAL, "width over threshold"),
    ({"height": BULKY_DIMENSION_THRESHOLD_CM}, STACK.SPECIAL, "height at threshold (inclusive)"),
    ({"height": BULKY_DIMENSION_THRESHOLD_CM * 2}, STACK.SPECIAL, "height over threshold"),
    ({"length": BULKY_DIMENSION_THRESHOLD_CM}, STACK.SPECIAL, "length at threshold (inclusive)"),
    ({"length": BULKY_DIMENSION_THRESHOLD_CM * 2}, STACK.SPECIAL, "length over threshold"),

    # SPECIAL - Bulky by volume (all dimensions under 150)
    (make_volume_bulky(), STACK.SPECIAL, "volume at threshold (inclusive)"),
    (make_volume_bulky(inclusive=False), STACK.SPECIAL, "volume over threshold"),

    # REJECTED - Heavy and bulky
    ({"width": BULKY_DIMENSION_THRESHOLD_CM, "weight": HEAVY_THRESHOLD_KG}, STACK.REJECTED, "heavy and bulky by dimension"),
    ({**make_volume_bulky(), "weight": HEAVY_THRESHOLD_KG}, STACK.REJECTED, "heavy and bulky by volume"),
    ({"width": BULKY_DIMENSION_THRESHOLD_CM * 2, "weight": HEAVY_THRESHOLD_KG * 2}, STACK.REJECTED, "heavy and bulky (both over)"),

])
def test_sort(params, expected, message):
    assert sort(
        params.get('width') or STANDARD_WIDTH,
        params.get('height') or STANDARD_HEIGHT,
        params.get('length') or STANDARD_LENGTH,
        params.get('weight') or STANDARD_WEIGHT
    ) == expected, message