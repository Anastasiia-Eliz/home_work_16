from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import data
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mybase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	age = db.Column(db.Integer)
	email = db.Column(db.String(100))
	role = db.Column(db.String(100))
	phone = db.Column(db.String(100))

	def to_dict(self):
		return {
			"id": self.id,
			"first_name": self.first_name,
			"last_name": self.last_name,
			"age": self.age,
			"email": self.email,
			"role": self.role,
			"phone": self.phone,
		}

class Offer(db.Model):
	__tablename__ = "offer"
	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
	executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
	order = relationship("Order", foreign_keys=[order_id])
	executor = relationship("User", foreign_keys=[executor_id])


class Order(db.Model):
	__tablename__ = "order"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	description = db.Column(db.String)
	start_date = db.Column(db.Date)
	end_date = db.Column(db.Date)
	address = db.Column(db.String(100))
	price = db.Column(db.Integer)
	customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
	executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
	customer = relationship("User", foreign_keys=[customer_id])
	executor = relationship("User", foreign_keys=[executor_id])


db.create_all()

for user in data.USERS:
	db.session.add(User(
		id=user['id'],
		first_name=user['first_name'],
		last_name=user['last_name'],
		age=user['age'],
		email=user['email'],
		role=user['role'],
		phone=user['phone'])
	)
	db.session.commit()

for order in data.ORDER:
	db.session.add(Order(
		id=order['id'],
		name=order['name'],
		description=order['description'],
		start_date=datetime.strptime(order['start_date'], '%m/%d/%Y'),
		end_date=datetime.strptime(order['end_date'], '%m/%d/%Y'),
		address=order['address'],
		price=order['price'],
		customer_id=order['customer_id'],
		executor_id=order['executor_id']
	))
	db.session.commit()

for offer in data.OFFER:
	db.session.add(Offer(
		id=offer['id'],
		order_id=offer['order_id'],
		executor_id=offer['executor_id']
	))

	db.session.commit()

db.session.close()



