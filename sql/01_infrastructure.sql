-- ==========================================
-- Aegis Infrastructure & Data Model Setup
-- ==========================================

-- 1. Initialize core database and switch context
CREATE DATABASE IF NOT EXISTS AEGIS_DB;
USE DATABASE AEGIS_DB;

-- Create a dedicated schema adhering to enterprise standards
CREATE SCHEMA IF NOT EXISTS AEGIS_CORE;
USE SCHEMA AEGIS_CORE;

-- 2. Create Table: API_HEALTH_LOGS
-- Logs telemetry data for fiat gateways and blockchain nodes
CREATE OR REPLACE TABLE AEGIS_DB.AEGIS_CORE.API_HEALTH_LOGS (
    LOG_ID VARCHAR DEFAULT UUID_STRING(), 
    TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    ENDPOINT_NAME VARCHAR(255),           
    STATUS_CODE INTEGER,                  
    LATENCY_MS INTEGER,                   
    IS_HEALTHY BOOLEAN                    
);

-- 3. Create Table: STABLECOIN_TRANSFERS
-- Acts as the Single Source of Truth (SSOT) for RBAC data masking
CREATE OR REPLACE TABLE AEGIS_DB.AEGIS_CORE.STABLECOIN_TRANSFERS (
    TX_ID VARCHAR DEFAULT UUID_STRING(),
    TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    SENDER_WALLET VARCHAR(255),           
    RECEIVER_WALLET VARCHAR(255),         
    AMOUNT_USDC NUMBER(38, 6),            
    RISK_SCORE NUMBER(5, 2)               
);

-- Insert baseline test data to validate schema
INSERT INTO AEGIS_DB.AEGIS_CORE.STABLECOIN_TRANSFERS (SENDER_WALLET, RECEIVER_WALLET, AMOUNT_USDC, RISK_SCORE)
VALUES ('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045', '0x28C6c06298d514Db089934071355E5743bf21d60', 150000.000000, 12.5);

SELECT * FROM AEGIS_DB.AEGIS_CORE.STABLECOIN_TRANSFERS;