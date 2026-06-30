from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text

from api.database import get_db

app = FastAPI(
    title="Medical Telegram Warehouse API",
    description="Analytical API for Telegram Medical Data",
    version="1.0"
)


@app.get("/")
def home():
    return {"message": "Medical Telegram Warehouse API"}


# --------------------------------------------------
# Endpoint 1
# Top Products (Most Common Words)
# --------------------------------------------------

@app.get("/api/reports/top-products")
def top_products(
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):

    query = text("""

    WITH words AS (

        SELECT
            lower(word) AS term

        FROM raw.fct_messages,
        regexp_split_to_table(message_text,'\\s+') word

    )

    SELECT

        term,

        COUNT(*) AS count

    FROM words

    WHERE length(term) > 3

    GROUP BY term

    ORDER BY count DESC

    LIMIT :limit

    """)

    return db.execute(query, {"limit": limit}).mappings().all()


# --------------------------------------------------
# Endpoint 2
# Channel Activity
# --------------------------------------------------

@app.get("/api/channels/{channel_name}/activity")
def channel_activity(
    channel_name: str,
    db: Session = Depends(get_db)
):

    query = text("""

    SELECT

        d.full_date,

        COUNT(*) AS total_posts

    FROM raw.fct_messages f

    JOIN raw.dim_dates d

    ON f.date_key=d.date_key

    JOIN raw.dim_channels c

    ON f.channel_key=c.channel_key

    WHERE c.channel_name=:channel

    GROUP BY d.full_date

    ORDER BY d.full_date

    """)

    return db.execute(
        query,
        {"channel": channel_name}
    ).mappings().all()


# --------------------------------------------------
# Endpoint 3
# Message Search
# --------------------------------------------------

@app.get("/api/search/messages")
def search_messages(
    query: str,
    limit: int = 20,
    db: Session = Depends(get_db)
):

    sql = text("""

    SELECT

        message_id,

        message_text,

        views

    FROM raw.fct_messages

    WHERE message_text ILIKE :query

    LIMIT :limit

    """)

    return db.execute(

        sql,

        {
            "query": f"%{query}%",
            "limit": limit
        }

    ).mappings().all()


# --------------------------------------------------
# Endpoint 4
# Visual Content
# --------------------------------------------------

@app.get("/api/reports/visual-content")
def visual_content(
    db: Session = Depends(get_db)
):

    query = text("""

    SELECT

        image_category,

        COUNT(*) AS total_posts,

        ROUND(AVG(confidence_score),2) AS avg_confidence

    FROM raw.fct_image_detections

    GROUP BY image_category

    ORDER BY total_posts DESC

    """)

    return db.execute(query).mappings().all()