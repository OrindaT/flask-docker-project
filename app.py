from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@db:3306/your_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)

def initialize_database():
    with app.app_context():
        db.create_all()


initialize_database()


@app.route('/add', methods=['POST'])
def add_user():
    data = request.json
    email = data.get('email')
    phone = data.get('phone')

    if not email or not phone:
        return jsonify({"error": "Email and phone are required"}), 400

    new_user = User(email=email, phone=phone)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User added successfully"}), 201


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "email": user.email, "phone": user.phone} for user in users]
    return jsonify(user_list), 200


@app.route('/')
def index():
    return "Welcome to the Flask Dockerized App!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')