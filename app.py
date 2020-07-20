from flask import Flask, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import ValidationError
from flask_cors import CORS, cross_origin
import os

# variables and application instance
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
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
            'url': url_for('get_category', id = self.id),
            'name': self.name,
            # how to get food items? +++ TODO
            }
        return json_category

    @staticmethod
    def from_json(json_post):
        name = json_post['name']
        if name is None or name == '':
            raise ValidationError('Category does not have a name')
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
            'url': url_for('get_foodItem', id = self.id),
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
        name = json_post['name']
        isVegan = json_post['isVegan']
        caveats = json_post['caveats']
        categoryId = json_post['categoryId'] # how to get category name? +++ TODO
        isApprovedItem = json_post['isApprovedItem']
        isApprovedData = json_post['isApprovedData']
        if name is None or name == '':
            raise ValidationError('Item does not have a name')
        return FoodItem(name=name, isVegan=isVegan, caveats=caveats, categoryId=categoryId, isApprovedItem=isApprovedItem, isApprovedData=isApprovedData)

#db.create_all() 


# routes
@app.route('/')
def index():
    return "<h1>Is Vegan API</h1><p>Endpoints:<ul><li>category</li><li>foodItem</li><li>isVegan</li><li>isVeganById</li></ul></p>"

## CATEGORIES ##
#create
@app.route('/category/', methods = ['POST'])
def new_category():
    content = request.json
    name = content["name"]
    category_test = Category.query.filter_by(name=name).first()
    if category_test:
       return jsonify(message="The category already exists"), 409
    else:
        category = Category.from_json(content)
        db.session.add(category)
        db.session.commit()
        return jsonify(category.to_json()), 200

#read
@app.route('/category/', methods = ['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify({ 'categories': [category.to_json() for category in categories] }), 200

#read
@app.route('/category/<int:id>', methods = ['GET'])
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify(category.to_json()), 200

#update
@app.route('/category/<int:id>', methods = ['PUT'])
def update_category(id):
    category = Category.query.filter_by(id=id).first()
    if category:
        content = request.json
        category.name = content["name"]
        db.session.commit()
        return jsonify(message="The category was updated"), 202
    else:
        return jsonify(message="The category does not exist"), 404

#delete
@app.route('/category/<int:id>', methods = ['DELETE'])
def remove_category(id:int):
    category = Category.query.filter_by(id=id).first()
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify(message="You deleted the category"), 202
    else:
        return jsonify(message="The category doesn't exist"), 404

## FOOD ITEMS ##
#create
@app.route('/foodItem/', methods = ['POST'])
def new_foodItem():
    content = request.json
    name = content["name"]
    food_test = FoodItem.query.filter_by(name=name).first()
    if food_test:
       return jsonify(message="The food already exists"), 409
    else:
        foodItem = FoodItem.from_json(content)
        db.session.add(foodItem)
        db.session.commit()
        return jsonify(foodItem.to_json()), 200

#read
@app.route('/foodItem/', methods = ['GET'])
def get_foodItems():
    foodItems = FoodItem.query.all()
    return jsonify({ 'foodItems': [foodItem.to_json() for foodItem in foodItems] }), 200

#read
@app.route('/foodItem/<int:id>', methods = ['GET'])
def get_foodItem(id):
    foodItem = FoodItem.query.get_or_404(id)
    return jsonify(foodItem.to_json()), 200

#update
@app.route('/foodItem/<int:id>', methods = ['PUT'])
def update_foodItem(id):
    foodItem = FoodItem.query.filter_by(id=id).first()
    if foodItem:
        content = request.json
        foodItem.name = content["name"]
        foodItem.isVegan = content["isVegan"]
        foodItem.caveats = content["caveats"]
        foodItem.categoryId = content["categoryId"] # how to get category name? +++ TODO
        foodItem.isApprovedItem = content["isApprovedItem"]
        foodItem.isApprovedData = content["isApprovedData"]
        db.session.commit()
        return jsonify(message="The food was updated"), 202
    else:
        return jsonify(message="The food does not exist"), 404

#delete
@app.route('/foodItem/<int:id>', methods = ['DELETE'])
def remove_foodItem(id:int):
    foodItem = FoodItem.query.filter_by(id=id).first()
    if foodItem:
        db.session.delete(foodItem)
        db.session.commit()
        return jsonify(message="You deleted the food"), 202
    else:
        return jsonify(message="That food doesn't exist"), 404

## IS VEGAN ##
# read
@app.route('/isVegan/<string:name>', methods = ['GET'])
def isVegan(name):
    search = "%"+name+"%"
    #foodItems = FoodItem.query.filter_by(name=name).all()
    foodItems = FoodItem.query.filter(FoodItem.name.like(search)).all()
    if foodItems==[]:
        return jsonify(message="That food doesn't exist"), 404
    else:
        return jsonify({ 'foodItems': [{'id':foodItem.id, 'name':foodItem.name, 'isVegan':foodItem.isVegan, 'caveats':foodItem.caveats} for foodItem in foodItems] }), 200

# read
@app.route('/isVeganById/<int:id>', methods = ['GET'])
def isVeganById(id):
    foodItem = FoodItem.query.get_or_404(id)
    return jsonify({ 'isVegan':foodItem.isVegan, 'caveats':foodItem.caveats }), 200

# run app
if __name__ == '__main__':
    app.run(debug=True)