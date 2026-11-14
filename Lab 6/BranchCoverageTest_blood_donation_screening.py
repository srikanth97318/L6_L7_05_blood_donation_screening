"""
Lab 6 - BRANCH coverage tests for blood_donation_screening.py
Goal: make every decision evaluate to BOTH True and False (>= 90% branch coverage),
including boundary values (17 / 50 / 12.5 / 18.0 / 3000 rpm).

Run:
    coverage run --branch -m pytest BranchCoverageTest_blood_donation_screening.py
    coverage report -m --include=blood_donation_screening.py
"""
import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge


def make_cohort(donors, registered=True, ctype="standard", fast_track=False):
    return {
        "clinic_registered": registered,
        "type": ctype,
        "fast_track": fast_track,
        "donors": donors,
    }


GOOD = {"age": 25, "weight_kg": 65, "hb": 14.0}
BAD = {"age": 16, "weight_kg": 40, "hb": 10.0}


# ---------- input validation: both operands of  `not list or volume <= 0` ----------
def test_single_accepted_donor():
    assert process_donor_cohort([make_cohort([GOOD])], 450) == {
        "collected_ml": 450, "status": "ACCEPTED"}


def test_non_list_cohorts_raises():
    with pytest.raises(ValueError):
        process_donor_cohort({"a": 1}, 450)


@pytest.mark.parametrize("volume", [0, -1, -450])
def test_non_positive_volume_raises(volume):
    with pytest.raises(ValueError):
        process_donor_cohort([make_cohort([GOOD])], volume)


def test_empty_cohort_list_is_zero_yield():
    assert process_donor_cohort([], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


# ---------- clinic_registered True / False / missing ----------
def test_unregistered_cohort_skipped_registered_one_counted():
    cohorts = [make_cohort([GOOD], registered=False), make_cohort([GOOD])]
    assert process_donor_cohort(cohorts, 450)["collected_ml"] == 450


def test_missing_registered_key_defaults_to_skip():
    result = process_donor_cohort([{"donors": [GOOD]}], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


# ---------- age / weight deferral (both sides of `or`) ----------
@pytest.mark.parametrize("age,weight,expected", [
    (16, 65, 0),     # age fails, weight ok
    (17, 65, 450),   # age boundary passes
    (25, 49, 0),     # weight fails, age ok
    (25, 50, 450),   # weight boundary passes
    (16, 49, 0),     # both fail
])
def test_age_weight_boundaries(age, weight, expected):
    donor = {"age": age, "weight_kg": weight, "hb": 14.0}
    assert process_donor_cohort([make_cohort([donor])], 450)["collected_ml"] == expected


def test_donor_with_missing_fields_is_deferred():
    result = process_donor_cohort([make_cohort([{}])], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


# ---------- hemoglobin branches ----------
@pytest.mark.parametrize("hb,expected", [
    (12.4, 0),     # just below lower bound -> deferred
    (12.5, 450),   # lower boundary accepted
    (18.0, 450),   # upper boundary accepted
    (18.1, 0),     # just above upper bound -> deferred
])
def test_hemoglobin_boundaries(hb, expected):
    donor = {"age": 30, "weight_kg": 70, "hb": hb}
    assert process_donor_cohort([make_cohort([donor])], 450)["collected_ml"] == expected


def test_low_hb_standard_cohort_does_not_break_loop():
    low = {"age": 30, "weight_kg": 70, "hb": 11.0}
    result = process_donor_cohort([make_cohort([low, GOOD])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_low_hb_high_altitude_breaks_and_resets_total():
    low = {"age": 30, "weight_kg": 70, "hb": 11.0}
    cohort = make_cohort([GOOD, GOOD, low, GOOD], ctype="high_altitude")
    # break happens at `low`: previous 900 ml wiped, last GOOD never processed
    assert process_donor_cohort([cohort], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_altitude_cohort_with_healthy_donors_is_fine():
    cohort = make_cohort([GOOD], ctype="high_altitude")
    assert process_donor_cohort([cohort], 450)["collected_ml"] == 450


def test_default_cohort_type_is_standard():
    low = {"age": 30, "weight_kg": 70, "hb": 11.0}
    cohort = {"clinic_registered": True, "donors": [GOOD, low]}  # no "type" key
    assert process_donor_cohort([cohort], 450)["collected_ml"] == 450


def test_cohort_without_donors_key():
    assert process_donor_cohort([{"clinic_registered": True}], 450)["status"] == "ZERO_YIELD"


# ---------- fast_track True / False ----------
def test_fast_track_adds_50():
    cohort = make_cohort([GOOD], fast_track=True)
    assert process_donor_cohort([cohort], 450) == {"collected_ml": 500, "status": "ACCEPTED"}


def test_fast_track_applies_even_after_high_altitude_reset():
    low = {"age": 30, "weight_kg": 70, "hb": 11.0}
    cohort = make_cohort([low], ctype="high_altitude", fast_track=True)
    assert process_donor_cohort([cohort], 450) == {"collected_ml": 50, "status": "ACCEPTED"}


# ---------- final status branches ----------
def test_deferral_count_of_four_is_not_high_deferral():
    result = process_donor_cohort([make_cohort([BAD] * 4 + [GOOD])], 450)
    assert result["status"] == "ACCEPTED"


def test_deferral_count_of_five_is_high_deferral():
    result = process_donor_cohort([make_cohort([BAD] * 5 + [GOOD])], 450)
    assert result == {"collected_ml": 450, "status": "HIGH_DEFERRAL"}


def test_high_deferral_takes_priority_over_zero_yield():
    result = process_donor_cohort([make_cohort([BAD] * 5)], 450)
    assert result == {"collected_ml": 0, "status": "HIGH_DEFERRAL"}


def test_multiple_cohorts_accumulate():
    cohorts = [make_cohort([GOOD, GOOD]), make_cohort([GOOD], fast_track=True)]
    assert process_donor_cohort(cohorts, 100) == {"collected_ml": 350, "status": "ACCEPTED"}


# ---------- verify_storage_centrifuge ----------
@pytest.mark.parametrize("empty", [[], None])
def test_centrifuge_no_data(empty):
    assert verify_storage_centrifuge(empty) == "NO_DATA"


def test_centrifuge_two_consecutive_drops_abort():
    assert verify_storage_centrifuge([[3500, 2900, 2800]]) == "ABORT_SPIN"


def test_centrifuge_single_drop_then_recovery_is_stable():
    assert verify_storage_centrifuge([[3500, 2900, 3500, 2900, 3500]]) == "STABLE"


def test_centrifuge_3000_rpm_is_not_a_drop():
    assert verify_storage_centrifuge([[3000, 3000, 3000]]) == "STABLE"


def test_centrifuge_streak_resets_between_runs():
    # last rpm of run 1 and first rpm of run 2 are both low, but must NOT combine
    assert verify_storage_centrifuge([[3500, 2900], [2900, 3500]]) == "STABLE"


def test_centrifuge_abort_in_second_run():
    assert verify_storage_centrifuge([[3500, 3500], [2000, 2000]]) == "ABORT_SPIN"


def test_centrifuge_empty_run_is_stable():
    assert verify_storage_centrifuge([[]]) == "STABLE"
