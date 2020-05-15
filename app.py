from flask import Flask, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import ValidationError
import os

# variables and application instance
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# database
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    # helper to add category function to foodItems and foodItems function to category, to make lookup easier
    foodItems = db.relationship('FoodItem', backref = 'category') 

    def to_json(self):
        json_category = {
            'url': url_for('category', id = self.id),
            'name': self.name,
            # how to get food items? +++ TODO
            }
        return json_category

    @staticmethod
    def from_json(json_post):
        name = json_post('name')
        if name is None or name == '':
            raise ValidationError('Item does not have a name')
        return Category(name=name)

class FoodItem(db.Model):
    __tablename__ = 'foodItems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    isVegan = db.Column(db.Boolean)
    caveats = db.Column(db.Text)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'))
    isApprovedItem = db.Column(db.Boolean)
    isApprovedData = db.Column(db.Boolean)

    def to_json(self):
        json_fooditem = {
            'url': url_for('foodItem', id = self.id),
            'name': self.name,
            'isVegan': self.isVegan,
            'caveats': self.caveats,
            'categoryId': self.categoryId, # how to get category name? +++ TODO
            'isApprovedItem': self.isApprovedItem,
            'isApprovedData': self.isApprovedData
        }
        return json_fooditem

    @staticmethod
    def from_json(json_post):
        name = json_post('name')
        isVegan = json_post('isVegan')
        caveats = json_post('caveats')
        categoryId = json_post('categoryId') # how to get category name? +++ TODO
        isApprovedItem = json_post('isApprovedItem')
        isApprovedData = json_post('isApprovedData')
        if name is None or name == '':
            raise ValidationError('Item does not have a name')
        return FoodItem(name=name, isVegan=isVegan, caveats=caveats, categoryId=categoryId, isApprovedItem=isApprovedItem, isApprovedData=isApprovedData)

#db.create_all() 


# routes
@app.route('/')
def index():
    return "<h1>Is Vegan API</h1><p>Endpoints:<ul><li>category</li><li>foodItem</li><li>isVegan</li></ul></p>"

## CATEGORIES ##
#create
@app.route('/category/', methods = ['POST'])
def new_category():
    category = Category.from_json(request.json)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_json())

#read
@app.route('/category/', methods = ['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify({ 'categories': [category.to_json() for category in categories] })

#read
@app.route('/category/<int:id>', methods = ['GET'])
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify(category.to_json())

###+++ TODO
#update
@app.route('/category/<int:id>', methods = ['PUT'])
def update_category(id):
    #category = Category.query.get_or_404(id)
    return jsonify(category.to_json())

###+++ TODO
#delete
@app.route('/category/<int:id>', methods = ['DELETE'])
def remove_category(id):
    #category = Category.query.get_or_404(id)
    return jsonify(category.to_json())


## FOOD ITEMS ##
#create
@app.route('/foodItem/', methods = ['POST'])
def new_foodItem():
    foodItem = FoodItem.from_json(request.json)
    db.session.add(foodItem)
    db.session.commit()
    return jsonify(foodItem.to_json())

#read
@app.route('/foodItem/', methods = ['GET'])
def get_foodItems():
    foodItems = FoodItem.query.all()
    return jsonify({ 'foodItems': [foodItem.to_json() for foodItem in foodItems] })

#read
@app.route('/foodItem/<int:id>', methods = ['GET'])
def get_foodItem(id):
    foodItem = FoodItem.query.get_or_404(id)
    return jsonify(foodItem.to_json())

###+++ TODO
#update
@app.route('/foodItem/<int:id>', methods = ['PUT'])
def update_foodItem(id):
    #foodItem = FoodItem.query.get_or_404(id)
    return jsonify(foodItem.to_json())

###+++ TODO
#delete
@app.route('/foodItem/<int:id>', methods = ['DELETE'])
def remove_foodItem(id):
    #foodItem = FoodItem.query.get_or_404(id)
    return jsonify(foodItem.to_json())

## IS VEGAN ##
# read
@app.route('/isVegan/<int:id>', methods = ['GET'])
def isVegan(id):
    foodItem = FoodItem.query.get_or_404(id)
    return jsonify({ 'isVegan':foodItem.isVegan, 'caveats':foodItem.caveats })

# run app
if __name__ == '__main__':
    app.run(debug=True)