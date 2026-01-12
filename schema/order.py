from psycopg2.extras import execute_batch
from faker import Faker
import random
import psycopg2

def order(conn):
    command = """
    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        order_date TIMESTAMP NOT NULL,

        seller_id INT NOT NULL,
        status VARCHAR(20) NOT NULL,

        total_amount DECIMAL(12,2) NOT NULL CHECK (total_amount >= 0),
        created_at TIMESTAMP NOT NULL,

        CONSTRAINT fk_orders_seller
            FOREIGN KEY (seller_id) REFERENCES seller(seller_id),

        CONSTRAINT chk_order_status
            CHECK (
                status IN (
                    'PLACED',
                    'PAID',
                    'SHIPPED',
                    'DELIVERED',
                    'CANCELLED',
                    'RETURNED'
                )
            )
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(command)
        conn.commit()
        print("Table order created or already exists")
    except psycopg2.DatabaseError as e:
        conn.rollback()
        print("Error creating table:", e)

def fetch_seller_ids(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT seller_id FROM seller;")
        seller_ids = [row[0] for row in cur.fetchall()]
    if not seller_ids:
        raise ValueError("No sellers found. Insert sellers before orders.")
    return seller_ids

ORDER_STATUSES = [
    "PLACED",
    "PAID",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
]

def insert_order(conn):
    fake = Faker()
    volume = 2500000
    batch_size=2000
    seller_ids = fetch_seller_ids(conn)

    orders = []

    for _ in range(volume):
        orders.append((
            fake.date_time_between(start_date="-3y", end_date="now"),
            random.choice(seller_ids),
            random.choice(ORDER_STATUSES),
            round(random.uniform(100_000, 50_000_000), 2),
            fake.date_time_between(start_date="-3y", end_date="now")
        ))

    sql = """
        INSERT INTO orders (
            order_date,
            seller_id,
            status,
            total_amount,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s);
    """

    try:
        with conn.cursor() as cur:
            for i in range(0, volume, batch_size):
                execute_batch(cur, sql, orders[i:i + batch_size])

        conn.commit()
        print(f"Inserted {volume} orders successfully")

    except Exception as e:
        conn.rollback()
        print("Error inserting orders:", e)