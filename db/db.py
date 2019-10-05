import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from db.models import Brand, Product, Order, OrderItem, Outfit, OutfitItem, User


# engine = sql.create_engine('mysql+mysqldb://store:store@localhost/store')
# Session = sessionmaker(bind=engine)
# session = Session()


def get_products(session):
    return session.query(Product).all()


def get_products_by_category(session, category):
    return session.query(Product).filter_by(category=category).all()


def get_product(session, id):
    return session.query(Product).filter_by(id=id).first()


def get_trending(session):
    return session.query(Product).filter_by(trending=True).all()


def get_brands(session):
    return session.query(Brand).all()


def get_brand(session, id):
    return session.query(Brand).filter_by(id=id).first()


def get_outfits(session):
    return session.query(Outfit).all()


def get_outfit(session, id):
    return session.query(Outfit).filter_by(id=id).first()


def get_orders(session):
    return session.query(Order).all()


def get_order(session, id):
    return session.query(Order).filter_by(id=id).first()


def get_users(session):
    return session.query(User).all()


def get_user(session, id):
    return session.query(User).filter_by(id=id).first()


def get_user_by_name(session, name):
    return session.query(User).filter_by(name=name).first()


def new_product(session, name, brandID, price, description=None, image_path=None, trending=False, category=""):
    product = Product(name=name, brandID=brandID, price=price, description=description, imagePath=image_path, trending=trending, category=category)

    session.add(product)
    session.commit()


def new_brand(session, name, logo_path=None):
    brand = Brand(name=name, logoPath=logo_path)

    session.add(brand)
    session.commit()


def new_outfit(session, name, product_ids):
    outfit = Outfit(name=name)
    outfit.items = [OutfitItem(outfitID=outfit.id, productID=x) for x in product_ids]

    session.add(outfit)
    session.commit()


def new_order(session, first_name, last_name, address_line_1, address_line_2, city, state, zipcode, product_ids):
    order = Order(firstName=first_name, lastName=last_name, addressLine1=address_line_1, addressLine2=address_line_2, city=city, state=state, zipcode=zipcode)
    order.items = [OrderItem(orderID=order.id, productID=x) for x in product_ids]

    session.add(order)
    session.commit()


def new_user(session, username, password):
    user = User(username=username, password=password)

    session.add(user)
    session.commit()


def update_product(session, id, **kwargs):
    product = get_product(session, id)

    for key, value in kwargs.items():
        product.update(key, value)

    session.commit()


def update_brand(session, id, **kwargs):
    brand = get_brand(id)

    for key, value in kwargs.items():
        brand.update(key, value)

    session.commit()


def update_outfit(session, id, **kwargs):
    outfit = get_outfit(session, id)

    for key, value in kwargs.items():
        outfit.update(key, value)

    session.commit()


def update_order(session, id, **kwargs):
    order = get_order(session, id)

    for key, value in kwargs.items():
        order.update(key, value)

    session.commit()


def delete_product(session, id):
    product = get_product(session, id)

    session.delete(product)
    session.commit()


def delete_brand(session, id):
    brand = get_brand(session, id)

    session.delete(brand)
    session.commit()

def delete_outfit(session, id):
    outfit = get_outfit(session, id)

    session.delete(outfit)
    session.commit()


def delete_order(session, id):
    order = get_order(session, id)

    session.delete(order)
    session.commit()