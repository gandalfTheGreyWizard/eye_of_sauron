#### Dump Stats
- the file [dump_stats.py](dump_stats.py) is a script that reads the state of pg_stat_statements table and keeps dumping stats to a file against the captured date and time
- The script can be scheduled with a cron to capture the logs evey minute

#### Calculate Writes
- This python file [calculate_writes.py](calculate_writes.py) is used to compare two files genererate by dump_stats.py and calculate the writes per second
