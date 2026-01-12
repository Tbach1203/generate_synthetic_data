from config.config import load_config, connect
from schema.brand import brand, insert_brand
from schema.category import category, insert_category
from schema.seller import seller, insert_seller
from schema.product import product, insert_product
from schema.order import order, insert_order
from schema.order_item import order_item, insert_order_item
from schema.promotions import promotions, insert_promotions
from schema.promotion_products import promotion_products, insert_promotion_products

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

    #orders
    # order(conn)
    # insert_order(conn)

    #order_item
    order_item(conn)
    insert_order_item(conn)

    #promotions
    # promotions(conn)
    # insert_promotions(conn)

    #promotion_products
    # promotion_products(conn)
    # insert_promotion_products(conn)


