
from flask import Flask, request
from random import randint
import redis


redis = redis.Redis(host="localhost", port=6379, db=0)
app = Flask("teste")

def getProduct(product):
	if product == "1":
		return "{\"productId\" : 1, \"productName\":, \"bolsa de coco\"}"
	else:
		return "{\"productId\" : 2, \"productName\":, \"bolsonaro\"}"



@app.route('/cart/<user_id>',methods=['POST'])
def createCart(user_id):
	if redis.set('cart:'+user_id, 1) == 1:
		return '{\"returnCode\": 1}'
	else:
		return '{\"returnCode\": 0}'

@app.route('/cart/<user_id>/products',methods=['POST'])
def addProduct(user_id):
	flagCart = redis.get('cart:'+user_id)
	if flagCart != None and int(flagCart) == 1:
		produto = getProduct(request.form.get("produto"))
		redis.lpush('cart:'+user_id+':products', produto)
		return '{\"returnCode\": 1}'
	else:
		return '{\"returnCode\": 0}'

@app.route('/cart/<user_id>',methods=['GET'])
def getCart(user_id):
	flagCart = redis.get('cart:'+user_id)
	if flagCart != None and int(flagCart) == 1:
		productsCart = redis.lrange('cart:'+user_id+':products', 0, -1 )
		ret = "{\"products\":["
		for product in productsCart:
			ret += str(product.decode('utf-8'))
		ret += "]}"
		return ret
	else:
		return '{\"returnCode\": 0}'

@app.route('/cart/<user_id>/products/<product_id>',methods=['DELETE'])
def deleteProduct(user_id,product_id):
	flagCart = redis.get('cart:'+user_id)
	if flagCart != None and int(flagCart) == 1:
		redis.lrem('cart:'+user_id+':products', 1, getProduct(product_id))

		return '{\"returnCode\": 1}'
	else:
		return '{\"returnCode\": 0}'


@app.route('/cart/<user_id>',methods=['DELETE'])
def deleteCart(user_id):
	flagCart = redis.get('cart:'+user_id)
	if flagCart != None and int(flagCart) == 1:
		redis.delete('cart:'+user_id)

		return '{\"returnCode\": 1}'
	else:
		return '{\"returnCode\": 0}'

app.run()

