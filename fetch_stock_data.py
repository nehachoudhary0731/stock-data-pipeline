import os
import requests
import psycopg2
from psycopg2.extras import execute_values

def fetch_and_store_stock_data():
    try:
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        symbol = "AAPL"  # example stock
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=60min&apikey={api_key}"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract time series
        time_series = data.get("Time Series (60min)", {})
        records = []
        for timestamp, values in time_series.items():
            records.append((
                timestamp,
                float(values["1. open"]),
                float(values["2. high"]),
                float(values["3. low"]),
                float(values["4. close"]),
                int(values["5. volume"])
            ))

        # Insert into Postgres
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="postgres"
        )
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_data (
            timestamp TIMESTAMP PRIMARY KEY,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            volume BIGINT
        )
        """)

        insert_query = """
        INSERT INTO stock_data (timestamp, open, high, low, close, volume)
        VALUES %s
        ON CONFLICT (timestamp) DO NOTHING
        """
        execute_values(cursor, insert_query, records)

        conn.commit()
        cursor.close()
        conn.close()

        print("Data inserted successfully!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_store_stock_data()