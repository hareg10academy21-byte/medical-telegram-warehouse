from dagster import op, job


# =====================
# OP 1
# =====================
@op
def scrape_telegram_data():
    print("Scraping Telegram data...")
    return "scraped"


# =====================
# OP 2
# =====================
@op
def load_raw_to_postgres(data):
    print("Loading into Postgres...")
    return "loaded"


# =====================
# OP 3
# =====================
@op
def run_dbt_transformations(data):
    print("Running dbt models...")
    return "dbt_done"


# =====================
# OP 4
# =====================
@op
def run_yolo_enrichment(data):
    print("Running YOLO detection...")
    return "yolo_done"


# =====================
# JOB GRAPH (FIXED FLOW)
# =====================
@job
def medical_pipeline():
    data = scrape_telegram_data()
    data = load_raw_to_postgres(data)
    data = run_dbt_transformations(data)
    run_yolo_enrichment(data)