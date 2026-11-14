import math
import re

VALID_ANTIGENS = {"A", "B", "AB", "O"}
RH_MAP = {"+": "Positive", "-": "Negative"}

_BP_PATTERN = re.compile(r"\s*(\d{1,3})\s*/\s*(\d{1,3})\s*", re.ASCII)


def validate_blood_type(blood_code):
    """
    Standardizes blood group and Rh factor (e.g. 'O+', 'AB-').
    Returns 'Invalid blood type' for anything that is not a valid ABO group
    (A, B, AB, O) followed by '+' or '-'. Never raises.
    """
    if not isinstance(blood_code, str):
        return "Invalid blood type"
    cleaned = blood_code.strip().upper()
    if len(cleaned) < 2:
        return "Invalid blood type"
    antigen, rh_char = cleaned[:-1], cleaned[-1]
    if antigen not in VALID_ANTIGENS or rh_char not in RH_MAP:
        return "Invalid blood type"
    return f"{antigen} {RH_MAP[rh_char]}"


def calculate_pulse_pressure(bp_string):
    """
    Calculates pulse pressure (systolic - diastolic) and arterial ratio.
    Expects 'systolic/diastolic' (e.g. '120/80'), 1-3 digits each,
    diastolic > 0 and systolic >= diastolic. Never raises.
    """
    if not isinstance(bp_string, str):
        return "Invalid BP format"
    match = _BP_PATTERN.fullmatch(bp_string)
    if match is None:
        return "Invalid BP format"
    systolic, diastolic = int(match.group(1)), int(match.group(2))
    if diastolic == 0 or systolic < diastolic:
        return "Invalid BP values"
    pulse_diff = systolic - diastolic
    ratio = round(systolic / diastolic, 2)
    return f"Diff: {pulse_diff}, Ratio: {ratio}"


def parse_donor_registry(donor_entry):
    """
    Parses pipe-delimited record: 'DonorID|WeightKg|Hemoglobin'.
    Returns 'Invalid donor record' for malformed input (wrong token count,
    empty ID, non-numeric / NaN / infinite / non-positive numbers). Never raises.
    """
    if not isinstance(donor_entry, str):
        return "Invalid donor record"
    fields = donor_entry.split('|')
    if len(fields) != 3:
        return "Invalid donor record"
    donor_id = fields[0].strip()
    if not donor_id:
        return "Invalid donor record"
    try:
        weight = float(fields[1])
        hemoglobin = float(fields[2])
    except (ValueError, OverflowError):
        return "Invalid donor record"
    if not (math.isfinite(weight) and math.isfinite(hemoglobin)):
        return "Invalid donor record"
    if weight <= 0 or hemoglobin <= 0:
        return "Invalid donor record"
    eligible = weight >= 50.0 and hemoglobin >= 12.5
    return f"Donor {donor_id}: {'Eligible' if eligible else 'Deferred'}"


def main():
    print("==== Running validate_blood_type ====")
    b_input = input("Enter blood type (e.g. A+, O-, AB+): ")
    print("Validated:", validate_blood_type(b_input))

    print("\n==== Running calculate_pulse_pressure ====")
    bp_input = input("Enter BP (e.g. 120/80): ")
    print("BP Metrics:", calculate_pulse_pressure(bp_input))

    print("\n==== Running parse_donor_registry ====")
    d_input = input("Enter record (ID|Weight|Hemoglobin): ")
    print("Status:", parse_donor_registry(d_input))


if __name__ == "__main__":
    main()