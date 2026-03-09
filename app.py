"""
Application: Aegis Observability Dashboard
Description: A stateless Streamlit application for monitoring API latency and auditing RBAC data masking.
"""
import streamlit as st
import pandas as pd
from src.connection import get_snowflake_connection
from src.pipeline import execute_ingestion_pipeline

st.set_page_config(page_title="Aegis Governance", layout="wide")
st.title("Aegis: Regulated Data Pipeline & Observability Dashboard")
st.markdown("A stateless Minimum Viable Enterprise (MVE) demonstrating FINMA-grade dynamic data masking and API telemetry.")

st.sidebar.header("Zero-Trust Security Gateway")
st.sidebar.markdown("Enter ephemeral credentials. No state is persisted.")

sf_account = st.sidebar.text_input("Snowflake Account:")
sf_user = st.sidebar.text_input("Username:")
sf_password = st.sidebar.text_input("Password:", type="password")
sf_mfa = st.sidebar.text_input("TOTP Token (MFA):", type="password")

if st.sidebar.button("Establish Secure Connection", type="primary"):
    if all([sf_account, sf_user, sf_password, sf_mfa]):
        st.session_state['is_connected'] = True
    else:
        st.sidebar.error("All credential fields are required.")

if st.session_state.get('is_connected'):
    try:
        conn = get_snowflake_connection(sf_account, sf_user, sf_password, sf_mfa)
        st.sidebar.success("Connection verified.")
        
        st.sidebar.markdown("---")
        st.sidebar.header("Pipeline Control")
        
        if st.sidebar.button("Execute Ingestion Pipeline", use_container_width=True):
            progress_bar = st.sidebar.progress(0)
            status_text = st.sidebar.empty()
            execute_ingestion_pipeline(conn, progress_bar.progress, status_text.text)
            status_text.success("Pipeline execution completed.")
            st.rerun()
            
        st.sidebar.markdown("---")
        st.sidebar.header("Compliance Audit")
        selected_role = st.sidebar.radio("Assume Role Context:", ["DATA_ENGINEER", "COMPLIANCE_OFFICER"])
        
        cursor = conn.cursor()
        cursor.execute(f"USE ROLE {selected_role}")
        
        st.subheader("1. API Observability (Latency)")
        health_df = pd.read_sql("SELECT TIMESTAMP, LATENCY_MS, STATUS_CODE FROM API_HEALTH_LOGS ORDER BY TIMESTAMP DESC LIMIT 30", conn)
        if not health_df.empty:
            st.line_chart(health_df.set_index('TIMESTAMP')['LATENCY_MS'], color="#D92D20")
        else:
            st.warning("No telemetry data available. Execute the pipeline to generate logs.")
            
        st.markdown("---")

        st.subheader("2. PII Data Masking Audit")
        vault_df = pd.read_sql("SELECT TIMESTAMP, SENDER_WALLET, RECEIVER_WALLET, AMOUNT_USDC, RISK_SCORE FROM VW_STABLECOIN_TRANSFERS_SECURE ORDER BY TIMESTAMP DESC LIMIT 10", conn)
        st.dataframe(vault_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"System Error: {e}")
        st.cache_resource.clear()
        st.session_state['is_connected'] = False