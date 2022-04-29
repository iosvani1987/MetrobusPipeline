from flask import Flask, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = '192.168.1.115'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'metrobus_db'
app.config['MYSQL_PORT'] = 33066

mysql = MySQL(app)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/<name>')
def hello(name):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM metrobus''')
    rv = cur.fetchall()
    return jsonify({"data": rv})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)