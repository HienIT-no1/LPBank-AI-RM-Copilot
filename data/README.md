# Data Directory — LPBank Banking

This directory manages all dataset assets for the LPBank AI RM Copilot project.

---

## Directory Structure
- `source/`: Contains the original Excel spreadsheet (`LPB_AI_Banking_Realistic_Mock_Data_v2.xlsx`).
- `raw/`: 18 extracted CSV files representing the relational database tables (customers, accounts, cards, loans, transactions, signals).
- `catalogs/`: Business reference files and rule sets:
  - `PRODUCT_MASTER.csv`: Product catalog (Cards, Deposits, Loans).
  - `CAMPAIGN_MASTER.csv`: Marketing campaigns.
  - `PRODUCT_MATCHING_RULE.csv`: Rule mapping from signals to products.
  - `CAMPAIGN_MATCHING_RULE.csv`: Rule mapping from signals to campaigns.
  - `SAMPLE_PROMPTS.csv`: Benchmark evaluation prompts.

