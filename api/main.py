from flask import Flask, jsonify
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'metrobus_db'
app.config['MYSQL_PORT'] = 33066

mysql = MySQL(app)

def return_500_if_errors(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            response = {
                'status_code': 500,
                'status': 'Internal Server Error'
            }
            return jsonify(response), 500
    return wrapper

@app.route('/', methods=['GET'])
@return_500_if_errors
def homepage():
    return """
        <!DOCTYPE html>
        <html>

        <head>
        <title>Welcome to Metrobus API</title>
        </head>

        <body>

            <h1>Welcome to Metrobus API</h1>
            <h2>Metrobus Endpoint:</h2>

            <p>
                This Endpoint is used to get the metrobuses list. <br>
                https://localhost:5000/metrobuses
            </p>
            <p>
                This Endpoint is used to get the metrobuses by vehicle_id. <br>
                https://localhost:5000/metrobuses/<vehicle_id>
            </p>
            <p>
                This Endpoint is used to get the metrobuses by vehicle_id. <br>
                https://localhost:5000/metrobuses/<vehicle_id>
            </p>
            <p>
                This Endpoint is used to get the metrobuses list. <br>
                 https://localhost:5000/metrobuses
            </p>

        </body>
    </html>
    """

# @app.route('/metrobuses', methods=['GET'])
# def get_metrobuses():
#     """
#         This Endpoint is used to get the metrobuses list.
#             https://localhost:5000/metrobuses
#     """
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT * FROM metrobus''')
#     rv = cur.fetchall()
#     return jsonify({"data": rv})

@app.route('/metrobuses', methods=['GET'])
@app.route('/metrobuses/<int:vehicle_id>', methods=['GET'])
def get_metrobuses_by_vehicle_id(vehicle_id = None):
    """
        This Endpoint is used to get the metrobuses by vehicle_id.
            https://localhost:5000/metrobuses/<vehicle_id>
            This route just admits the vehicle_id as integer parameter.

            This Endpoint is used to get the metrobuses list.
            https://localhost:5000/metrobuses
    """
    cur = mysql.connection.cursor()
    if vehicle_id is not None:
        cur.execute('''SELECT * FROM metrobus WHERE vehicle_id = %s''', (vehicle_id,))
    else:
        cur.execute('''SELECT * FROM metrobus''')

    rv = cur.fetchall()
    return jsonify({"data": rv})


# @app.route('/metrobuses/county', methods=['GET'])
# def get_available_county():
#     """
#         This Endpoint is used to get the available counties.
#             https://localhost:5000/metrobuses/county
#     """
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT DISTINCT county FROM metrobus''')
#     rv = cur.fetchall()
#     return jsonify({"data": rv})

@app.route('/metrobuses/county', methods=['GET'])
@app.route('/metrobuses/county/<string:county>', methods=['GET'])
def get_metrobuses_by_county(county = None):
    """
        This Endpoint is used to get the metrobuses by county.\
            https://localhost:5000/metrobuses/county/<county>
            This route just admits the county as string parameter.

        This Endpoint is used to get the available counties.
            https://localhost:5000/metrobuses/county
    """
    cur = mysql.connection.cursor()
    if county is not None:
        cur.execute('''SELECT * FROM metrobus WHERE county = %s''', (county,))
    else:
        cur.execute('''SELECT DISTINCT county FROM metrobus''')
    rv = cur.fetchall()
    return jsonify({"data": rv})


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)