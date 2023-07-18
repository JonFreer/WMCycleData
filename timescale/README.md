## Timescale

There are 3 core tables COUNTS, COUNTERS and COUNTS_HOURLY

The COUNTERS table stores:
- Identity: the unique vivacity id of the table
- Name: custom name of the counter
- Lat/Lon
- Location Desc: Description of counter location

The COUNTS and COUNTS_HOURLY table stores:
- Identity: the identity of the counter
- Timestamp: UTC timestamp
- Counts In
- Counts Out
- Mode: the mode of transport eg "cyclist"

The counts table should be viewed as a short term cache before the counts are rolled into hourly aggregates in the COUNTS_HOURLY table.

The set up of these tables and continuous aggregate functions is defined in the models.py file.