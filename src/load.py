import psycopg
import psycopg2
import os
import pyarrow.parquet as pq
from glob import glob
from multiprocessing import Pool
import time

pguri = os.environ["DATABASE_URL"]
conn_dict = psycopg.conninfo.conninfo_to_dict(pguri)

def handle_file(file, columns, cabid):
    conn = psycopg2.connect(**conn_dict)

    print(f"Processing {file} at {time.time()}")
    trips = pq.read_table(file)
    trips = trips.to_pandas()
    trips = trips.iloc[:, columns]
    trips["cabid"] = cabid

    output = file.replace("parquet", "csv").replace("data/", "converted/")
    trips.to_csv(output, index=False)
    print(f"File {file} converted to csv")

    f = open(output, "r")
    cur = conn.cursor()
    copy_sql = """
           COPY trips_hyper FROM stdin WITH CSV HEADER
           DELIMITER as ','
           """
    cur.copy_expert(sql=copy_sql, file=f)
    cur.execute(
        f"INSERT INTO data_loaded (filename, loaded_at) VALUES ('{file}', now())"
    )
    conn.commit()
    f.close()

    os.remove(output)


def handle_green(file):
    pickup_col = 1
    dropoff_col = 2
    distance_col = 8
    tip_col = 12
    total_col = 16

    handle_file(file=file, columns=[pickup_col, dropoff_col, distance_col, tip_col, total_col], cabid=2)


def handle_yellow(file):
    handle_file(file=file, columns=[1, 2, 4, 15, 17], cabid=1)


if __name__ == "__main__":
    concurrency = 2

    # Get the files that have already been loaded
    conn = psycopg2.connect(**conn_dict)
    cur = conn.cursor()
    cur.execute("SELECT filename FROM data_loaded")
    loaded = cur.fetchall()
    loaded = set([x[0] for x in loaded])
    conn.close()

    yellow_files = glob("./data/yellow_tripdata_*.parquet")
    yellow_files = [x for x in yellow_files if x not in loaded]

    green_files = glob("./data/yellow_tripdata_*.parquet")
    green_files = [x for x in green_files if x not in loaded]

    with Pool(concurrency) as p:
        p.map(handle_yellow, yellow_files)
        p.map(handle_green, green_files)
