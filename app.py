import json
from flask import Flask, request, jsonify
from models import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mybase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)

@app.route("/users", methods=['GET'])
def get_all_users():
	users = User.query.all()
	result = []
	for user in users:
		result.append(user.to_dict())
	return jsonify(result)

@app.route("/users/<int:user_id>", methods=['GET'])
def get_one_user(user_id):
	user = User.query.get(user_id)
	if user is None:
		return "Не найден пользователь"
	return jsonify(user.to_dict())


@app.route("/orders", methods=['GET'])
def get_all_orders():
	result = []
	orders = Order.query.all()
	for order in orders:
		result.append(order.to_dict())
	return jsonify(result)


@app.route("/orders/<int:order_id>", methods=['GET'])
def get_one_order(order_id):
	order = Order.query.get(order_id)
	if order is None:
		return "Не найден заказ"
	return jsonify(order.to_dict())


@app.route("/offers", methods=['GET'])
def get_all_offers():
	result = []
	offers = Offer.query.all()
	for offer in offers:
		result.append(offer.to_dict())
	return jsonify(result)


@app.route("/offers/<int:offer_id>", methods=['GET'])
def get_one_offer(offer_id):
	offer = Offer.query.get(offer_id)
	if offer is None:
		return "Не найден заказ"
	return jsonify(offer.to_dict())


@app.route("/users", methods=['POST'])
def create_user():
	user = json.loads(request.data)
	new_user_obj = User(
		id=user['id'],
		first_name=user['first_name'],
		last_name=user['last_name'],
		age=user['age'],
		email=user['email'],
		role=user['role'],
		phone=user['phone']
	)
	db.session.add(new_user_obj)
	db.session.commit()
	db.session.close()
	return "Пользователь создан в базе данных", 200


@app.route("/orders", methods=['POST'])
def create_order():
	order = json.loads(request.data)
	new_order = Order(
		id=order['id'],
		name=order['name'],
		description=order['description'],
		start_date=datetime.strptime(order['start_date'], '%m/%d/%Y'),
		end_date=datetime.strptime(order['end_date'], '%m/%d/%Y'),
		address=order['address'],
		price=order['price'],
		customer_id=order['customer_id'],
		executor_id=order['executor_id']
	)

	db.session.add(new_order)
	db.session.commit()
	db.session.close()
	return f" Заказ создан"


@app.route("/offers", methods=['POST'])
def create_offer():
	offer = json.loads(request.data)
	new_offer = Offer(
		id=offer['id'],
		order_id=offer['order_id'],
		executor_id=offer['executor_id']
	)

	db.session.add(new_offer)
	db.session.commit()
	db.session.close()
	return f" Предложение создано"



@app.route("/users/<int:user_id>", methods=['PUT'])
def update_user(user_id):
	user_data = json.loads(request.data)
	user = db.session.query(User).get(user_id)
	if user is None:
		return "Пользователь не найден", 404
	user.first_name = user_data['first_name']
	user.last_name = user_data['last_name']
	user.age = user_data['age']
	user.email = user_data['email']
	user.role = user_data['role']
	user.phone = user_data['phone']
	db.session.add(user)
	db.session.commit()
	db.session.close()
	return f"Пользователь с id {user_id} успешно изменен"

@app.route("/users/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
		user = db.session.query(User).get(user_id)
		db.session.delete(user)
		db.session.commit()
		db.session.close()
		return f"Пользователь с id {user_id} удален"


@app.route("/orders/<int:order_id>", methods=['PUT'])
def update_order(order_id):
		update_order = json.loads(request.data)
		order = db.session.query(Order).get(order_id)
		if order is None:
			return "Пользователь не найден", 404
		order.name = update_order['name'],
		order.description = update_order['description'],
		order.start_date = update_order(['start_date'], '%m/%d/%Y'),
		order.end_date = update_order(['end_date'],'%m/%d/%Y'),
		order.address = update_order['address'],
		order.customer_id = update_order['customer_id']
		order.executor_id = update_order['executor_id']
		db.session.add(order)
		db.session.commit()
		return f"Заказ с id {order_id} успешно изменен"

@app.route("/orders/<int:order_id>", methods=['DELETE'])
def delete_order(order_id):
		order = db.session.query(Order).get(order_id)
		db.session.delete(order)
		db.session.commit()
		return f"Заказ с id {order_id} удален"


@app.route("/offers/<int:offer_id>", methods=['PUT'])
def update_offer(offer_id):
		update_offer = json.loads(request.data)
		offer = db.session.query(Offer).get(offer_id)
		if offer is None:
			return "Пользователь не найден", 404
		offer.order_id = update_offer['order_id']
		offer.executor_id = update_offer['executor_id']
		db.session.add(offer)
		db.session.commit()
		return f"Заказ с id {offer_id} успешно изменен"

@app.route("/offers/<int:offer_id>", methods=['DELETE'])
def delete_offer(offer_id):
		offer = db.session.query(Offer).get(offer_id)
		db.session.delete(offer)
		db.session.commit()
		return f"Заказ с id {offer_id} удален"


if __name__ == "__main__":
	app.run(debug=True)
