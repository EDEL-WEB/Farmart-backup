from app.config import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    _password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    carts = db.relationship('Cart', back_populates='user', lazy=True)
    orders = db.relationship("Order", back_populates="user", cascade="all, delete")
    payments = db.relationship("Payment", back_populates="user", cascade="all, delete")

    def __init__(self, username, email, is_admin=False):
        self.username = username
        self.email = email
        self.is_admin = is_admin

    @hybrid_property
    def password(self):
        return "Password hashes may not be viewed directly"

    @password.setter
    def password(self, plain_password):
        password_hash = bcrypt.generate_password_hash(plain_password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def check_password(self, plain_password):
        return bcrypt.check_password_hash(self._password_hash, plain_password.encode('utf-8'))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
