# 
# 🩸 Blood Donation Screening
### Software Engineering Lab 6 & Lab 7

A Python-based software testing project covering **Code Coverage, Branch Coverage, and Fuzz Testing** using a Blood Donation Screening system.

---

## 📌 Project Overview

This repository contains the implementation and testing activities for:

- **Lab 6:** Code and Branch Coverage Analysis
- **Lab 7:** Fuzzing for Input Validation Bugs

The project focuses on testing input validation, boundary conditions, decision branches, and robustness against invalid or unexpected inputs.

---

## 📂 Repository Structure

```text
L6_L7_05_blood_donation_screening/
│
├── Lab 6/
│   ├── blood_donation_screening.py
│   ├── test_blood_donation.py
│   ├── CodeCoverageTest_blood_donation_screening.py
│   ├── BranchCoverageTest_blood_donation_screening.py
│   ├── code_coverage.png
│   └── README.md
│
├── Lab 7/
│   ├── processor.py
│   ├── test_processor.py
│   ├── 1_buggy_output.png
│   ├── 2_tests_failing.png
│   ├── 3_fixed_output.png
│   ├── 4_tests_passing.png
│   └── README.md
│
├── .gitignore
└── README.md
```

---

# 🧪 Lab 6 – Code and Branch Coverage Analysis

## Objective

To analyze the Python program using code coverage and branch coverage techniques and ensure that different execution paths are tested.

## Implementation

The program contains two main functions:

**1. `process_donor_cohort(cohorts, standard_volume_ml)`**

- Processes registered donor cohorts.
- Checks donor age and weight.
- Validates haemoglobin levels.
- Handles high-altitude cohort conditions.
- Applies fast-track bonuses.
- Returns the collection status.

**2. `verify_storage_centrifuge(centrifuge_runs)`**

- Checks centrifuge RPM readings.
- Detects consecutive RPM drops.
- Identifies whether a spin should be aborted.
- Returns the centrifuge status.

## Test Files

| File | Description |
|---|---|
| `blood_donation_screening.py` | Main implementation |
| `test_blood_donation.py` | Basic test cases |
| `CodeCoverageTest_blood_donation_screening.py` | Statement coverage tests |
| `BranchCoverageTest_blood_donation_screening.py` | Branch coverage tests |

## Technologies Used

- Python
- Pytest
- Coverage.py

## Execution

Navigate to the Lab 6 directory:

```bash
cd "Lab 6"
```

Install dependencies:

```bash
pip install pytest coverage
```

Run the tests:

```bash
python -m pytest -v
```

### Code Coverage

```bash
coverage run -m pytest CodeCoverageTest_blood_donation_screening.py
```

Generate the coverage report:

```bash
coverage report -m --include=blood_donation_screening.py
```

### Branch Coverage

```bash
coverage run --branch -m pytest BranchCoverageTest_blood_donation_screening.py
```

Generate the branch coverage report:

```bash
coverage report -m --include=blood_donation_screening.py
```

---

# 🔍 Lab 7 – Fuzzing for Input Validation Bugs

## Objective

To identify input validation bugs using fuzz testing and property-based testing with Hypothesis.

The tests generate different types of inputs, including valid values, invalid strings, empty values, and unexpected data types.

## Implementation

The `processor.py` file contains three main functions:

**1. `validate_blood_type(blood_code)`**

- Validates ABO blood groups.
- Checks Rh-positive and Rh-negative factors.
- Normalizes valid blood type inputs.
- Handles invalid input safely.

**2. `calculate_pulse_pressure(bp_string)`**

- Validates blood pressure input.
- Calculates pulse pressure difference.
- Calculates the systolic/diastolic ratio.
- Handles invalid blood pressure formats and values.

**3. `parse_donor_registry(donor_entry)`**

- Parses pipe-delimited donor records.
- Validates donor ID, weight, and haemoglobin.
- Checks numeric values.
- Determines eligible or deferred status.

## Test Files

| File | Description |
|---|---|
| `processor.py` | Input processing implementation |
| `test_processor.py` | Hypothesis-based fuzz tests |

## Technologies Used

- Python
- Pytest
- Hypothesis

## Execution

Navigate to the Lab 7 directory:

```bash
cd "Lab 7"
```

Install dependencies:

```bash
pip install pytest hypothesis
```

Run the tests:

```bash
python -m pytest -v
```

## Testing Approach

The fuzz tests cover:

- Random text inputs.
- Empty and null inputs.
- Unexpected data types.
- Invalid blood group formats.
- Invalid blood pressure values.
- Malformed donor registry records.
- Boundary conditions.
- Valid-input properties.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Implementation |
| Pytest | Test execution |
| Coverage.py | Code and branch coverage |
| Hypothesis | Property-based fuzz testing |
| Git & GitHub | Version control and repository management |

---

## 🎯 Learning Outcomes

- Understanding statement and branch coverage.
- Writing effective unit test cases.
- Testing boundary conditions.
- Identifying input validation bugs.
- Using property-based testing.
- Improving software reliability through systematic testing.

---

## ⚠️ Disclaimer

This project is an academic software testing exercise. The donor screening rules are illustrative and are not intended for real-world medical decisions.

---

## 👨‍💻 Author

**Sri Kanth G**

GitHub: [@srikanth97318](https://github.com/srikanth97318)

---

**Course:** Software Engineering Lab  
**Repository:** L6_L7_05_blood_donation_screening
