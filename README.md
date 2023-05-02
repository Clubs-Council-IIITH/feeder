# Data Feeder

A service meant to populate the database with CSV data.

## Usage
1. Place the CSVs inside a directory named `data`. 
2. Make sure the CSVs are appropriately named (`events.csv`, `clubs.csv`, `members.csv`, `users.csv`)
3. Run the feeder service. (`make start S=feeder`)

## Note
Run `make logs S=feeder` to check the status and logs.  
Each CSV once fed will be renamed to `<file>_<timestamp_when_done>.csv` to prevent the feeder from trying to push data from the same file repeatedly.
