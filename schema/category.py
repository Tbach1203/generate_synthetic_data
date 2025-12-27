import psycopg2
from faker import Faker
import random

def category(conn):
    command = """
    CREATE TABLE IF NOT EXISTS category (
        category_id SERIAL PRIMARY KEY,
        category_name VARCHAR(100) NOT NULL,
        parent_category_id INT NULL,
        level SMALLINT NOT NULL,
        created_at TIMESTAMP,
        CONSTRAINT fk_category_parent
            FOREIGN KEY (parent_category_id)
            REFERENCES category(category_id)
            ON DELETE SET NULL
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(command)
        conn.commit()
        print("Table category created or already exists")
    except psycopg2.DatabaseError as e:
        conn.rollback()
        print("Error creating category table:", e)

CATEGORY_NAMES = [
    "Electronics",
    "Fashion",
    "Home",
    "Sports",
    "Beauty",
    "Books",
    "Toys",
    "Automotive",
    "Health",
    "Groceries"
]

def insert_category(conn):
    fake = Faker()
    try:
        with conn.cursor() as cur:
            main_category_ids = []
            # 1️⃣ Insert main categories (level = 1)
            for name in CATEGORY_NAMES[:3]:
                cur.execute("""
                    INSERT INTO category (category_name, parent_category_id, level, created_at)
                    VALUES (%s, NULL, 1, %s)
                    RETURNING category_id;
                """, (name, fake.date_time_this_year()))
                main_category_ids.append(cur.fetchone()[0])

            # 2️⃣ Insert sub categories (level = 2)
            for name in CATEGORY_NAMES[3:]:
                parent_id = random.choice(main_category_ids)
                cur.execute("""
                    INSERT INTO category (category_name, parent_category_id, level, created_at)
                    VALUES (%s, %s, 2, %s);
                """, (name, parent_id, fake.date_time_this_year()))
        conn.commit()
        print("Inserted 10 categories")
    except psycopg2.DatabaseError as e:
        conn.rollback()
        print("Error inserting category:", e)
