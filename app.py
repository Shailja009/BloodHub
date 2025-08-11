from flask import Flask, render_template, request, redirect, url_for, session, send_file
import sqlite3
import csv
import io

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# --- DATABASE CONNECTION ---
def get_db_connection():
    conn = sqlite3.connect('blood_reservation.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- HOME PAGE ---
@app.route('/')
def home():
    return render_template('home.html')

# --- DONOR FORM ---
@app.route('/donor', methods=['GET', 'POST'])
def donor_form():
    if request.method == 'POST':
        data = {k: request.form.get(k) for k in ['name', 'sex', 'age', 'height', 'weight', 'blood_type', 'illness', 'allergy', 'phone', 'city']}
        conn = get_db_connection()
        conn.execute("INSERT INTO donors (name, sex, age, height, weight, blood_type, illness, allergy, phone, city) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     tuple(data.values()))
        conn.commit()
        conn.close()
        camp_info = match_camp(data['city'])
        return render_template('confirmation.html', data=data, camp_info=camp_info)
    return render_template('donor_form.html')

# --- RECEIVER FORM ---
@app.route('/receiver', methods=['GET', 'POST'])
def receiver_form():
    if request.method == 'POST':
        data = {k: request.form.get(k) for k in ['name', 'sex', 'age', 'height', 'weight', 'blood_type', 'illness', 'allergy', 'phone', 'city']}
        conn = get_db_connection()
        conn.execute("INSERT INTO receivers (name, sex, age, height, weight, blood_type, illness, allergy, phone, city) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     tuple(data.values()))
        conn.commit()
        conn.close()
        camp_info = match_camp(data['city'])
        return render_template('confirmation.html', data=data, camp_info=camp_info)
    return render_template('receiver_form.html')

def match_camp(city):
    city = city.lower()
    camp_database = {
        'delhi': [
            'AIIMS Blood Bank, Ansari Nagar, Delhi',
            'Red Cross Center, Connaught Place, Delhi',
            'Max Healthcare, Saket, Delhi'
        ],
        'mumbai': [
            'KEM Hospital, Parel, Mumbai',
            'Hinduja Hospital, Mahim, Mumbai',
            'Tata Memorial, Parel, Mumbai'
        ],
        'bangalore': [
            'NIMHANS Blood Center, Hosur Road',
            'Manipal Hospital, Old Airport Road',
            'St. John\'s Medical College, Koramangala'
        ],
        'kolkata': [
            'Apollo Gleneagles, Salt Lake',
            'Swasthya Bhawan Blood Bank, GN-29, Sector-V',
            'Sambhu Nath Pandit Hospital, Elgin Road'
        ]
    }

    return camp_database.get(city, [
        'Central Blood Bank, Contact local health center',
        'Nearest Govt Hospital Blood Unit',
        'District Red Cross Society Office'
    ])

# --- ADMIN LOGIN ---
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
    return render_template('admin_login.html')

# --- ADMIN PANEL ---
@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    search_blood = request.args.get('search_blood', '').strip().lower()
    search_city = request.args.get('search_city', '').strip().lower()

    conn = get_db_connection()
    donors = conn.execute("SELECT * FROM donors").fetchall()
    receivers = conn.execute("SELECT * FROM receivers").fetchall()
    conn.close()

    if search_blood:
        donors = [d for d in donors if d['blood_type'].lower() == search_blood]
        receivers = [r for r in receivers if r['blood_type'].lower() == search_blood]
    if search_city:
        donors = [d for d in donors if d['city'] and d['city'].lower() == search_city]
        receivers = [r for r in receivers if r['city'] and r['city'].lower() == search_city]

    return render_template('admin.html', donors=donors, receivers=receivers)

# --- EXPORT TO CSV ---
@app.route('/export_csv')
def export_csv():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    donors = conn.execute("SELECT * FROM donors").fetchall()
    receivers = conn.execute("SELECT * FROM receivers").fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['--- DONORS ---'])
    writer.writerow(['ID', 'Name', 'Sex', 'Age', 'Height', 'Weight', 'Blood Type', 'Illness', 'Allergy', 'Phone', 'City'])
    for row in donors:
        writer.writerow([row['id'], row['name'], row['sex'], row['age'], row['height'], row['weight'], row['blood_type'], row['illness'], row['allergy'], row['phone'], row['city']])

    writer.writerow([])
    writer.writerow(['--- RECEIVERS ---'])
    writer.writerow(['ID', 'Name', 'Sex', 'Age', 'Height', 'Weight', 'Blood Type', 'Illness', 'Allergy', 'Phone', 'City'])
    for row in receivers:
        writer.writerow([row['id'], row['name'], row['sex'], row['age'], row['height'], row['weight'], row['blood_type'], row['illness'], row['allergy'], row['phone'], row['city']])

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='blood_data.csv')

# --- LOGOUT ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/delete/<type>/<int:id>')
def delete_entry(type, id):
    conn = sqlite3.connect('blood_reservation.db')
    cursor = conn.cursor()
    if type == 'donor':
        cursor.execute('DELETE FROM donors WHERE id = ?', (id,))
    elif type == 'receiver':
        cursor.execute('DELETE FROM receivers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)
