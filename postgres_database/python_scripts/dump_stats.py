import psycopg2
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection details from .env
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# SQL query to fetch the write-related statistics from pg_stat_statements
QUERY = """
SELECT
    queryid,
    query,
    COALESCE(shared_blks_written, 0) * 8192 AS bytes_written,  -- Convert shared blocks written to bytes
    COALESCE(blk_write_time, 0) AS blk_write_time  -- Time spent writing blocks in milliseconds
FROM
    pg_stat_statements;
"""

def collect_stats(conn):
    """Collects statistics from pg_stat_statements."""
    with conn.cursor() as cursor:
        cursor.execute(QUERY)
        return cursor.fetchall()

def dump_stats_to_file(stats, filename):
    """Dumps statistics to a JSON file with a timestamp."""
    timestamp = datetime.now().isoformat()
    data = {
        "timestamp": timestamp,
        "stats": stats
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Stats dumped to {filename} at {timestamp}")

def main():
    # Connect to the database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    try:
        # Collect statistics
        stats = collect_stats(conn)
        # Convert stats to a more readable format
        stats = [{"queryid": row[0], "bytes_written": row[2], "blk_write_time": row[3]} for row in stats]

        # Define the output file with a timestamp
        output_filename = f"pg_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        dump_stats_to_file(stats, output_filename)

    finally:
        conn.close()

if __name__ == "__main__":
    main()
