import os
import pymongo
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
		
	str1 = raw_input("enter ingredients separated by commas: ")
	input_list = str1.split(',')

	ing = {}
	count = 0
	
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
			print 'cannot find ing: ' + i
	print ing

	collection.remove({})
	
	return str1

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

