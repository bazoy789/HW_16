from flask import Flask, json, request
import db_setup as db
from flask_sqlalchemy import SQLAlchemy
import row_data

db = SQLAlchemy()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String, unique=True)
    role = db.Column(db.String)
    phone = db.Column(db.String, unique=True, nullable=False)


    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
        }


class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))


    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'executor_id': self.executor_id,
        }

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String(255))
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'address': self.address,
            'price': self.price,
            'customer_id': self.customer_id,
            'executor_id': self.executor_id,
        }

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        result = []
        for user in User.query.all():
            result.append(user.to_dict())
        return json.dumps(result), 200

    if request.method == 'POST':
        user_date = json.loads(request.data)
        new_user = User(
            id = user_date['id'],
            first_name= user_date['first_name'],
            last_name = user_date['last_name'],
            age = user_date['age'],
            email = user_date['email'],
            role = user_date['role'],
            phone = user_date['phone'],
        )

        db.session.add(new_user)
        db.session.commit()

        return "User created", 201

@app.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def user(uid:int):

    if request.method == 'GET':
        return json.dumps(User.query.get(uid).to_dict()), 200

    if request.method == 'PUT':
        user_date = json.loads(request.data)
        u = User.query.get(uid)
        u.first_name= user_date['first_name'],
        u.last_name = user_date['last_name'],
        u.age = user_date['age'],
        u.email = user_date['email'],
        u.role = user_date['role'],
        u.phone = user_date['phone'],

        db.session.add(u)
        db.session.commit()

        return 'User updated', 204

    if request.method == 'DELETE':
        u = User.query.get(uid)
        db.session.delete(u)
        db.session.commit()
        return "User delete" ,204


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        result = []
        for order in Order.query.all():
            result.append(order.to_dict())
        return json.dumps(result), 200

    if request.method == 'POST':
        order_date = json.loads(request.data)
        new_order = Order(
            id=order_date['id'],
            name=order_date['name'],
            description=order_date['description'],
            start_date=order_date['start_date'],
            end_date=order_date['end_date'],
            address=order_date['address'],
            price=order_date['price'],
            customer_id=order_date['customer_id'],
            executor_id=order_date['executor_id'],
        )

        db.session.add(new_order)
        db.session.commit()

        return "Order created", 201

@app.route('/orders/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def order(uid:int):
    if request.method == 'GET':
        return json.dumps(Order.query.get(uid).to_dict()), 200

    if request.method == 'PUT':
        order_data = json.loads(request.data)
        u = Order.query.get(uid)
        u.name = order_data['name'],
        u.description = order_data['description'],
        u.start_date = order_data['start_date'],
        u.end_date = order_data['end_date'],
        u.address = order_data['address'],
        u.price = order_data['price'],
        u.customer_id = order_data['customer_id'],
        u.executor_id = order_data['executor_id'],

        db.session.add(u)
        db.session.commit()

        return 'Order updated', 204

    if request.method == 'DELETE':
        u = Order.query.get(uid)
        db.session.delete(u)
        db.session.commit()
        return "Order delete" ,204


@app.route('/offers', methods=['GET', 'POST'])
def offers():
    if request.method == 'GET':
        result = []
        for offer in Offer.query.all():
            result.append(offer.to_dict())
        return json.dumps(result), 200

    if request.method == 'POST':
        offer_date = json.loads(request.data)
        new_offer = Offer(
            id=offer_date['id'],
            order_id=offer_date['order_id'],
            executor_id=offer_date['executor_id'],
        )

        db.session.add(new_offer)
        db.session.commit()

        return "Offer created", 201

@app.route('/offers/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def offer(uid:int):
    if request.method == 'GET':
        return json.dumps(Offer.query.get(uid).to_dict()), 200

    if request.method == 'PUT':
        offer_data = json.loads(request.data)
        u = Offer.query.get(uid)
        u.order_id = offer_data['order_id'],
        u.executor_id = offer_data['executor_id'],

        db.session.add(u)
        db.session.commit()

        return 'Offer updated', 204

    if request.method == 'DELETE':
        u = Offer.query.get(uid)
        db.session.delete(u)
        db.session.commit()
        return "Offer delete" ,204

def users():
    if request.method == 'GET':
        result = []
        for user in User.query.all():
            result.append(user.to_dict())
        return json.dumps(result), 200



def init_data():
    db.drop_all()
    db.create_all()

    for user in row_data.users:
        new_user = User(
            id = user['id'],
            first_name= user['first_name'],
            last_name = user['last_name'],
            age = user['age'],
            email = user['email'],
            role = user['role'],
            phone = user['phone'],
        )

        db.session.add(new_user)
        db.session.commit()

    for order in row_data.orders:
        new_order = Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=order['start_date'],
            end_date=order['end_date'],
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id'],
        )

        db.session.add(new_order)
        db.session.commit()


    for offer in row_data.offers:
        new_offer = Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id'],
        )

        db.session.add(new_offer)
        db.session.commit()


if __name__ == "__main__":
    init_data()
    app.run(debug=True)

