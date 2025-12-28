from config.config import load_config, connect
from schema.brand import brand, insert_brand
from schema.category import category, insert_category
from schema.seller import seller, insert_seller
from schema.product import product, insert_product

if __name__ == '__main__':
    config = load_config()
    conn = connect(config)

    # brand
    # brand(conn)
    # insert_brand(conn)

    #category
    # category(conn)
    # insert_category(conn)

    #seller
    # seller(conn)
    # insert_seller(conn)

    #product
    # product(conn)
    # insert_product(conn)
