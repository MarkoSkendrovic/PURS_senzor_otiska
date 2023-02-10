import json
from flask import Flask
from flask_mysqldb import MySQL
from hashlib import sha256
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session

app = Flask(__name__)
app.secret_key = 'rtx5c8a3&22_c'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'korisnici'
mysql = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = sha256(request.form.get('password').encode()).hexdigest()

        query = f"SELECT username,slika_profila,id_uloge FROM korisnik WHERE HEX(password) = '{password}' AND email = '{email}'"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        korisnik = cursor.fetchall()

        if korisnik:
            session['username'] = korisnik[0][0]
            session['profilna'] = korisnik[0][1]
            session['id_uloge'] = korisnik[0][2]
            print(korisnik)
            return redirect(url_for('pocetna')), 303
        else:
            return render_template('login.html', error='Uneseni su krivi korisnički podaci')



@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    session.pop('profilna', None)
    session.pop('id_uloge', None)
    return render_template('login.html')


@app.route('/', methods=['GET'])
def pocetna():
    print(session)
    if 'username' in session:
        return render_template('indeks.html', sesija=session)

    return redirect(url_for('login')), 303

@app.route('/checkin', methods=['POST'])
def prisutnost():
    print(request)
    podaci = request.get_json()
    korisnik_id = podaci["id"]

    query = f"SELECT username FROM korisnik WHERE fingerprint_id = {korisnik_id}"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    korisnik = cursor.fetchall()

    if korisnik:
        username = korisnik[0][0]
        query = f"INSERT INTO prisutnost(username) VALUES ('{username}');"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        mysql.connection.commit()
        return 'ok', 200
    return 'NOT FOUND', 404

@app.route('/pregled', methods=['GET'])
def pregled_prisutnosti():

    uloga_korisnika=session['id_uloge']
    print(uloga_korisnika)

    if uloga_korisnika==1:
        query = f"SELECT * FROM prisutnost"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        podaci = cursor.fetchall()
        print(podaci)
        return render_template('pregled.html', pregled=podaci)
    if uloga_korisnika==2:
        query = f"SELECT *FROM prisutnost WHERE username = '{session['username']}'"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        podaci = cursor.fetchall()
        print(podaci)
        return render_template('pregled.html', pregled=podaci)


if __name__ == '__main__':
    app.run(host='0.0.0.0')



