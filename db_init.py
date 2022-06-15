from models import *
import data
from datetime import datetime

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
