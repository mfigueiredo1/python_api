
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy #ORM

app = Flask(__name__)

# Create a Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'

db = SQLAlchemy(app)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)



    def to_Dict(self):
        return {
            'id': self.id,
            'destination': self.destination,
            'country': self.country,
            'rating': self.rating
            # This makes it easier to conver to JSON later
        }

with app.app_context():
    db.create_all()

# Create Routes
#https://www.thenerdnook.io/
@app.route('/')
def home():
    
    return jsonify({"message":"Welcome to the Travel API"})

#https://www.thenerdnook.io/destinations
@app.route("/destinations", methods=["GET"])
def get_destinations():
    destinations = Destination.query.all()

    return jsonify([destination.to_Dict() for destination in destinations])


#https://www.thenerdnook.io/destination/2
@app.route("/destinations/<int:destination_id>", methods=["GET"])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        return jsonify(destination.to_Dict())
    else:
        return jsonify({'message': 'No destination found with that ID'}), 404


# POST (Send information to our API)


@app.route("/destinations", methods=['POST'])
def add_destination():
    data = request.get_json()
    #taking the incoming json body and parsing that information

    # make an object using that so we can insert it into our database

    new_destination = Destination(destination=data['destination'], country=data['country'], rating=data['rating'])

    # here we need to insert this new object into the database and tap into the current session we're on
    db.session.add(new_destination)
    db.session.commit()


    return jsonify(new_destination.to_Dict()), 201


# PUT -> Update
@app.route("/destinations/<int:destination_id>", methods=['PUT'])

def update_destination(destination_id):
    data = request.get_json()
    destination = Destination.query.get(destination_id)

    if destination:
        destination.destination = data.get('destination', destination.destination)
        destination.country = data.get('country', destination.country)
        destination.rating = data.get('rating', destination.rating)

        db.session.commit()

        return jsonify(destination.to_Dict())
    else:
        return jsonify({'message': 'No destination found'}), 404
    
# DELETE
@app.route("/destinations/<int:destination_id>", methods=['DELETE'])
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)

    if destination:
        db.session.delete(destination)
        db.session.commit()

        return jsonify({'message': 'Destination has been deleted'})
    else:
        return jsonify({'message': 'No destination found'}), 404



if __name__ == '__main__':
    app.run(debug=True)