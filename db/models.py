from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Brand(Base):
    __tablename__ = 'Brands'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    logoPath = Column(String)

    products = relationship("Product", back_populates="brand", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"<Brand {self.name}>"

    def update(self, key, value):
        self.__setattr__(key, value)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'logoPath': self.logoPath
        }


class Product(Base):
    __tablename__ = 'Products'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    brandID = Column(Integer, ForeignKey('Brands.id'))
    price = Column(Float, nullable=False)
    rating = Column(Float)
    ratingCount = Column(Integer)
    imagePath = Column(String)
    trending = Column(Boolean)
    category = Column(String)

    brand = relationship("Brand", back_populates="products")
    

    def __repr__(self):
        return f"<Product {self.name}>"

    def update(self, key, value):
        self.__setattr__(key, value)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'brandID': self.brandID,
            'price': self.price,
            'imagePath': self.imagePath,
            'trending': self.trending,
            'brand': self.brand.to_dict(),
            'category': self.category
        }


class Order(Base):
    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    addressLine1 = Column(String)
    addressLine2 = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(String)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f'<Order for {self.firstName} {self.lastName}>'

    def update(self, key, value):
        self.__setattr__(key, value)

    def to_dict(self):
        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'addressLine1': self.addressLine1,
            'addressLine2': self.addressLine2,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'items': self.items.to_dict()
        }


class OrderItem(Base):
    __tablename__ = 'OrderItems'

    id = Column(Integer, primary_key=True, nullable=False)
    orderID = Column(Integer, ForeignKey('Orders.id'))
    productID = Column(Integer, ForeignKey('Products.id'))

    product = relationship("Product")
    order = relationship("Order", back_populates="items")

    def __repr__(self):
        return f'<OrderItem {product.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'productID': self.productID,
            'product': self.product.to_dict()
        }


class Outfit(Base):
    __tablename__ = 'Outfits'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)

    items = relationship("OutfitItem", back_populates="outfit", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f'<Outfit {self.id}:{self.name}>'

    def update(self, key, value):
        self.__setattr__(key, value)

    def to_dict(self):
        return {
            'id': self.id,
            'name':self.name,
            'items':[x.to_dict() for x in self.items]
        }


class OutfitItem(Base):
    __tablename__ = 'OutfitItems'

    id = Column(Integer, primary_key=True)
    outfitID = Column(Integer, ForeignKey('Outfits.id'))
    productID = Column(Integer, ForeignKey('Products.id'))

    outfit = relationship("Outfit", back_populates="items")
    product = relationship("Product")

    def __repr__(self):
        return f'<OutfitItem {self.product.name}>'

    def to_dict(self):
        return {
            'id':self.id,
            'productID': self.productID,
            'product': self.product.to_dict()
        }


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)