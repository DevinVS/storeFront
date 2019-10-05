import db.db as db
import tornado.ioloop
import tornado.web
import json
import decimal, datetime
import hashlib
import os
import random
import string
from tornado_sqlalchemy import as_future, make_session_factory, SessionMixin


class Main(tornado.web.RequestHandler):

    def get(self):
        self.render("templates/index.html")


class Products(SessionMixin, tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self):
        with self.make_session() as session:
            products = db.get_products(session)
            self.write(json.dumps([x.to_dict() for x in products]))


class Product(SessionMixin, tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self, id):
        with self.make_session() as session:
            product = db.get_product(session, id)
            self.write(json.dumps(product.to_dict()))

    def post(self, _):
        with self.make_session() as session:
            data = json.loads(self.request.body)
        
            db.new_product(
                session,
                name=data["name"],
                brandID=data["brandID"],
                price=data["price"],
                description=data["description"],
                image_path=data["imagePath"],
                trending=data["trending"],
                category=data["category"]
            )
            self.write(json.dumps({"message":"success"}))

    def put(self, id):
        with self.make_session() as session:
            data = json.loads(self.request.body)

            db.update_product(
                session,
                id, 
                name=data["name"],
                brandID=data["brandID"],
                price=data["price"],
                description=data["description"],
                image_path=data["imagePath"],
                trending=data["trending"],
                category=data["category"]
            )
            self.write(json.dumps({"message":"success"}))

    def patch(self, id):
        with self.make_session() as session:
            data = json.loads(self.request.body)
            db.update_product(session, id, **data)
            self.write(json.dumps({"message":"success"}))

    def delete(self, id):
        with self.make_session() as session:
            db.delete_product(session, id)
            self.write(json.dumps({"message":"success"}))


class Brands(SessionMixin, tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self):
        with self.make_session() as session:
            brands = db.get_brands(session)
            self.write(json.dumps([x.to_dict() for x in brands]))


class Brand(SessionMixin, tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self, id):
        with self.make_session() as session:
            brand = db.get_brand(session, id)
            self.write(json.dumps(brand.to_dict()))

    def post(self, _):
        with self.make_session() as session:
            data = json.loads(self.request.body)
            db.new_brand(
                session,
                name=data["name"]
            )
            self.write(json.dumps({"message":"success"}))

    def put(self, id):
        with self.make_session() as session:
            data = json.loads(self.request.body)
            db.update_brand(
                session,
                id,
                name=data["name"],
                logo_path=data["logoPath"]
            )
            self.write(json.dumps({"message":"success"}))

    def patch(self, id):
        with self.make_session() as session:
            data = json.loads(self.request.body)
            db.update_brand(session, id, **data)
            self.write(json.dumps({"message":"success"}))

    def delete(self, id):
        with self.make_session() as session:
            db.delete_brand(session, id)
            self.write(json.dumps({"message":"success"}))


class Outfits(SessionMixin, tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self):
        with self.make_session() as session:
            outfits = db.get_outfits(session)
            self.write(json.dumps([x.to_dict() for x in outfits]))


class Outfit(SessionMixin, tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self, id):
        with self.make_session() as session:
            outfit = db.get_outfit(session, id)
            self.write(outfit.to_dict())

    def post(self, _):
        with self.make_session() as session:
            data = json.loads(self.request.body)

            db.new_outfit(
                session,
                name=data["name"],
                product_ids=data["productIDs"]
            )
            self.write(json.dumps({"message":"success"}))

    def put(self, id):
        with self.make_session() as session:
            data = json.loads(self.request.body)
            db.update_outfit(
                session,
                id,
                name=data["name"],
                product_ids=data["productIDs"]
            )
            self.write(json.dumps({"message":"success"}))

    def patch(self, id):
        with self.make_session() as session:
            data = json.loads(self.request.body)
            db.update_outfit(session, id, **data)
            self.write(json.dumps({"message":"success"}))

    def delete(self, id):
        with self.make_session() as session:
            db.delete_outfit(session, id)
            self.write(json.dumps({"message":"success"}))


class Orders(SessionMixin, tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self):
        with self.make_session() as session:
            orders = db.get_orders(session)
            self.write(json.dumps([x.to_dict() for x in orders]))


class Order(SessionMixin, tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self, id):
        with self.make_session() as session:
            order = db.get_order(session, id)
            self.write(json.dumps(order.to_dict()))

    def post(self, _):
        with self.make_session() as session:
            data = json.loads(self.request.body)

            db.new_order(
                session,
                first_name=data["firstName"],
                last_name=data["lastName"],
                address_line_1=data["addressLine1"],
                address_line_2=data["addressLine2"],
                city=data["city"],
                state=data["state"], 
                zipcode=data["zipcode"],
                product_ids=data["productIDs"]
            )
            self.write(json.dumps({"message":"success"}))

    def put(self, id):
        with self.make_session() as session:
            data = json.loads(self.request.body)
            db.update_order(
                session,
                id,
                first_name=data["firstName"],
                last_name=data["lastName"],
                address_line_1=data["addressLine1"],
                address_line_2=data["addressLine2"],
                city=data["city"],
                state=data["state"], 
                zipcode=data["zipcode"],
                product_ids=data["productIDs"]
            )
            self.write(json.dumps({"message":"success"}))

    def patch(self, id):
        with self.make_session() as session:
            data = json.loads(self.request.body)
            db.update_order(session, id, **data)

    def delete(self, id):
        with self.make_session() as session:
            db.delete_order(session, id)
            self.write(json.dumps({"message":"success"}))


class ImageHandler(tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def post(self):
        file1 = self.request.files['file'][0]
        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        final_filename= fname+extension
        output_file = open("static/images/products/" + final_filename, 'wb')
        output_file.write(file1['body'])
        self.write(json.dumps({"message":"success", "filePath":final_filename}))

class AdminHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("templates/admin.html")


class AdminBrands(tornado.web.RequestHandler):

    def get(self):
        self.render("templates/admin_brands.html")


class AdminProducts(tornado.web.RequestHandler):

    def get(self):
        self.render("templates/admin_products.html")

    
class AdminOutfits(tornado.web.RequestHandler):
    
    def get(self):
        self.render("templates/admin_outfits.html")


class AdminOrders(tornado.web.RequestHandler):
    
    def get(self):
        self.render("templates/admin_orders.html")


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', Main),
            (r'/api/products', Products),
            (r'/api/product/([^/]+)?', Product),
            (r'/api/brands', Brands),
            (r'/api/brand/([^/]+)?', Brand),
            (r'/api/outfits', Outfits),
            (r'/api/outfit/([^/]+)?', Outfit),
            (r'/api/orders', Orders),
            (r'/api/order/([^/]+)?', Order),
            (r'/api/images', ImageHandler),
            (r'/admin', AdminHandler),
            (r'/admin/brands', AdminBrands),
            (r'/admin/products', AdminProducts),
            (r'/admin/outfits', AdminOutfits),
            (r'/admin/orders', AdminOrders)
        ]
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            session_factory=make_session_factory('mysql+mysqldb://store:store@localhost/store')
        )
        super(Application, self).__init__(handlers, **settings)


if __name__ == "__main__":
    application = Application()
    application.listen(3000)
    tornado.ioloop.IOLoop.current().start()

    