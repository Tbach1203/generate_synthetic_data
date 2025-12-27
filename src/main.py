from config.config import load_config, connect
from schema.brand import brand, insert_brand
from schema.category import category, insert_category

if __name__ == '__main__':
    config = load_config()
    conn = connect(config)

    # brand
    # brand(conn)
    # insert_brand(conn)

    #category
    # category(conn)
    # insert_category(conn)
