BEGIN;

CREATE table data_loaded (
  filename varchar not null primary key,
  loaded_at TIMESTAMPTZ not null
);

CREATE TABLE cab_types (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

INSERT INTO cab_types (name) VALUES ('yellow'), ('green'); 

COMMIT;
