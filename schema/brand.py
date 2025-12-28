import psycopg2
from faker import Faker

def brand(conn):
    command = """
    CREATE TABLE IF NOT EXISTS brand (
        brand_id SERIAL PRIMARY KEY,
        brand_name VARCHAR(100) NOT NULL,
        country VARCHAR(50),
        created_at TIMESTAMP
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

def insert_brand(conn):
    fake = Faker()
    volume = 20
    command = """
        INSERT INTO brand (brand_name, country, created_at)
        VALUES (%s, %s, %s);
    """
    try:
        with conn.cursor() as cur:
            for _ in range(volume):
                brand_name = fake.company()
                country = fake.country()
                created_at = fake.date_time_this_decade()

                cur.execute(command, (brand_name, country, created_at))

        conn.commit()
        print(f"Inserted {volume} brands successfully")
    except psycopg2.DatabaseError as e:
        conn.rollback()
        print("Error inserting brand data:", e)