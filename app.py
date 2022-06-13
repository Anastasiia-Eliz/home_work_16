import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from main import User, Order, Offer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mybase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route("/users", methods=['GET'])
def get_all_users():
	users = User.query.all()
	result = []
	for user in users:
		result.append({
			"id": user.id,
			"first_name": user.first_name,
			"last_name": user.last_name,
			"age": user.age,
			"email": user.email,
			"role": user.role,
			"phone": user.phone,
		})
	return json.dumps(result)


@app.route("/users/<int:user_id>", methods=['GET'])
def get_one_user(user_id):
	user = User.query.get(user_id)
	return jsonify(user.to_dict())


@app.route("/orders")
def get_all_orders():
	result = []
	orders = Order.query.all()
	for order in orders:
		result.append(order)
		return jsonify(result)


@app.route("/orders/<int:order_id>")
def get_one_order(order_id):
	order = Order.query.get(order_id)
	return jsonify(order)


@app.route("/offers")
def get_all_offers():
	result = []
	offers = Offer.query.all()
	for offer in offers:
		result.append(offer)
		return jsonify(result)


@app.route("/offers/<int:offer_id>")
def get_one_offer(offer_id):
	offer = Offer.query.get(offer_id)
	return jsonify(offer)


@app.route("/users", methods=['POST'])
def create_user():
	user = json.loads(request.data)
	new_user = User(
		id=user['id'],
		first_name=user['first_name'],
		last_name=user['last_name'],
		age=user['age'],
		email=user['email'],
		role=user['role'],
		phone=user['phone'])
	db.session.add(new_user)
	db.session.commit()
	db.session.close()
	return f"Пользователь создан"


@app.route("/orders", methods=['POST'])
def create_order():
	order = json.loads(request.data)
	new_order = Order(
		id=order['id'],
		name=order['name'],
		description=order['description'],
		start_date=order['start_date'],
		end_date=order['end_date'],
		addres=order['address'],
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


@app.route("/users/<int:user_id>", methods=['PUT', 'DELETE'])
def update_user(user_id):
	if request.method == 'PUT':
		update_user = json.loads(request.data)
		user = User.query.get(user_id)
		user.first_name = update_user['first_name'],
		user.last_name = update_user['last_name'],
		user.age = update_user['age'],
		user.email = update_user['email'],
		user.role = update_user['role'],
		user.phone = update_user['phone']
		db.session.add(user)
		db.session.commit()
		return f"Пользователь с id {user_id} успешно изменен"
	elif request.method == "DELETE":
		user = User.query.get(user_id)
		db.session.delete(user)
		db.session.commit()
		return f"Пользователь с id {user_id} удален"


@app.route("/orders/<int:order_id>", methods=['PUT', 'DELETE'])
def update_order(order_id):
	if request.method == 'PUT':
		update_order = json.loads(request.data)
		order = Order.query.get(order_id)
		order.name = update_order['name'],
		order.description = update_order['description'],
		order.start_date = update_order['start_date'],
		order.end_date = update_order['end_date'],
		order.address = update_order['address'],
		order.customer_id = update_order['customer_id']
		order.executor_id = update_order['executor_id']
		db.session.add(order)
		db.session.commit()
		return f"Заказ с id {order_id} успешно изменен"
	elif request.method == "DELETE":
		order = Order.query.get(order_id)
		db.session.delete(order)
		db.session.commit()
		return f"Заказ с id {order_id} удален"


@app.route("/offers/<int:offer_id>", methods=['PUT', 'DELETE'])
def update_offer(offer_id):
	if request.method == 'PUT':
		update_offer = json.loads(request.data)
		offer = Offer.query.get(offer_id)
		offer.order_id = update_offer['order_id']
		offer.executor_id = update_offer['executor_id']
		db.session.add(offer)
		db.session.commit()
		return f"Заказ с id {offer_id} успешно изменен"
	elif request.method == "DELETE":
		offer = Offer.query.get(offer_id)
		db.session.delete(offer)
		db.session.commit()
		return f"Заказ с id {offer_id} удален"


if __name__ == "__main__":
	app.run(debug=True)
