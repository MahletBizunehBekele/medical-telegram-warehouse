from dagster import job, op
import subprocess


@op
def scrape_telegram_data():
    subprocess.run(["python", "src/scraper.py"], check=True)
    return True


@op
def load_raw_to_postgres(_):
    subprocess.run(["python", "src/load_raw.py"], check=True)
    return True


@op
def run_dbt_transformations(_):
    subprocess.run(
        ["dbt", "run"],
        cwd="medical_warehouse",
        check=True,
    )
    return True


@op
def run_yolo_enrichment(_):
    subprocess.run(["python", "src/yolo_detect.py"], check=True)
    subprocess.run(["python", "src/load_detections.py"], check=True)


@job
def medical_pipeline():
    scrape = scrape_telegram_data()
    load = load_raw_to_postgres(scrape)
    dbt = run_dbt_transformations(load)
    run_yolo_enrichment(dbt)