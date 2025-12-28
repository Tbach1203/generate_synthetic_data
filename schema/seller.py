import random
from faker import Faker
import psycopg2

def seller(conn):
    command = """
    CREATE TABLE IF NOT EXISTS seller (
        seller_id SERIAL PRIMARY KEY,
        seller_name VARCHAR(150) NOT NULL,
        join_date DATE NOT NULL,
        seller_type VARCHAR(50) NOT NULL,
        rating DECIMAL(2,1) NOT NULL CHECK (rating BETWEEN 0 AND 5),
        country VARCHAR(50) NOT NULL
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(command)
        conn.commit()
        print("Table seller created or already exists") 
    except psycopg2.DatabaseError as e:
        conn.rollback()
        print("Error creating table:", e)

SELLER_TYPES = [
    "Official",              # Gian hàng chính hãng
    "Official Store",        # Flagship store
    "Marketplace",           # Người bán thường
    "Mall",                  # Gian hàng Mall
    "Authorized Reseller",   # Nhà phân phối ủy quyền
    "Distributor",           # Nhà phân phối
    "Retailer",              # Bán lẻ
    "Wholesale",             # Bán sỉ
    "Local Shop"             # Cửa hàng địa phương
]

def insert_seller(conn):
    fake = Faker("vi_VN")
    volume = 25
    try:
        with conn.cursor() as cur:
            for _ in range(volume):
                seller_name = fake.company()
                join_date = fake.date_between(start_date="-5y", end_date="today")
                seller_type = random.choice(SELLER_TYPES)
                rating = round(random.uniform(3.0, 5.0), 1)

                cur.execute("""
                    INSERT INTO seller (
                        seller_name,
                        join_date,
                        seller_type,
                        rating,
                        country
                    )
                    VALUES (%s, %s, %s, %s, %s);
                """, (
                    seller_name,
                    join_date,
                    seller_type,
                    rating,
                    "Vietnam"
                ))
        conn.commit()
        print(f"Inserted {volume} sellers successfully")

    except psycopg2.DatabaseError as e:
        conn.rollback()
        print("Error inserting seller:", e)