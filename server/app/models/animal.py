from app.config import db

class Animal(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    description = db.Column(db.Text)

    farmer_id = db.Column(db.Integer, db.ForeignKey("farmers.id"), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=True)

    farmer = db.relationship("Farmer", back_populates="animals")
    cart = db.relationship("Cart", back_populates="animals")
    order = db.relationship("Order", back_populates="animals")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "price": self.price,
            "image_url": self.image_url,
            "description": self.description,
            "farmer_id": self.farmer_id,
            "cart_id": self.cart_id,
            "order_id": self.order_id
        }
