from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

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

class FoodItem(db.Model):
    __tablename__ = 'foodItems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    isVegan = db.Column(db.Boolean)
    caveats = db.Column(db.Text)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'))
    isApprovedItem = db.Column(db.Boolean)
    isApprovedData = db.Column(db.Boolean)

#db.create_all() 


# routes
@app.route('/')
def index():
    return '<h1>Hello World</h1>'

# run app
if __name__ == '__main__':
    app.run(debug=True)