"""
Module: connection.py
Description: Handles zero-trust authentication and establishes secure sessions with Snowflake.
"""
import snowflake.connector
import streamlit as st

@st.cache_resource(ttl=300)
def get_snowflake_connection(account: str, user: str, password: str, mfa_token: str):
    """
    Establishes a stateless, MFA-authenticated connection to Snowflake.
    Credentials are processed in-memory and never cached persistently.
    """
    try:
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            passcode=mfa_token,
            warehouse='COMPUTE_WH',
            database='AEGIS_DB',  
            schema='AEGIS_CORE'
        )
        return conn
    except Exception as e:
        raise ConnectionError(f"Authentication failed. Verify credentials and MFA token. Details: {str(e)}")