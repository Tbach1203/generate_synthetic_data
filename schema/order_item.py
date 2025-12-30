import psycopg2
from faker import Faker
import random
from psycopg2.extras import execute_batch

def order_item(conn):
    command = """
    CREATE TABLE IF NOT EXISTS order_item(
        order_item_id SERIAL PRIMARY KEY,
        order_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL CHECK (quantity > 0),
        unit_price DECIMAL(12,2) NOT NULL CHECK (unit_price > 0),
        subtotal DECIMAL(12,2) NOT NULL CHECK (subtotal >=0),

        CONSTRAINT fk_order_item_order
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
        
        CONSTRAINT fk_order_item_product
            FOREIGN KEY (product_id) REFERENCES product(product_id),
        
        CONSTRAINT chk_subtotal
            CHECK (subtotal = quantity * unit_price)
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(command)
        conn.commit()
        print("Table order_item created or already exists")
    except psycopg2.DatabaseError as e:
        conn.rollback()
        print("Error creating table:", e)

def fech_order_and_product_ids(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT order_id FROM orders")
        order_ids = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT product_id, discount_price FROM product")
        products = cur.fetchall()
    if not order_ids or not products:
        raise ValueError("Orders and products must exist before inserting order items")
    return order_ids, products

def insert_order_item(conn):
    order_ids, products = fech_order_and_product_ids(conn)
    volume = 1_000_000
    batch_size = 5000
    command = """
    INSERT INTO order_item (
        order_id,
        product_id,
        quantity,
        unit_price,
        subtotal
    )
    VALUES (%s, %s, %s, %s, %s);
    """
    items_buffer = []
    total_inserted = 0
    try:
        with conn.cursor() as cur:
            for order_id in order_ids:
                item_count = random.randint(2, 5)
                selected_products = random.sample(products, item_count)

                for product_id, unit_price in selected_products:
                    quantity = random.randint(1,5)
                    subtotal = quantity*unit_price
                    items_buffer.append((
                        order_id,
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    ))
                    total_inserted += 1

                    if total_inserted >= volume:
                        break
                if len(items_buffer) >= batch_size:
                    execute_batch(cur, command, items_buffer)
                    items_buffer.clear()
                if total_inserted >= volume:
                    break
            if items_buffer:
                execute_batch(cur, command, items_buffer)
                
        conn.commit()
        print(f"Inserted {total_inserted} order items successfully")

    except Exception as e:
        conn.rollback()
        print("Error inserting order_item:", e)