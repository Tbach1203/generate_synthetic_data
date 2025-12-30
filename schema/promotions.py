import psycopg2
import random
from faker import Faker
from datetime import timedelta

def promotions(conn):
    command = """
    CREATE TABLE IF NOT EXISTS promotions (
        promotion_id SERIAL PRIMARY KEY,
        promotion_name VARCHAR(100) NOT NULL,
        promotion_type VARCHAR(50) NOT NULL,
        discount_type VARCHAR(20) NOT NULL,
        discount_value NUMERIC(10,2) NOT NULL CHECK (discount_value > 0),
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,

        CONSTRAINT chk_promotion_type 
            CHECK (
                promotion_type IN (
                    'product',
                    'category',
                    'seller',
                    'flash_sale',
                    'site_wide'
                )
            ),

        CONSTRAINT chk_discount_type
        CHECK (
            discount_type IN (
                'percentage',
                'fixed_amount'
            )
        ),

        CONSTRAINT chk_date_range
            CHECK (end_date > start_date)
    );    
    """
    try:
        with conn.cursor() as cur:
            cur.execute(command)
        conn.commit()
        print("Table promotions created or already exists")
    except psycopg2.DatabaseError as e:
        print("Error creating table:", e)

PROMOTION_TYPES = [
    "product",
    "category",
    "seller",
    "flash_sale",
    "site_wide"
]

DISCOUNT_TYPES = [
    "percentage",
    "fixed_amount"
]

PROMOTION_NAMES = [
    "Mega Sale",
    "Super Deal",
    "Flash Sale",
    "Hot Promotion",
    "Big Saving",
    "Weekend Sale",
    "Holiday Deal",
    "Special Offer"
]

def insert_promotions(conn):
    fake = Faker()
    volume = 10
    try:
        with conn.cursor() as cur:
            for _ in range(volume):
                discount_type = random.choice(DISCOUNT_TYPES)

                if discount_type == "percentage":
                    discount_value = round(random.uniform(5, 50), 2)
                else:
                    discount_value = round(random.uniform(10_000, 500_000), 2)

                start_date = fake.date_between(start_date="-1y", end_date="today")
                end_date = start_date + timedelta(days=random.randint(30, 50))

                promotion_name = f"{random.choice(PROMOTION_NAMES)} {start_date.strftime('%m.%d')}"

                cur.execute("""
                    INSERT INTO promotions (
                        promotion_name,
                        promotion_type,
                        discount_type,
                        discount_value,
                        start_date,
                        end_date
                    )
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (
                    promotion_name,
                    random.choice(PROMOTION_TYPES),
                    discount_type,
                    discount_value,
                    start_date,
                    end_date
                ))

        conn.commit()
        print(f"Inserted {volume} promotions successfully")

    except psycopg2.DatabaseError as e:
        conn.rollback()
        print("Error inserting promotion:", e)