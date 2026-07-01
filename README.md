Medical Telegram Warehouse
Shipping a Data Product: From Raw Telegram Data to an Analytical API

An end-to-end data engineering pipeline that extracts Telegram medical business data, transforms it into a structured data warehouse, enriches it with computer vision (YOLO), and exposes insights through a FastAPI analytical service.

🚀 Project Overview

This project builds a modern ELT data platform for analyzing Ethiopian medical product trends from Telegram channels.

We process raw Telegram data → store in a data lake → load into PostgreSQL → transform with dbt → enrich with YOLO → expose insights via FastAPI → orchestrate with Dagster.

🎯 Business Goals
Identify top mentioned medical products
Analyze price/availability trends across channels
Measure visual content usage in posts
Track posting trends over time
Compare engagement across content types
🏗️ Architecture
Telegram Channels
        ↓
📥 Scraper (Telethon)
        ↓
🗂️ Data Lake (JSON + Images)
        ↓
🐘 PostgreSQL (Raw Schema)
        ↓
🧹 dbt Transformations
        ↓
📊 Star Schema (Marts)
        ↓
👁️ YOLOv8 Image Enrichment
        ↓
🚀 FastAPI Analytical Layer
        ↓
⚙️ Dagster Orchestration
📁 Project Structure
medical-telegram-warehouse/
│
├── .github/workflows/         # CI tests
├── .vscode/                   # VS Code settings
├── data/                      # Raw + processed data lake
│   ├── raw/
│   └── images/
│
├── src/                       # Core pipelines
│   ├── scraper.py
│   ├── yolo_detect.py
│
├── api/                       # FastAPI service
│   ├── main.py
│   ├── database.py
│   └── schemas.py
│
├── medical_warehouse/        # dbt project
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   ├── tests/
│   ├── dbt_project.yml
│
├── scripts/                   # ETL loaders
├── notebooks/                 # Exploration
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
🧩 Task Breakdown
🟢 Task 1 — Data Scraping & Data Lake
Goal

Extract Telegram messages and images from medical channels.

What you build:
Telegram scraper using Telethon
Raw JSON data lake
Image downloader pipeline
Logging system
Output:
data/raw/telegram_messages/YYYY-MM-DD/channel.json
data/raw/images/channel_name/message_id.jpg
logs/scraper.log
Key Fields Collected:
message_id
channel_name
message_date
message_text
views
forwards
has_media
image_path
🟡 Task 2 — Data Modeling (dbt)
Goal

Transform raw data into a clean analytical warehouse.

Steps:
Load JSON → PostgreSQL raw schema
Build staging models (cleaning + typing)
Create star schema
Star Schema Design:
Dimension Tables
dim_channels
dim_dates
Fact Table
fct_messages
dbt Tests:
Primary key uniqueness
Not-null constraints
Relationship integrity
Custom tests:
no future messages
non-negative views
🔵 Task 3 — YOLO Image Enrichment
Goal

Use computer vision to classify Telegram images.

Steps:
Run YOLOv8 (yolov8n.pt)
Detect objects in images
Classify images:
Category	Meaning
promotional	person + product
product_display	product only
lifestyle	person only
other	none
Output Table:

fct_image_detections

Includes:

message_id
detected_class
confidence_score
image_category
🟣 Task 4 — FastAPI Analytical Layer
Goal

Expose warehouse insights via REST API.

Endpoints:
1. Top Products
GET /api/reports/top-products?limit=10
2. Channel Activity
GET /api/channels/{channel_name}/activity
3. Message Search
GET /api/search/messages?query=drug
4. Visual Content Stats
GET /api/reports/visual-content
Features:
Pydantic validation
Error handling
Auto Swagger docs (/docs)
🟠 Task 5 — Dagster Orchestration
Goal

Automate the full pipeline.

Pipeline Steps:
scrape_telegram_data
load_raw_to_postgres
run_dbt_transformations
run_yolo_enrichment
Run UI:
dagster dev -f pipeline.py

Access:

http://localhost:3000
🧪 Data Quality & Testing
dbt tests for warehouse integrity
Custom SQL validation tests
Logging for pipeline observability
Error handling for API + scraping
⚙️ Tech Stack
Python (Telethon, FastAPI)
PostgreSQL
dbt (Data Build Tool)
YOLOv8 (Ultralytics)
Dagster (Orchestration)
Docker
GitHub Actions
📊 Key Insights we Will Produce
Most mentioned medical products
Channel comparison (activity + engagement)
Visual vs non-visual post performance
Image content classification trends
🧠 Learning Outcomes
ELT pipeline design
Dimensional modeling (Star Schema)
Data engineering best practices
Computer vision integration in analytics
API development for data products
Workflow orchestration
🚀 How to Run
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start PostgreSQL
docker-compose up -d

# 3. Run scraper
python src/scraper.py

# 4. Load raw data
python scripts/load_to_postgres.py

# 5. Run dbt
cd medical_warehouse
dbt run
dbt test

# 6. Run YOLO enrichment
python src/yolo_detect.py

# 7. Start API
uvicorn api.main:app --reload

# 8. Start Dagster
dagster dev -f pipeline.py
📌 Deliverables Checklist
 Telegram scraper
 Raw data lake
 PostgreSQL warehouse
 dbt models + tests
 YOLO image enrichment
 FastAPI service
 Dagster pipeline
 Documentation

🏁 Final Note

This project is a full production-style data engineering system, combining:

Data Engineering + Data Modeling + AI + API + Orchestration