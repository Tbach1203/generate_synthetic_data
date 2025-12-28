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

CATEGORY = {
    "Electronics": [
        "Mobile Phones", "Laptops", "Tablets", "Cameras"
    ],
    "Fashion": [
        "Jeans", "T-Shirts", "Jackets", "Shoes"
    ],
    "Home": [
        "Furniture", "Kitchen", "Decor"
    ],
    "Sports": [
        "Fitness", "Outdoor", "Cycling"
    ],
    "Beauty": [
        "Skincare", "Makeup", "Hair Care"
    ]
}

def insert_category(conn):
    fake = Faker()
    volume = 10
    try:
        with conn.cursor() as cur:
            parent_map = {}
            used_count = 0
            # 1️⃣ Random main categories (3–4)
            main_count = random.randint(3, 4)
            main_categories = random.sample(list(CATEGORY.keys()), main_count)

            for parent_name in main_categories:
                cur.execute("""
                    INSERT INTO category (category_name, parent_category_id, level, created_at)
                    VALUES (%s, NULL, 1, %s)
                    RETURNING category_id;
                """, (parent_name, fake.date_time_this_year()))
                parent_id = cur.fetchone()[0]
                parent_map[parent_name] = parent_id
                used_count += 1
            # 2️⃣ Insert sub categories until đủ 10
            remaining = volume - used_count
            sub_candidates = []
            for parent in main_categories:
                for child in CATEGORY[parent]:
                    sub_candidates.append((parent, child))
            random.shuffle(sub_candidates)
            for parent_name, child_name in sub_candidates[:remaining]:
                cur.execute("""
                    INSERT INTO category (category_name, parent_category_id, level, created_at)
                    VALUES (%s, %s, 2, %s);
                """, (
                    child_name,
                    parent_map[parent_name],
                    fake.date_time_this_year()
                ))
        conn.commit()
        print(f"Inserted {volume} categories successfully")
    except psycopg2.DatabaseError as e:
        conn.rollback()
        print("Error inserting category:", e)