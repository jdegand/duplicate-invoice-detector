# Duplicate Invoice Detector

A Python-based financial ledger auditing system designed to automatically screen corporate transaction datasets for internal control anomalies. This tool simulates standard corporate compliance oversight (e.g., Sarbanes-Oxley / SOX controls) by scanning ledger data for duplicate charges, policy violations, and split transactions intended to bypass authorization thresholds.

## Core Financial Controls Enacted

* **Exact Duplicate Detection (Critical Severity)**: Scans for identical transactions (same merchant, amount, and day) submitted by different employee IDs to identify potential fraud or billing system processing errors.
* **Split Transaction / Threshold Bypass Auditing**: Identifies single-employee multi-swipes at the same merchant within a 15-minute window, highlighting transactions engineered to circumvent corporate card limit approval workflows.
* **Weekend Policy Enforcement**: Flags charges executed on Saturdays or Sundays to enforce internal travel and expense authorization policies.
* **Round-Number Padding Flag**: Surfaces transactions totaling flat round numbers (e.g., $100.00, $400.00) above a threshold, mitigating the risk of undocumented expense reimbursement claims.
* **Merchant Category Mismatch Detection**: Audits standard vendor listings against unexpected account logging categories to guarantee general ledger formatting and data integrity.

### Project Structure

```text
corporate-spend-audit/
│
├── data/
│   └── mock_corporate_ledger.csv      # Raw input corporate transaction ledger
│
├── outputs/
│   └── .gitkeep                       # Ensures output folder schema tracks in Git
│
├── .gitignore                         # Excludes system caches and audited datasets
├── ledger_audit.py                    # Isolated Python / Pandas auditing engine
├── README.md                          # Documentation and business compliance overview
└── requirements.txt                   # Application dependencies
```

### Setup & Execution

1. Clone the repository and navigate into the root directory.
2. Initialize and activate an isolated virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. Install the application dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the core audit engine:

    ```bash
    python3 ledger_audit.py
    ```

5. The system dynamically creates the `outputs/` directory and drops the generated report there. Import `outputs/audited_corporate_ledger.csv` directly into Google Sheets or Excel to execute conditional formatting rules on CRITICAL or WARNING flag cells.
