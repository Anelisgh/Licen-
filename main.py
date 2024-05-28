# import modules:
from flask import jsonify, render_template, request, redirect, url_for, session, flash
from datetime import timedelta, date, datetime
from werkzeug.security import check_password_hash
from app import app
import json
from mysql.connector import connect
from functools import wraps # for @login_required

app.permanent_session_lifetime = timedelta(hours=1) # după cât timp să delogheze utilizatorul

def get_db():
    with open('pswd.json') as pwsd:
        data = json.load(pwsd)
        password = data['password']
    db = connect(
        host="localhost",
        user="root",
        password=password,
        database="mydatabase",    
    )
    return db

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Conectează-te pentru a accesa pagina!")
            return redirect(url_for("conectare"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["POST", "GET"])
def conectare():
    if request.method == "POST":
        session.permanent = True
        nume = request.form["nume"]
        parola = request.form['parola']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Angajati WHERE nume = %s", (nume,))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        if user and user[2]: 
            stored_password = user[2] 
            if check_password_hash(stored_password, parola):
                session['user'] = nume
                flash(f"Bine ai revenit, {nume}!")
                return redirect(url_for('angajati'))
            else:
                flash('Parola este incorectă!')
        else:
            flash('Numele este incorect!')
    else:
        if "user" in session:
            return redirect(url_for('angajati'))
    return render_template("conectare.html")

@app.route("/deconectare")
def deconectare():
    session.pop("user", None)
    flash("Te-ai deconectat cu succes!")
    return redirect(url_for("conectare"))

@app.route("/angajati", methods=["POST", "GET"])
@login_required
def angajati():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT nume FROM angajati")
    angajati = cursor.fetchall()
    cursor.execute("SELECT * FROM Angajati ORDER BY FIELD(functie, 'Director','Secretara','Consilier','Traducator','Muncitor calificat','Ingrijitor','Conducator auto','Portar')")
    lista_angajati = cursor.fetchall()
    if request.method == 'POST':
        if 'adaugare' in request.form:
            nume = request.form['numeA']
            serie_actIdentitate = request.form['serie_actIdentitateA']
            CNP = request.form['CNPA']
            dataNastere = request.form['dataNastereA']
            dataEmitere_actIdentitate = request.form['dataEmitere_actIdentitateA']
            dataExpirare_actIdentitate = request.form['dataExpirare_actIdentitateA']
            functie = request.form['functieA']
            dataAngajare = date.fromisoformat(request.form['dataAngajareA'])
            vechimeAnterioara = int(request.form['vechimeAnterioaraA'])
            salariu = request.form['salariuA']
            vechimeInInstitutie = date.today().year - dataAngajare.year
            vechimeTotala = vechimeInInstitutie + vechimeAnterioara
            cursor.execute("INSERT INTO angajati (nume, serie_actIdentitate, CNP, dataNastere, dataEmitere_actIdentitate, dataExpirare_actIdentitate, functie, dataAngajare, vechimeInInstitutie, vechimeAnterioara, vechimeTotala, salariu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
(nume, serie_actIdentitate, CNP, dataNastere, dataEmitere_actIdentitate, dataExpirare_actIdentitate, functie, dataAngajare, vechimeInInstitutie, vechimeAnterioara, vechimeTotala, salariu))
            db.commit()
            flash('Adăugarea a fost un succes!')
        elif 'modifica' in request.form:
            nume_modificare = request.form['NumeModificare']
            nume = request.form['numeM']
            data_nastere = request.form['dataNastereM']
            functie = request.form['functieM']
            data_angajare = request.form['dataAngajareM']
            vechime_anterioara = request.form['vechimeAnterioaraM']
            salariu = request.form['salariuM']
            serie_act_identitate = request.form['serie_actIdentitateM']
            CNP = request.form['CNPM']
            data_emitere_act_identitate = request.form['dataEmitere_actIdentitateM']
            data_expirare_act_identitate = request.form['dataExpirare_actIdentitateM']
            if data_angajare or vechime_anterioara:
                cursor.execute(f"SELECT dataAngajare, vechimeAnterioara FROM angajati WHERE nume = '{nume_modificare}'")
                data_angajare_db, vechime_anterioara_db = cursor.fetchone()
                if data_angajare:
                    data_angajare = date.fromisoformat(data_angajare)
                else:
                    data_angajare = data_angajare_db
                if vechime_anterioara:
                    vechime_anterioara = int(vechime_anterioara)
                else:
                    vechime_anterioara = vechime_anterioara_db
                vechime_in_institutie = date.today().year - data_angajare.year
                vechime_totala = vechime_in_institutie + vechime_anterioara
            update_query = "UPDATE angajati SET "
            if nume:
                update_query += f"nume = '{nume}', "
            if data_nastere:
                update_query += f"dataNastere = '{data_nastere}', "
            if functie:
                update_query += f"functie = '{functie}', "
            if data_angajare:
                update_query += f"dataAngajare = '{data_angajare}', " 
            if data_angajare or vechime_anterioara:
                update_query += f"vechimeAnterioara = {vechime_anterioara}, "
                update_query += f"vechimeInInstitutie = {vechime_in_institutie}, "
                update_query += f"vechimeTotala = {vechime_totala}, "
            if salariu:
                update_query += f"salariu = {salariu}, "
            if serie_act_identitate:
                update_query += f"serie_actIdentitate = '{serie_act_identitate}', "
            if CNP:
                update_query += f"CNP = {CNP}, "
            if data_emitere_act_identitate:
                update_query += f"dataEmitere_actIdentitate = '{data_emitere_act_identitate}', "
            if data_expirare_act_identitate:
                update_query += f"dataExpirare_actIdentitate = '{data_expirare_act_identitate}', "
            if data_angajare:
                update_query += f"vechimeInInstitutie = {vechime_in_institutie}, "
                update_query += f"vechimeTotala = {vechime_totala}, "
            update_query = update_query[:-2]
            update_query += f" WHERE nume = '{nume_modificare}'"
            cursor.execute(update_query)
            db.commit()
            flash('Modificarea a fost un succes!')
        elif 'sterge' in request.form:
            nume_angajat = request.form['NumeAngajat']
            cursor.execute("DELETE FROM angajati WHERE nume = %s", (nume_angajat,))
            flash('Ștergerea a fost un succes!')
        db.commit()
        return redirect(url_for('angajati'))
    cursor.close()
    db.close()
    return render_template('angajati.html', Angajati=angajati, lista_angajati=lista_angajati)

# pt form -> modificare ca datele sa apara introduse automat
@app.route('/get_date_angajat')
@login_required
def get_date_angajat():
    nume = request.args.get('nume')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Angajati WHERE nume = %s", (nume,))
    row = cursor.fetchone()
    date_angajat = {
        'nume': row[1],
        'dataNastere': row[5].strftime('%Y-%m-%d') if row[5] else '',
        'functie': row[8],
        'dataAngajare': row[9].strftime('%Y-%m-%d') if row[9] else '',
        'vechimeAnterioara': row[11],
        'salariu': row[13],
        'serie_actIdentitate': row[3],
        'CNP': row[4],
        'dataEmitere_actIdentitate': row[6].strftime('%Y-%m-%d') if row[6] else '',
        'dataExpirare_actIdentitate': row[7].strftime('%Y-%m-%d') if row[7] else ''
    }
    return jsonify(date_angajat)


@app.route("/concedii", methods=["POST", "GET"])
@login_required
def concedii():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT nume FROM angajati")
    angajati = cursor.fetchall()
    cursor.execute("SELECT * FROM Angajati")
    lista_angajati = cursor.fetchall()
    concedii_angajati = {}
    for angajat in lista_angajati:
        id_angajat = angajat[0]
        an_curent = datetime.now().year
        cursor.execute(f"SELECT tipConcediu, DATEDIFF(dataSfarsit, dataInceput) + 1 as durata FROM Concedii WHERE id_angajat={id_angajat} AND YEAR(dataInceput)={an_curent}")
        concedii = cursor.fetchall()
        odihna = medical = fara_plata = 0
        for concediu in concedii:
            tip = concediu[0]
            durata = concediu[1]
            if tip == 'Odihna':
                odihna += durata
            elif tip == 'Medical':
                medical += durata
            elif tip == 'Fara plata':
                fara_plata += durata
        zile_ramase = 35 - odihna
        concedii_angajati[id_angajat] = [odihna, medical, fara_plata, zile_ramase]
    if request.method == 'POST':
        if 'adaugare' in request.form:
            nume_modificareC = request.form['NumeAngajatA']
            tipConcediu = request.form['tipConcediuA']
            dataCerere = date.fromisoformat(request.form['dataCerereA'])
            dataInceput = date.fromisoformat(request.form['dataInceputA'])
            dataSfarsit = date.fromisoformat(request.form['dataSfarsitA'])
            eliberatDe = request.form['eliberatDeA']
            diagnostic = request.form['diagnosticA']
            accidentMunca = request.form['accidentMuncaA']
            if accidentMunca not in ['Da', 'Nu', '']:
                accidentMunca = ''
            cursor.execute("SELECT id FROM Angajati WHERE nume = %s", (nume_modificareC,))
            id_angajat = cursor.fetchone()[0]
            cursor.execute("INSERT INTO Concedii (id_angajat, tipConcediu, dataCerere, dataInceput, dataSfarsit, eliberatDe, diagnostic, accidentMunca) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (id_angajat, tipConcediu, dataCerere, dataInceput, dataSfarsit, eliberatDe, diagnostic, accidentMunca))
            db.commit()
            flash('Adăugarea a fost un succes!')
        elif 'modifica' in request.form:
            nume_modificareC = request.form['NumeAngajatM']
            data_cerere = request.form['Cerere']
            tip_concediu = request.form['tipConcediuM']
            data_cerere_noua = request.form['dataCerereM']
            data_inceput = request.form['dataInceputM']
            data_sfarsit = request.form['dataSfarsitM']
            eliberat_de = request.form['eliberatDeM']
            diagnostic = request.form['diagnosticM']
            accident_munca = request.form['accidentMuncaM']
            cursor.execute("SELECT id FROM Angajati WHERE nume = %s", (nume_modificareC,))
            id_angajat = cursor.fetchone()[0]
            update_query = "UPDATE concedii SET "
            if tip_concediu: update_query += f"tipConcediu = '{tip_concediu}', "
            if data_cerere_noua: update_query += f"dataCerere = '{data_cerere_noua}', "
            if data_inceput: update_query += f"dataInceput = '{data_inceput}', "
            if data_sfarsit: update_query += f"dataSfarsit = '{data_sfarsit}', "
            if eliberat_de: update_query += f"eliberatDe = '{eliberat_de}', "
            if diagnostic: update_query += f"diagnostic = '{diagnostic}', "
            if accident_munca and accident_munca != "": update_query += f"accidentMunca = '{accident_munca}', "
            update_query = update_query[:-2]
            update_query += f" WHERE id_angajat = {id_angajat} AND dataCerere = '{data_cerere}'"
            cursor.execute(update_query)
            db.commit()
            flash('Modificarea a fost un succes!')
        elif 'sterge' in request.form:
            nume_angajat = request.form['NumeAngajatS']
            data_cerere = request.form['dataCerere']  
            cursor.execute("SELECT id FROM Angajati WHERE nume = %s", (nume_angajat,))
            id_angajat = cursor.fetchone()[0]
            cursor.execute("DELETE FROM concedii WHERE id_angajat = %s AND dataCerere = %s", (id_angajat, data_cerere))
            db.commit()
            flash('Ștergerea a fost un succes!')
            return redirect(url_for('concedii'))
    cursor.close()
    db.close()
    return render_template('concedii.html', Angajati=angajati, lista_angajati=lista_angajati, concedii_angajati=concedii_angajati)

@app.route('/get_cereri')
@login_required
def get_cereri():
    angajat = request.args.get('angajat')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT dataCerere FROM Concedii WHERE id_angajat = (SELECT id FROM Angajati WHERE nume = %s)", (angajat,))
    cereri = [item[0].strftime('%Y-%m-%d') for item in cursor.fetchall()]
    return jsonify(cereri)

@app.route('/get_date_cerere')
@login_required
def get_date_cerere():
    angajat = request.args.get('angajat')
    cerere = request.args.get('cerere')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Concedii WHERE id_angajat = (SELECT id FROM Angajati WHERE nume = %s) AND dataCerere = %s", (angajat, cerere))
    row = cursor.fetchone()
    date_cerere = {
        'tipConcediu': row[2],
        'dataCerere': row[3].strftime('%Y-%m-%d'),
        'dataInceput': row[4].strftime('%Y-%m-%d'),
        'dataSfarsit': row[5].strftime('%Y-%m-%d'),
        'eliberatDe': row[6],
        'diagnostic': row[7],
        'accidentMunca': row[8]
    }
    return jsonify(date_cerere)

@app.route("/detalii_concedii/<int:id_angajat>/<tip_concediu>", methods=["GET"])
@login_required
def detalii_concedii(id_angajat, tip_concediu):
    db = get_db()
    cursor = db.cursor()
    if tip_concediu == 'Medical':
        cursor.execute(f"SELECT dataCerere, dataInceput, dataSfarsit, eliberatDe, diagnostic, accidentMunca FROM Concedii WHERE id_angajat={id_angajat} AND tipConcediu='{tip_concediu}' ORDER BY dataInceput")
    else:
        cursor.execute(f"SELECT dataCerere, dataInceput, dataSfarsit FROM Concedii WHERE id_angajat={id_angajat} AND tipConcediu='{tip_concediu}' ORDER BY dataInceput")
    concedii = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('detalii_concedii.html', concedii=concedii, tip_concediu=tip_concediu)

@app.route('/date_histograma_concedii')
@login_required
def date_histograma_concedii():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT MONTH(Concedii.dataInceput) as luna, COUNT(*) as numarConcedii
        FROM Concedii
        JOIN Angajati ON Concedii.id_angajat = Angajati.id
        GROUP BY luna
    """)
    rezultate = cursor.fetchall()
    date_histograma_concedii = {}
    for rezultat in rezultate:
        luna, numar_concedii = rezultat
        date_histograma_concedii[luna] = numar_concedii
    cursor.close()
    db.close()
    return jsonify(date_histograma_concedii)

@app.route('/unitate/concedii')
@login_required
def histograma_concedii():
    return render_template('histograma_concedii.html')

@app.route('/date_histograma_varsta')
@login_required
def date_histograma_varsta():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT FLOOR((YEAR(CURDATE()) - YEAR(dataNastere)) / 5) * 5 as varsta, COUNT(*) as numarAngajati
        FROM Angajati
        GROUP BY varsta
    """)
    rezultate = cursor.fetchall()
    date_histograma_varsta = {}
    for rezultat in rezultate:
        varsta, numar_angajati = rezultat
        date_histograma_varsta[varsta] = numar_angajati
    cursor.close()
    db.close()
    return jsonify(date_histograma_varsta)

@app.route('/unitate/varsta')
@login_required
def histograma_varsta():
    return render_template('histograma_varsta.html')

@app.route('/date_histograma_vechime')
@login_required
def date_histograma_vechime():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT FLOOR(vechimeInInstitutie / 3) * 3 as vechime, COUNT(*) as numarAngajati
        FROM Angajati
        WHERE vechimeInInstitutie IS NOT NULL
        GROUP BY vechime
    """)
    rezultate = cursor.fetchall()
    date_histograma_vechime = {}
    for rezultat in rezultate:
        vechime, numar_angajati = rezultat
        date_histograma_vechime[vechime] = numar_angajati
    cursor.close()
    db.close()
    return jsonify(date_histograma_vechime)

@app.route('/unitate/vechime')
@login_required
def histograma_vechime():
    return render_template('histograma_vechime.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nume = session['user'] if 'user' in session else request.form.get('nume')
        email = request.form.get('email')
        mesaj = request.form.get('mesaj')
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO Contact (nume, email, mesaj) VALUES (%s, %s, %s)", (nume, email, mesaj))
        db.commit()
        cursor.close()
        db.close()
        flash('Mesajul a fost trimis cu succes!')
        return redirect(url_for("contact"))
    else:
        if "user" in session:
            return render_template('contact_in_session.html')
        else:
            return render_template('contact_not_in_session.html')

#  În acest mod, serverul Flask va reporni automat de fiecare dată când detectează o modificare în codul sursă. Acest lucru este foarte util în timpul dezvoltării, deoarece permite actualizarea aplicației fără a fi necesar să o opriți și să o porniți de fiecare dată când faceți o schimbare.       
if __name__ == "__main__":
    app.run(debug=True)
