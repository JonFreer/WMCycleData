CREATE MATERIALIZED VIEW counts_daily
WITH (timescaledb.continuous) AS
SELECT
   time_bucket('1 day', timestamp) as timestamp,
   mode, counter,
   sum(count_in) as count_in, 
   sum(count_out) as count_out 
FROM counts
GROUP BY 1,2,3;

CREATE MATERIALIZED VIEW counts_weekly
WITH (timescaledb.continuous) AS
SELECT
   time_bucket('1 week', timestamp) as timestamp,
   mode, counter,
   sum(count_in) as count_in, 
   sum(count_out) as count_out 
FROM counts_daily
GROUP BY 1,2,3;

SELECT add_continuous_aggregate_policy('counts_daily',
  start_offset => INTERVAL '4 days',
  end_offset => NULL,
  schedule_interval => INTERVAL '6 hours');

SELECT add_continuous_aggregate_policy('conditions_weekly',
  start_offset => INTERVAL '1 month',
  end_offset => NULL,
  schedule_interval => INTERVAL '1 day');

# SELECT add_continuous_aggregate_policy('counts_hourly',
#   start_offset => INTERVAL '4 hours',
#   end_offset => NULL,
#   schedule_interval => INTERVAL '3 minutes');

# SELECT add_continuous_aggregate_policy('counts_hourly',
#   start_offset => INTERVAL '1 week',
#   end_offset => NULL,
#   schedule_interval => INTERVAL '1 day');

# SELECT add_retention_policy('counts', INTERVAL '30 days');