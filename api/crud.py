from sqlalchemy import text


def search_messages(db, keyword, limit):

    query = text("""

        SELECT

            message_id,

            message_text

        FROM raw.fct_messages

        WHERE message_text ILIKE :kw

        LIMIT :limit

    """)

    return db.execute(

        query,

        {

            "kw": f"%{keyword}%",

            "limit": limit

        }

    ).mappings().all()