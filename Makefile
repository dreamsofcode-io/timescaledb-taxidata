#!make
include .env
export $(shell sed 's/=.*//' .env)

# Run the hypertable migration
migrate-hypertable:
	@echo "Running hypertable migration"
	migrate -path ./migrations -database $(DATABASE_URL) goto 1

# Run the continuous aggregate migration
migrate-aggregate:
	@echo "Running continuous aggregate migration"
	migrate -path ./migrations -database $(DATABASE_URL) goto 2
	psql $(DATABASE_URL) -c "CALL refresh_continuous_aggregate('total_summary_daily', '2008-12-31', '2023-01-01');"
