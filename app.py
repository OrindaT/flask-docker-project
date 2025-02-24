from flask import Flask, request, render_template
import pymysql

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'your_db'

def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    email = request.form['email']
    phone = request.form['phone']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (email, phone) VALUES (%s, %s)", (email, phone))
    connection.commit()
    cursor.close()
    connection.close()
    return "Data added successfully!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')