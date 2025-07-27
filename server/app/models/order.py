from app.config import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="orders")
    animals = db.relationship("Animal", back_populates="order")
    payment = db.relationship("Payment", back_populates="order", uselist=False, cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "total_amount": self.total_amount,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id,
            "animals": [animal.to_dict() for animal in self.animals],
            "payment": {"id": self.payment.id, "status": self.payment.status} if self.payment else None
        }
