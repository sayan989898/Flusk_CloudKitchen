from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Users Table
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    user_type = db.Column(db.Enum('admin', 'customer', 'delivery'), default='customer')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    orders = db.relationship('Order', backref='user', lazy=True)

# Menu Categories
class MenuCategory(db.Model):
    __tablename__ = 'menu_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

    dishes = db.relationship('Dish', backref='category', lazy=True)

# Dishes
class Dish(db.Model):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('menu_categories.id'))
    is_special = db.Column(db.Boolean, default=False)
    availability = db.Column(db.Enum('available', 'not_available'), default='available')

# Specials
class Special(db.Model):
    __tablename__ = 'specials'

    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id', ondelete='CASCADE'))
    special_date = db.Column(db.Date)

# Orders
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_type = db.Column(db.Enum('delivery', 'takeaway'), default='delivery')
    delivery_address = db.Column(db.Text)
    status = db.Column(db.Enum('pending', 'accepted', 'preparing', 'out_for_delivery', 'delivered', 'cancelled'), default='pending')
    total_price = db.Column(db.Numeric(10, 2))
    order_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    delivery_partner_id = db.Column(db.Integer, db.ForeignKey('users.id'), default=None)

# Order Items
class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))

# Payments
class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    payment_method = db.Column(db.Enum('credit_card', 'paypal', 'upi', 'cod'), nullable=False)
    payment_status = db.Column(db.Enum('paid', 'pending', 'failed'), default='pending')
    payment_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

# Chefs
class Chef(db.Model):
    __tablename__ = 'chefs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    popularity = db.Column(db.Integer, default=0)

# Chef Dishes
class ChefDish(db.Model):
    __tablename__ = 'chef_dishes'

    id = db.Column(db.Integer, primary_key=True)
    chef_id = db.Column(db.Integer, db.ForeignKey('chefs.id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'))

# Takeaway Counters
class TakeawayCounter(db.Model):
    __tablename__ = 'takeaway_counters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.Text)
    contact_number = db.Column(db.String(20))

# Takeaway Orders
class TakeawayOrder(db.Model):
    __tablename__ = 'takeaway_orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    counter_id = db.Column(db.Integer, db.ForeignKey('takeaway_counters.id'))
    preferred_pickup_time = db.Column(db.DateTime)
    total_price = db.Column(db.Numeric(10, 2))
    status = db.Column(db.Enum('pending', 'accepted', 'ready_for_pickup', 'picked_up', 'cancelled'), default='pending')
    order_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

# Takeaway Items
class TakeawayItem(db.Model):
    __tablename__ = 'takeaway_items'

    id = db.Column(db.Integer, primary_key=True)
    takeaway_order_id = db.Column(db.Integer, db.ForeignKey('takeaway_orders.id', ondelete='CASCADE'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))

# Feedback
class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

# Offers
class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
