BEGIN;

CREATE table trips (
  started_at TIMESTAMPTZ not null,
  ended_at TIMESTAMPTZ not null,
  distance float not null,
  tip_amount float,
  total_amount float,
  cab_type_id int not null references cab_types(id)
);

CREATE table trips_hyper (
  started_at TIMESTAMPTZ not null,
  ended_at TIMESTAMPTZ not null,
  distance float not null,
  tip_amount float,
  total_amount float,
  cab_type_id int not null references cab_types(id)
);

SELECT create_hypertable('trips_hyper', 'started_at');

COMMIT;
