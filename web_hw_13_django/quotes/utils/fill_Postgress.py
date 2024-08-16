import json

from psycopg2 import connect


def fill_authors():
    db = connect(
        host="localhost",
        database="postgres",
        port=5432,
        user="admin",
        password="admin"
    )

    with open("authors.json", "r", encoding="utf-8") as f:
        authors = json.load(f)
        for author in authors:
            query = "insert into quotes_author (fullname, born_date, born_location, description)  values ( %s, %s, %s, %s)"
            parameters = [value for value in author.values()]
            # print(parameters)
            db.cursor().execute(query, parameters)
    db.commit()
    db.close()


def fill_quotes_and_tags():
    db = connect(
        host="localhost",
        database="postgres",
        port=5432,
        user="admin",
        password="admin"
    )
    cursor = db.cursor()
    with open("quotes.json", "r", encoding="utf-8") as f:
        qoutes = json.load(f)
        for quote in qoutes:
            query_quote = "insert into quotes_quote (quote, author_id)  values ( %s, %s )"
            query_tag = "insert into quotes_tag (name) values ( %s ) ON CONFLICT (name) DO NOTHING"
            query_author_id = "select id from quotes_author where fullname = %s"
            query_quotes_tags = "insert into quotes_quote_tags (quote_id, tag_id) values ( %s, %s )"
            query_get_quote_id = "select id from quotes_quote where quote = %s"

            for tag in [tag.split(",") for tag in quote.get("tags")]:
                cursor.execute(query_tag, tag)
                db.commit()

            parameters = quote.get("author")
            cursor.execute(query_author_id, (parameters,))
            author_id = cursor.fetchall()
            parameters = [quote.get("quote"), author_id[0]]
            cursor.execute(query_quote, parameters)
            db.commit()
            cursor.execute(query_get_quote_id, (quote.get("quote"),))
            quote_id = cursor.fetchall()

            parameters = "'"
            for r in quote.get("tags"):
                parameters = parameters + r + "', '"
            parameters = parameters[:len(parameters)-3]
            if parameters > "":
                query_tags_id = "select id from quotes_tag where name in ( " + parameters + " )"
                cursor.execute(query_tags_id)
                tags_id = cursor.fetchall()
                for tag_id in tags_id:
                    parameters = [quote_id[0], tag_id]
                    cursor.execute(query_quotes_tags, parameters)
                    db.commit()

    db.close()


if __name__ == "__main__":
    fill_quotes_and_tags()
