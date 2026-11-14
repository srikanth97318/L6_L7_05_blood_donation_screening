"""
Lab 7 - Fuzz tests (Hypothesis) for processor.py
Property tested: none of the three functions may ever raise an exception,
whatever input they receive (random text, None, numbers, bytes ...).
"""
from hypothesis import given, settings, strategies as st
from processor import validate_blood_type, calculate_pulse_pressure, parse_donor_registry


# ---------------- 1. "must not crash" fuzz tests (required by the handout) ----------------
@given(st.text() | st.none())
def test_validate_blood_type_no_crash(s):
    try:
        result = validate_blood_type(s)
    except Exception as e:
        assert False, f"validate_blood_type crashed with: {type(e).__name__}: {e}"
    assert isinstance(result, str)


@given(st.text() | st.none())
def test_calculate_pulse_pressure_safe(s):
    try:
        result = calculate_pulse_pressure(s)
    except Exception as e:
        assert False, f"calculate_pulse_pressure crashed with: {type(e).__name__}: {e}"
    assert isinstance(result, str)


@given(st.text() | st.none())
def test_parse_donor_registry_safe(s):
    try:
        result = parse_donor_registry(s)
    except Exception as e:
        assert False, f"parse_donor_registry crashed with: {type(e).__name__}: {e}"
    assert isinstance(result, str)


# ---------------- 2. wider type fuzzing (non-string garbage) ----------------
ANYTHING = st.one_of(st.none(), st.integers(), st.floats(), st.binary(),
                     st.lists(st.integers()), st.booleans(), st.text())


@given(ANYTHING)
def test_all_functions_survive_any_type(x):
    for fn in (validate_blood_type, calculate_pulse_pressure, parse_donor_registry):
        try:
            fn(x)
        except Exception as e:
            assert False, f"{fn.__name__}({x!r}) crashed with: {type(e).__name__}: {e}"


# ---------------- 3. correctness properties on VALID input ----------------
@given(st.sampled_from(["A", "B", "AB", "O"]), st.sampled_from(["+", "-"]),
       st.text(alphabet=" \t", max_size=3), st.booleans())
def test_valid_blood_types_are_normalised(antigen, rh, pad, lower):
    code = antigen + rh
    code = code.lower() if lower else code
    expected = f"{antigen} {'Positive' if rh == '+' else 'Negative'}"
    assert validate_blood_type(pad + code + pad) == expected


@given(st.integers(1, 300), st.integers(1, 300))
def test_valid_pulse_pressure(a, b):
    sys_bp, dia_bp = max(a, b), min(a, b)
    out = calculate_pulse_pressure(f"{sys_bp}/{dia_bp}")
    assert out == f"Diff: {sys_bp - dia_bp}, Ratio: {round(sys_bp / dia_bp, 2)}"


@given(st.integers(0, 10**6), st.floats(1, 300), st.floats(1, 30))
def test_valid_donor_registry(did, weight, hb):
    out = parse_donor_registry(f"D{did}|{weight}|{hb}")
    expected = "Eligible" if (float(str(weight)) >= 50.0 and float(str(hb)) >= 12.5) else "Deferred"
    assert out == f"Donor D{did}: {expected}"


# ---------------- 4. known edge cases found by fuzzing ----------------
def test_known_edge_cases_do_not_crash():
    for bad in ["", " ", "A", "+", "XY+", "A*", None, "ab", "O++"]:
        assert isinstance(validate_blood_type(bad), str)
    for bad in ["", "120", "120/0", "a/b", "1/2/3", "/", "120/", "/80", None, "-5/-2", "nan/1"]:
        assert isinstance(calculate_pulse_pressure(bad), str)
    for bad in ["", "D1", "D1|60", "D1|abc|13", "D1|nan|13", "D1|inf|13", "D1|-5|13", "|60|13", "a|b|c|d", None]:
        assert isinstance(parse_donor_registry(bad), str)