from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    # def __repr__(self):
    #     return f"<Cafe Name: {self.name}\nMap URL: {self.map_url}\n" \
    #            f"Img URL: {self.img_url}\nLocation: {self.location}\n" \
    #            f"Seats: {self.seats}\nToilet: {self.has_toilet}\n" \
    #            f"Wifi: {self.has_wifi}\nSockets: {self.has_sockets}\n" \
    #            f"Take Calls: {self.can_take_calls}\nCoffee Price: {self.coffee_price}>"


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    all_cafe = db.session.query(Cafe).all()
    cafe = choice(all_cafe)
    return jsonify(cafe={"id": cafe.id, "name": cafe.name, "map_url": cafe.map_url,
                         "img_url": cafe.img_url, "location": cafe.location, "seats": cafe.seats,
                         "has_toilet": cafe.has_toilet, "has_wifi": cafe.has_wifi, "has_sockets": cafe.has_sockets,
                         "can_take_calls": cafe.can_take_calls, "coffee_price": cafe.coffee_price})


@app.route("/all")
def get_all_cafe():
    all_cafe = db.session.query(Cafe).all()
    all_cafes = []
    for cafe in all_cafe:
        all_cafes.append({"id": cafe.id, "name": cafe.name, "map_url": cafe.map_url,
                          "img_url": cafe.img_url, "location": cafe.location, "seats": cafe.seats,
                          "has_toilet": cafe.has_toilet, "has_wifi": cafe.has_wifi, "has_sockets": cafe.has_sockets,
                          "can_take_calls": cafe.can_take_calls, "coffee_price": cafe.coffee_price})
    return jsonify(cafe=all_cafes)


@app.route("/search")
def get_a_cafe():
    all_cafe = db.session.query(Cafe).all()
    loc = request.args.get("loc")
    for cafe in all_cafe:
        if cafe.location == loc:
            return jsonify(cafe={"id": cafe.id, "name": cafe.name, "map_url": cafe.map_url,
                                 "img_url": cafe.img_url, "location": cafe.location, "seats": cafe.seats,
                                 "has_toilet": cafe.has_toilet, "has_wifi": cafe.has_wifi,
                                 "has_sockets": cafe.has_sockets,
                                 "can_take_calls": cafe.can_take_calls, "coffee_price": cafe.coffee_price})
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def post_add_cafe():
    args = request.args.get("api-key")
    if args == "TopSecretAPIKey":
        name, map_url, img_url = request.form["name"], request.form["map_url"], request.form["img_url"]
        location, seats, has_toilet = request.form["location"], request.form["seats"], request.form["has_toilet"]
        has_wifi, has_sockets = request.form["has_wifi"], request.form["has_sockets"]
        can_take_calls, coffee_price = request.form["can_take_calls"], request.form["coffee_price"]
        new_cafe = Cafe(
            name=name,
            map_url=map_url,
            img_url=img_url,
            location=location,
            seats=seats,
            has_toilet=has_toilet,
            has_wifi=has_wifi,
            has_sockets=has_sockets,
            can_take_calls=can_take_calls,
            coffee_price=coffee_price)
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})
    else:
        pass


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:id>", methods=["PATCH"])
def cafe_update_price(id):
    args = request.args.get("new_price")
    cafe = db.session.query(Cafe).get(id)
    if cafe:
        cafe.coffee_price = args
        db.session.commit()
        return jsonify(success="Successfully updated the price")
    else:
        return jsonify(error={"Not Found": "Sorry the cafe with that id was not found in the database."})


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:id>", methods=['DELETE'])
def delete_record(id):
    args = request.args.get("api-key")
    if args == "TopSecretAPIKey":
        cafe = db.session.query(Cafe).get(id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(success="Successfully deleted the query.")
        else:
            return jsonify(error={"Not Found":"Sorry a cafe with that id was not found in the database."})
    else:
        return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api-key.")


if __name__ == '__main__':
    app.run(debug=True)
