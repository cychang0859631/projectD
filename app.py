from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'A15446546ab'
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        numm = details['num']
        if int(numm)>20:
            cur = mysql.connection.cursor()
            cur.execute("SELECT firstname FROM myusers")
            fetchdata = cur.fetchall()
            mysql.connection.commit()
            cur.close()
            return render_template('t3.html',data= fetchdata)
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT lastname FROM myusers")
            fetchdata = cur.fetchall()
            mysql.connection.commit()
            cur.close()
            return render_template('t3.html',data= fetchdata)
    return render_template('ttt.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)