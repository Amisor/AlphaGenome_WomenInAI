# Automated Quality Assurance & Verification Suite

This directory contains automated unit and integration tests verifying the clinical validity, data integrity, and interface safety of the platform.

---

## Test Inventory

| Test Module | Coverage |
| :--- | :--- |
| **[`test_clinical_system.py`](test_clinical_system.py)** | • **Test 1**: Data schema validation of staged multigene panel findings.<br/>• **Test 2**: Strict clinician pivot verification (ensures zero direct-to-patient letters).<br/>• **Test 3**: Visual HTML report integrity, SVG tracks, AI assistant presence, warm editorial palette, zero emojis, zero doctor branding.<br/>• **Test 4**: Archetype distinctiveness across pathogenic, benign, and deep-intronic cases.<br/>• **Test 5**: Antigravity workspace skill specification conformance.<br/>• **Test 6**: Master review dashboard integrity and metric links. |

---

## Running Tests

Execute all tests from repository root:
```bash
python -m unittest discover tests
```
Or execute the test module directly:
```bash
python tests/test_clinical_system.py
```
