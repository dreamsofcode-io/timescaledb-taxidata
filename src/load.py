import psycopg
import psycopg2
import os
import pyarrow.parquet as pq
from glob import glob
from multiprocessing import Pool
import time
from dotenv import load_dotenv

load_dotenv()
pguri = os.environ["DATABASE_URL"]
conn_dict = psycopg.conninfo.conninfo_to_dict(pguri)

os.makedirs("data/converted", exist_ok=True)


def handle_file(file, columns, cabid):
    conn = psycopg2.connect(**conn_dict)

    print(f"Processing {file} at {time.time()}")
    trips = pq.read_table(file)
    trips = trips.to_pandas()
    trips = trips.iloc[:, columns]
    trips["cabid"] = cabid

    output = file.replace("parquet", "csv").replace("data/", "data/converted/")
    trips.to_csv(output, index=False)
    print(f"File {file} converted to csv at {time.time()}")

    cur = conn.cursor()
    f = open(output, "r")
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
    conn.close()
    print(f"File {file} loaded to db at {time.time()}")


def handle_green(file):
    if "green_tripdata_2023" in file:
        print(f"Skipping {file}")
        return

    pickup_col = 1
    dropoff_col = 2
    distance_col = 8
    tip_col = 12
    total_col = 16

    handle_file(
        file=file,
        columns=[pickup_col, dropoff_col, distance_col, tip_col, total_col],
        cabid=2,
    )


def handle_yellow(file):
    if "yellow_tripdata_2023" in file:
        print(f"Skipping {file}")
        return

    handle_file(file=file, columns=[1, 2, 4, 15, 17], cabid=1)


if __name__ == "__main__":
    concurrency = 2

    # Get the files that have already been loaded
    conn = psycopg2.connect(**conn_dict)
    cur = conn.cursor()
    cur.execute("select filename from data_loaded")
    loaded = cur.fetchall()
    loaded = set([x[0] for x in loaded])
    conn.close()

    yellow_files = glob("./data/yellow_tripdata_*.parquet")
    yellow_files = [x for x in yellow_files if x not in loaded]

    green_files = glob("./data/green_tripdata_*.parquet")
    green_files = [x for x in green_files if x not in loaded]

    with Pool(concurrency) as p:
        p.map(handle_yellow, yellow_files)
        p.map(handle_green, green_files)

    conn = psycopg2.connect(**conn_dict)
    cur = conn.cursor()
    cur.execute("INSERT INTO trips SELECT * FROM trips_hyper")
    conn.commit()
    conn.close()

    print("Done!")
