import random
from faker import Faker
import psycopg2

def product(conn):
    command = """
    CREATE TABLE IF NOT EXISTS product (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR(200) NOT NULL,
        category_id INT NOT NULL,
        brand_id INT NOT NULL,
        seller_id INT NOT NULL,
        price DECIMAL(12,2) NOT NULL CHECK (price > 0),
        discount_price DECIMAL(12,2) NOT NULL CHECK (discount_price >= 0),
        stock_qty INT NOT NULL CHECK (stock_qty >= 0),
        rating FLOAT CHECK (rating BETWEEN 0 AND 5),
        created_at TIMESTAMP NOT NULL,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id) REFERENCES category(category_id),

    CONSTRAINT fk_product_brand
        FOREIGN KEY (brand_id) REFERENCES brand(brand_id),

    CONSTRAINT fk_product_seller
        FOREIGN KEY (seller_id) REFERENCES seller(seller_id),

    CONSTRAINT chk_discount_price
        CHECK (discount_price <= price)
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(command)
        conn.commit()
        print("Table brand created or already exists")
    except psycopg2.DatabaseError as e:
        conn.rollback()
        print("Error creating table:", e) 

def fetch_existing_ids(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT category_id FROM category;")
        category_ids = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT brand_id FROM brand;")
        brand_ids = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT seller_id FROM seller;")
        seller_ids = [row[0] for row in cur.fetchall()]

    if not category_ids or not brand_ids or not seller_ids:
        raise ValueError("category / brand / seller must exist before inserting products")

    return category_ids, brand_ids, seller_ids
 
def insert_product(conn):
    fake = Faker()
    volume = 200 
    try:
        category_ids, brand_ids, seller_ids = fetch_existing_ids(conn)

        with conn.cursor() as cur:
            for _ in range(volume):
                price = round(random.uniform(100_000, 50_000_000), 2)
                discount_price = round(price * random.uniform(0.7, 1.0), 2)

                cur.execute("""
                    INSERT INTO product (
                        product_name,
                        category_id,
                        brand_id,
                        seller_id,
                        price,
                        discount_price,
                        stock_qty,
                        rating,
                        created_at,
                        is_active
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    fake.catch_phrase(),
                    random.choice(category_ids),
                    random.choice(brand_ids),
                    random.choice(seller_ids),
                    price,
                    discount_price,
                    random.randint(0, 500),
                    round(random.uniform(3.0, 5.0), 1),
                    fake.date_time_between(start_date="-3y", end_date="now"),
                    random.choice([True, False])
                ))
        conn.commit()
        print(f"Inserted {volume} products successfully")
    except (psycopg2.DatabaseError, ValueError) as e:
        conn.rollback()
        print("Error inserting product:", e)