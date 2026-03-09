
    # Aegis: Stateless Zero-Trust Data Pipeline & Observability SaaS

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Snowflake](https://img.shields.io/badge/Snowflake-Data_Warehouse-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Full_Stack_SaaS-red)
![Compliance](https://img.shields.io/badge/Compliance-FINMA%20%2F%20FCA-success)

## Business Context
In strictly regulated financial sectors (e.g., FINMA, FCA), data engineering pipelines must adhere to rigorous operational risk controls:
1. **API High Availability:** Fiat-to-crypto gateways and settlement APIs require real-time latency observability.
2. **Data Privacy (PII):** Sensitive financial data (e.g., wallet addresses, transaction volumes) must be strictly masked from standard developers under the "Need-to-Know" basis.

**Aegis** is an industry-agnostic Minimum Viable Enterprise (MVE) pipeline built as a **100% stateless web application**, demonstrating a production-grade approach to these challenges without relying on local secret management.

## Core Architecture Features

### 1. 100% Stateless Zero-Trust Portal
To eliminate local credential vulnerabilities (and bypass the need for `.env` files or complex Secrets Manager integrations for this repository), the frontend acts as a pure zero-trust gateway. Credentials and ephemeral **TOTP MFA Tokens** are passed directly from the UI to the data warehouse connector in-memory, never touching the disk.

### 2. Edition-Agnostic Dynamic Data Masking (RBAC)
Instead of relying on expensive Enterprise-tier `MASKING POLICY` features, this architecture implements a highly cost-effective **`SECURE VIEW`** model. Direct table access is completely revoked. The view dynamically masks wallet addresses and zero-outs financial amounts based on the `CURRENT_ROLE()` context (`DATA_ENGINEER` vs. `COMPLIANCE_OFFICER`), achieving strict regulatory compliance regardless of the underlying database license tier.

### 3. Integrated Telemetry Engine
A Python-driven ETL engine sits behind the UI. With a single click, it simulates real-time financial settlements while simultaneously probing external gateway APIs, logging HTTP status codes and millisecond latencies directly into the warehouse for high-availability auditing.

## Quick Start (No Local Config Required)

```bash
# 1. Clone the repository and install dependencies
pip install -r requirements.txt

# 2. Launch the stateless dashboard
streamlit run app.py

# 3. Authenticate

# Enter your Data Warehouse Account, User, Password, and a live TOTP MFA token directly in the UI to unlock the pipeline.

