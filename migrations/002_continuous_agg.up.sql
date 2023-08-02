CREATE MATERIALIZED VIEW total_summary_daily 
WITH (timescaledb.continuous) 
AS SELECT 
time_bucket(INTERVAL '1 day', started_at) AS bucket, 
AVG(total_amount), 
MAX(total_amount),
MIN(total_amount) 
FROM trips_hyper
WHERE total_amount > 0
GROUP BY bucket
WITH NO DATA;

SELECT add_continuous_aggregate_policy('total_summary_daily',
  start_offset => INTERVAL '1 year',
  end_offset => INTERVAL '1 month',
  schedule_interval => INTERVAL '1 hour');

