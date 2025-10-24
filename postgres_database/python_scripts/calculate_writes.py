import json
import sys
from datetime import datetime

def load_stats(filename):
    """Load stats from a JSON file."""
    with open(filename, "r") as f:
        data = json.load(f)
    timestamp = datetime.fromisoformat(data["timestamp"])
    stats = {row["queryid"]: row["bytes_written"] for row in data["stats"]}
    return timestamp, stats

def calculate_write_rate(file1, file2):
    """Calculate the write rate between two snapshots."""
    timestamp1, stats1 = load_stats(file1)
    timestamp2, stats2 = load_stats(file2)

    # Calculate time difference in seconds
    time_diff = (timestamp2 - timestamp1).total_seconds()

    if time_diff <= 0:
        print("Invalid time difference between snapshots.")
        return

    # Calculate the total bytes written difference
    total_bytes_written = 0

    # Iterate over the stats to calculate the total bytes written difference
    for queryid in stats2:
        bytes_written2 = stats2.get(queryid, 0)
        bytes_written1 = stats1.get(queryid, 0)
        bytes_diff = max(bytes_written2 - bytes_written1, 0)
        total_bytes_written += bytes_diff

    # Calculate the write rate
    write_rate = total_bytes_written / time_diff
    print(f"Total Bytes Written: {total_bytes_written} bytes")
    print(f"Average Write Rate: {write_rate:.2f} bytes/sec (~{write_rate / 1024:.2f} KB/sec)")

def main():
    if len(sys.argv) != 3:
        print("Usage: python calculate_write_rate.py <file1.json> <file2.json>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    calculate_write_rate(file1, file2)

if __name__ == "__main__":
    main()
