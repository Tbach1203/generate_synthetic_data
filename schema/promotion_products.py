import psycopg2
import random
from faker import Faker

def promotion_products(conn):
    command = """
    CREATE TABLE IF NOT EXISTS promotion_products (
        promo_product_id SERIAL PRIMARY KEY,
        promotion_id INT NOT NULL,
        product_id INT NOT NULL,
        created_at TIMESTAMP NOT NULL,

        CONSTRAINT fk_promo_product_promotion
            FOREIGN KEY (promotion_id)
            REFERENCES promotions(promotion_id),

        CONSTRAINT fk_promo_product_product
            FOREIGN KEY (product_id)
            REFERENCES product(product_id),

        CONSTRAINT uq_promotion_product
            UNIQUE (promotion_id, product_id)
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(command)
        conn.commit()
        print("Table promotion_products created or already exists")
    except psycopg2.DatabaseError as e:
        conn.rollback()
        print("Error creating table promotion_products:", e)

def fetch_existing_promo_product_ids(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT promotion_id FROM promotions;")
        promotion_ids = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT product_id FROM product;")
        product_ids = [row[0] for row in cur.fetchall()]

    if not promotion_ids or not product_ids:
        raise ValueError("promotion & product must exist before inserting promotion_products")

    return promotion_ids, product_ids

def insert_promotion_products(conn):
    fake = Faker()
    volume = 100
    try:
        promotion_ids, product_ids = fetch_existing_promo_product_ids(conn)
        used_pairs = set()
        with conn.cursor() as cur:
            inserted = 0
            while inserted < volume:
                promotion_id = random.choice(promotion_ids)
                product_id = random.choice(product_ids)

                if (promotion_id, product_id) in used_pairs:
                    continue

                used_pairs.add((promotion_id, product_id))

                cur.execute("""
                    INSERT INTO promotion_products (
                        promotion_id,
                        product_id,
                        created_at
                    )
                    VALUES (%s, %s, %s);
                """, (
                    promotion_id,
                    product_id,
                    fake.date_time_this_year()
                ))
                inserted += 1 
        conn.commit()
        print(f"Inserted {inserted} promotion_products successfully")

    except (psycopg2.DatabaseError, ValueError) as e:
        conn.rollback()
        print("Error inserting promotion_products:", e)
