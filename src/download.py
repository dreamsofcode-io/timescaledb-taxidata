import time
import requests
import os

years = range(2009, 2023)
months = range(1, 13)

data_dir = "data"

os.makedirs(f"{data_dir}", exist_ok=True)


def download_file(prefix, year, month):
    if os.path.exists(f"{data_dir}/{prefix}_tripdata_{year}-{month:02d}.parquet"):
        print(f"File {prefix}_tripdata_{year}-{month:02d}.parquet exists, skipping")
        return

    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{prefix}_tripdata_{year}-{month:02d}.parquet"
    print(f"Downloading {url}")
    r = requests.get(url)

    if r.status_code == 403:
        print("rate limit detected, sleeping for 10 minutes")
        time.sleep(600)
        download_file(prefix, year, month)
        return
    elif r.status_code != 200:
        print("file not found, skipping")
        return

    with open(f"{data_dir}/{prefix}_tripdata_{year}-{month:02d}.parquet", "wb") as f:
        f.write(r.content)


table = (
    ("green", (2014, 1), (2024, 4)),
    ("yellow", (2009, 1), (2024, 4)),
)

for prefix, (start_year, start_month), (end_year, end_month) in table:
    for year in range(start_year, end_year):
        for month in range(1, 13):
            if year == start_year and month < start_month:
                continue
            if year == end_year - 1 and month > end_month:
                continue
            download_file(prefix, year, month)
