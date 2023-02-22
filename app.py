from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'

db = SQLAlchemy(app)


class Drinks(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f'{self.name} - {self.description}'


@app.route('/drinks')
def get_drinks():
    drinks = Drinks.query.all()

    output = []

    for drink in drinks:
        drink_data = {'name': drink.name, 'description':drink.description}

        output.append(drink_data)
    return {'drinks' : output}


@app.route('/drinks/<id>')
def get_a_drink(id):
    drink = Drinks.query.get_or_404(id)   
    return ({'name': drink.name, 'description':drink.description})

@app.route('/drinks', methods = ['POST'])
def add_drink():
    drink = Drinks(name=request.json['name'], description = request.json['description'])

    db.session.add(drink)
    db.session.commit()

    return {'id': drink.id}

@app.route('drinks/<id>', methods = ['DELETE'])
def delete_drink(id):
    drink = Drinks.query.get_or_404()
    if drink is None:
        return {'error' : 'Drink not found'}
    db.session.delete(drink)
    db.session.commit()
    return {"message": "Drink deleted!"}