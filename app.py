from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Swe21tha07$'   
app.config['MYSQL_DB'] = 'bloodbank'

mysql = MySQL(app)

# Home (redirect to donors page)
@app.route('/')
def index():
    return redirect(url_for('donors'))

# View donors
@app.route('/donors')
def donors():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM donor")
    data = cur.fetchall()
    cur.close()
    return render_template('donors.html', donors=data)

# Add donor
@app.route('/add', methods=['GET', 'POST'])
def add_donor():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        bloodgroup = request.form['bloodgroup']
        lastdate = request.form['lastdonationdate']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO donor(name, age, gender, bloodgroup, lastdonationdate) VALUES (%s,%s,%s,%s,%s)",
            (name, age, gender, bloodgroup, lastdate)
        )
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('donors'))

    return render_template('adddonor.html')

# Delete donor
@app.route('/delete/<int:id>')
def delete_donor(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM donor WHERE donorid=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('donors'))

# Edit donor
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_donor(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        bloodgroup = request.form['bloodgroup']
        lastdate = request.form['lastdonationdate']

        cur.execute("""
            UPDATE donor 
            SET name=%s, age=%s, gender=%s, bloodgroup=%s, lastdonationdate=%s
            WHERE donorid=%s
        """, (name, age, gender, bloodgroup, lastdate, id))

        mysql.connection.commit()
        cur.close()
        return redirect(url_for('donors'))

    cur.execute("SELECT * FROM donor WHERE donorid=%s", (id,))
    data = cur.fetchone()
    cur.close()

    return render_template('editdonor.html', donor=data)
@app.route('/bloodstock')
def bloodstock():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bloodstock")
    data = cur.fetchall()
    cur.close()
    return render_template('bloodstock.html', stock=data)
@app.route('/hospitals')
def hospitals():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hospital")
    data = cur.fetchall()
    cur.close()
    return render_template('hospitals.html', hospitals=data)


@app.route('/add_hospital', methods=['GET', 'POST'])
def add_hospital():
    if request.method == 'POST':
        name = request.form['hospitalname']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO hospital(hospitalname) VALUES (%s)", (name,))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('hospitals'))

    return render_template('addhospital.html')
@app.route('/requests')
def requests_page():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bloodrequest")
    data = cur.fetchall()
    cur.close()
    return render_template('requests.html', requests=data)


@app.route('/add_request', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        bloodgroup = request.form['bloodgroup']
        units = request.form['units']
        hospitalid = request.form['hospitalid']

        cur = mysql.connection.cursor()

        # Check stock
        cur.execute("SELECT unitsavailable FROM bloodstock WHERE bloodgroup=%s", (bloodgroup,))
        stock = cur.fetchone()

        if stock and stock[0] >= int(units):
            status = "Approved"
            cur.execute("UPDATE bloodstock SET unitsavailable = unitsavailable - %s WHERE bloodgroup=%s",
                        (units, bloodgroup))
        else:
            status = "Rejected"

        cur.execute("""
            INSERT INTO bloodrequest (bloodgroupreq, units, requestdate, status, hospitalid)
            VALUES (%s, %s, CURDATE(), %s, %s)
        """, (bloodgroup, units, status, hospitalid))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('requests_page'))

    return render_template('addrequest.html')
                


if __name__ == '__main__':
    app.run(debug=True)