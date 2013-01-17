import os
import pymongo
import operator

from bson.objectid import ObjectId
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/db')
def testdb():
	connection = pymongo.Connection()
	db = connection["my_db"]
	collection = db["recipe_list"]

	collection.insert({
		'recipe': 'Shahi Kesuri Tikka',
		'type': 'main',
		'Ingredients': ['ginger', 'garlic', 'salt', 'garam masala', 'chilli powder', 'tumeric powder', 'chicken breast'],
	})
	
	collection.insert({
		'recipe': 'Raita',
		'type': 'accompanyment',
		'Ingredients': ['salt','garam masala','chilli powder','cucumber'],
	})
	
	collection.insert({
		'recipe': 'Ceasor salad',
		'type': 'appetizer',
		'Ingredients': ['lettuce','lemon','crutons','bacon'],
	})
	
	while True:
		str1 = raw_input("What to do? (type one of the following: search,insert,exit): ")
		if str1 == "search":
			str2 = raw_input("enter ingredients separated by commas: ")
			input_list = str2.split(',')
			ing = {}
			for i in input_list:
				finder = collection.find({"Ingredients": i})
				if finder.count() > 0:
					recipe = finder.distinct("recipe")
					for j in recipe:
						if j not in ing:
							ing[str(j)] = 0
							temp = 1/float(len(collection.find({"recipe":j}).distinct("Ingredients")))
							ing[str(j)] += temp
				else:
					print 'cannot find: ' + i + " in MongoDB"
			print ing
			best = max(ing.iteritems(), key=operator.itemgetter(1))[0]
			print best + " is your best option."
		elif str1 == "insert":
			print "function not created"
		elif str1 == "exit":
			collection.remove({})
			return "Thank you for using!"
		else:
			print "not a valid choice"

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

