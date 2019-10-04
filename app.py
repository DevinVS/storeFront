import db.db as db
import tornado.ioloop
import tornado.web
import json
import decimal, datetime
import hashlib
import os
import random
import string



class Main(tornado.web.RequestHandler):

    def get(self):
        self.render("templates/index.html")


class Products(tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self):
        products = db.get_products()
        self.write(json.dumps([x.to_dict() for x in products]))


class Product(tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self, id):
        product = db.get_product(id)
        self.write(json.dumps(product.to_dict()))

    def post(self, _):
        data = json.loads(self.request.body)
        
        db.new_product(
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
        data = json.loads(self.request.body)

        db.update_product(
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
        data = json.loads(self.request.body)
        db.update_product(id, **data)
        self.write(json.dumps({"message":"success"}))

    def delete(self, id):
        db.delete_product(id)
        self.write(json.dumps({"message":"success"}))


class Brands(tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self):
        brands = db.get_brands()
        self.write(json.dumps([x.to_dict() for x in brands]))


class Brand(tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self, id):
        brand = db.get_brand(id)
        self.write(json.dumps(brand.to_dict()))

    def post(self, _):
        data = json.loads(self.request.body)
        db.new_brand(
            name=data["name"]
        )
        self.write(json.dumps({"message":"success"}))

    def put(self, id):
        data = json.loads(self.request.body)
        db.update_brand(
            id,
            name=data["name"],
            logo_path=data["logoPath"]
        )
        self.write(json.dumps({"message":"success"}))

    def patch(self, id):
        data = json.loads(self.request.body)
        db.update_brand(id, **data)
        self.write(json.dumps({"message":"success"}))

    def delete(self, id):
        db.delete_brand(id)
        self.write(json.dumps({"message":"success"}))


class Outfits(tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self):
        outfits = db.get_outfits()
        self.write(json.dumps([x.to_dict() for x in outfits]))


class Outfit(tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self, id):
        outfit = db.get_outfit(id)
        self.write(outfit.to_dict())

    def post(self, _):
        data = json.loads(self.request.body)

        db.new_outfit(
            name=data["name"],
            product_ids=data["productIDs"]
        )
        self.write(json.dumps({"message":"success"}))

    def put(self, id):
        data = json.loads(self.request.body)
        db.update_outfit(
            id,
            name=data["name"],
            product_ids=data["productIDs"]
        )
        self.write(json.dumps({"message":"success"}))

    def patch(self, id):
        data = json.loads(self.request.body)
        db.update_outfit(id, **data)
        self.write(json.dumps({"message":"success"}))

    def delete(self, id):
        db.delete_outfit(id)
        self.write(json.dumps({"message":"success"}))


class Orders(tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self):
        orders = db.get_orders()
        self.write(json.dumps([x.to_dict() for x in orders]))


class Order(tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self, id):
        order = db.get_order(id)
        self.write(json.dumps(order.to_dict()))

    def post(self, _):
        data = json.loads(self.request.body)

        db.new_order(
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
        data = json.loads(self.request.body)
        db.update_order(
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
        data = json.loads(self.request.body)
        db.update_order(id, **data)

    def delete(self, id):
        db.delete_order(id)
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
            debug=True
        )
        super(Application, self).__init__(handlers, **settings)


if __name__ == "__main__":
    application = Application()
    application.listen(3000)
    tornado.ioloop.IOLoop.current().start()

    