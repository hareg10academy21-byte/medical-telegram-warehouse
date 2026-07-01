from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from api.database import get_db

app = FastAPI(
    title="Medical Telegram Analytical API",
    description="Analytics API built on dbt warehouse",
    version="1.0.0"
)

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"message": "API is running successfully"}


# =========================
# 1. TOP PRODUCTS
# =========================
@app.get("/api/reports/top-products")
def top_products(limit: int = 10, db: Session = Depends(get_db)):

    try:
        query = text("""
            SELECT product, COUNT(*) AS count
            FROM analytics.fct_messages
            WHERE product IS NOT NULL
            GROUP BY product
            ORDER BY count DESC
            LIMIT :limit
        """)

        result = db.execute(query, {"limit": limit}).fetchall()

        return [
            {"product": row.product, "count": row.count}
            for row in result
        ]

    except Exception as e:
        return {"error": str(e)}


# =========================
# 2. CHANNEL ACTIVITY
# =========================
@app.get("/api/channels/{channel_name}/activity")
def channel_activity(channel_name: str, db: Session = Depends(get_db)):

    try:
        query = text("""
            SELECT DATE(created_at) AS date,
                   COUNT(*) AS message_count
            FROM analytics.fct_messages
            WHERE channel_name = :channel_name
            GROUP BY DATE(created_at)
            ORDER BY date
        """)

        result = db.execute(query, {"channel_name": channel_name}).fetchall()

        return [
            {"date": str(row.date), "message_count": row.message_count}
            for row in result
        ]

    except Exception as e:
        return {"error": str(e)}


# =========================
# 3. MESSAGE SEARCH
# =========================
@app.get("/api/search/messages")
def search_messages(query: str, limit: int = 20, db: Session = Depends(get_db)):

    try:
        sql = text("""
            SELECT id, channel_name, message, created_at
            FROM analytics.fct_messages
            WHERE message ILIKE :query
            ORDER BY created_at DESC
            LIMIT :limit
        """)

        result = db.execute(sql, {
            "query": f"%{query}%",
            "limit": limit
        }).fetchall()

        return [
            {
                "message_id": row.id,
                "channel_name": row.channel_name,
                "message": row.message,
                "created_at": str(row.created_at)
            }
            for row in result
        ]

    except Exception as e:
        return {"error": str(e)}


# =========================
# 4. VISUAL CONTENT
# =========================
@app.get("/api/reports/visual-content")
def visual_content(db: Session = Depends(get_db)):

    try:
        query = text("""
            SELECT channel_name,
                   COUNT(*) FILTER (WHERE has_image = true) AS image_count,
                   COUNT(*) AS total_messages
            FROM analytics.fct_messages
            GROUP BY channel_name
        """)

        result = db.execute(query).fetchall()

        return [
            {
                "channel_name": row.channel_name,
                "image_count": row.image_count,
                "total_messages": row.total_messages
            }
            for row in result
        ]

    except Exception as e:
        return {"error": str(e)}