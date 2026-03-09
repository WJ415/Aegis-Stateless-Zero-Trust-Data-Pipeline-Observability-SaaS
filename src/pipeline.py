"""
Module: pipeline.py
Description: Executes the ETL pipeline, combining external API telemetry and mock settlement ingestion.
"""
import requests
import random
import uuid
import time

def execute_ingestion_pipeline(conn, progress_callback=None, status_callback=None):
    """
    Simulates high-throughput stablecoin transactions and API latency probing.
    """
    cursor = conn.cursor()
    target_api = "https://api.binance.com/api/v3/ping"
    api_name = "Fiat_Gateway_Probe" # 更加通用的命名

    for step in range(5):
        if status_callback:
            status_callback(f"Generating transaction batch {step + 1}/5...")

        # 1. Telemetry Probe
        status_code = 500
        latency_ms = 0
        is_healthy = False
        try:
            response = requests.get(target_api, timeout=5)
            status_code = response.status_code
            latency_ms = int(response.elapsed.total_seconds() * 1000)
            is_healthy = (status_code == 200 and latency_ms < 1000)
        except requests.RequestException:
            latency_ms = 5000 
            
        cursor.execute(f"""
            INSERT INTO AEGIS_DB.AEGIS_CORE.API_HEALTH_LOGS 
            (ENDPOINT_NAME, STATUS_CODE, LATENCY_MS, IS_HEALTHY)
            VALUES ('{api_name}', {status_code}, {latency_ms}, {is_healthy})
        """)

        # 2. Settlement Ingestion
        mock_sender = f"0x{uuid.uuid4().hex[:40]}"
        mock_receiver = f"0x{uuid.uuid4().hex[:40]}"
        mock_amount = round(random.uniform(100.0, 500000.0), 6)
        mock_risk = round(random.uniform(0.1, 99.9), 2)
        
        cursor.execute(f"""
            INSERT INTO AEGIS_DB.AEGIS_CORE.STABLECOIN_TRANSFERS 
            (SENDER_WALLET, RECEIVER_WALLET, AMOUNT_USDC, RISK_SCORE)
            VALUES ('{mock_sender}', '{mock_receiver}', {mock_amount}, {mock_risk})
        """)
        
        if progress_callback:
            progress_callback((step + 1) / 5)
        time.sleep(1)

    cursor.close()