from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'A15446546ab'
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM myusers")
    fetchdata = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('t3.html',data= fetchdata)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)