import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'ekderwasecretkey99'

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def get_db_connection():
    return psycopg2.connect(host="localhost", database="postgres", user="postgres", password="admin123", port="5432")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    if 'user_id' in session: return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name, mobile, email, password, re_password = request.form['name'], request.form['mobile'], request.form['email'], request.form['password'], request.form['re_password']
        if password != re_password:
            flash("Error: Dono Password match nahi ho rahe hain!")
            return redirect(url_for('register'))
        conn = get_db_connection(); cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM web_users WHERE email = %s OR mobile = %s", (email, mobile))
            if cur.fetchone():
                flash("Error: Email ya Mobile Number pehle se registered hai!")
                return redirect(url_for('register'))
            cur.execute("INSERT INTO web_users (name, mobile, email, password) VALUES (%s, %s, %s, %s)", (name, mobile, email, password))
            conn.commit()
            flash("Success: Account ban gaya! Ab login karein.")
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback(); flash(f"Database Error: {str(e)}")
        finally: cur.close(); conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input, password = request.form['login_input'], request.form['password']
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT id, name, password FROM web_users WHERE email = %s OR mobile = %s", (login_input, login_input))
        user = cur.fetchone(); cur.close(); conn.close()
        if user and user[2] == password:
            session['user_id'], session['user_name'] = user[0], user[1]
            return redirect(url_for('dashboard'))
        flash("Error: Invalid Email/Mobile ya Password!")
    return render_template('login.html')

# 1. MAIN DASHBOARD ROUTE (FIXED)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("SELECT target_post, batch_time, running_1600m, profile_pic FROM web_users WHERE id = %s", (session['user_id'],))
    data = cur.fetchone(); cur.close(); conn.close()
    
    t_post = data[0] if data and data[0] else 'Bihar Police'
    b_time = data[1] if data and data[1] else 'Morning (5:00 AM)'
    run_t = data[2] if data and data[2] else '00:00'
    p_pic = data[3] if data and data[3] else 'default_avatar.png'
    
    return render_template('dashboard.html', target_post=t_post, batch_time=b_time, running_1600m=run_t, profile_pic=p_pic)

# 2. MY PROFILE ROUTE (FIXED)
@app.route('/profile')
def profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("SELECT mobile, email, profile_pic, target_post, batch_time, student_height, student_chest, running_1600m FROM web_users WHERE id = %s", (session['user_id'],))
    data = cur.fetchone(); cur.close(); conn.close()
    
    p_pic = data[2] if data and data[2] else 'default_avatar.png'
    return render_template('profile.html', 
                           user_mobile=data[0] if data else '', 
                           user_email=data[1] if data else '', 
                           profile_pic=p_pic, 
                           target_post=data[3] if data and data[3] else 'Bihar Police', 
                           batch_time=data[4] if data and data[4] else 'Morning', 
                           student_height=data[5] if data and data[5] else 'Not Measured', 
                           student_chest=data[6] if data and data[6] else 'Not Measured', 
                           running_1600m=data[7] if data and data[7] else '00:00')

# 3. UPDATE PROFILE PAGE (INDEX INDEX FIXED)
@app.route('/update_profile_page')
def update_profile_page():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("SELECT target_post, batch_time, student_height, student_chest, running_1600m, profile_pic FROM web_users WHERE id = %s", (session['user_id'],))
    data = cur.fetchone(); cur.close(); conn.close()
    
    p_pic = data[5] if data and data[5] else 'default_avatar.png'
    return render_template('update_profile.html', 
                           target_post=data[0] if data and data[0] else '', 
                           batch_time=data[1] if data and data[1] else '', 
                           student_height=data[2] if data and data[2] else '', 
                           student_chest=data[3] if data and data[3] else '', 
                           running_1600m=data[4] if data and data[4] else '', 
                           profile_pic=p_pic)

# 4. ACTION UPDATE ROUTE (FIXED)
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    name = request.form['name']
    target_post = request.form['target_post']
    batch_time = request.form['batch_time']
    student_height = request.form['student_height']
    student_chest = request.form['student_chest']
    running_1600m = request.form['running_1600m']
    
    file = request.files.get('profile_pic')
    conn = get_db_connection(); cur = conn.cursor()
    try:
        if file and allowed_file(file.filename):
            filename = secure_filename(f"cadet_{session['user_id']}_{file.filename}")
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cur.execute("UPDATE web_users SET name=%s, target_post=%s, batch_time=%s, student_height=%s, student_chest=%s, running_1600m=%s, profile_pic=%s WHERE id=%s", 
                        (name, target_post, batch_time, student_height, student_chest, running_1600m, filename, session['user_id']))
        else:
            cur.execute("UPDATE web_users SET name=%s, target_post=%s, batch_time=%s, student_height=%s, student_chest=%s, running_1600m=%s WHERE id=%s", 
                        (name, target_post, batch_time, student_height, student_chest, running_1600m, session['user_id']))
        conn.commit(); session['user_name'] = name
        flash("Success: Profile successfully update ho gayi!")
    except Exception as e: 
        conn.rollback(); flash(f"Update Error: {str(e)}")
    finally: cur.close(); conn.close()
    return redirect(url_for('profile'))

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email, new_password, re_password = request.form['email'], request.form['new_password'], request.form['re_password']
        if new_password != re_password:
            flash("Error: Dono Password match nahi ho rahe hain!"); return redirect(url_for('forgot'))
        conn = get_db_connection(); cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM web_users WHERE email = %s", (email,))
            if not cur.fetchone(): flash("Error: Yeh Email registered nahi hai!"); return redirect(url_for('forgot'))
            cur.execute("UPDATE web_users SET password = %s WHERE email = %s", (new_password, email)); conn.commit()
            flash("Success: Password badal gaya! Naye password se login karein.")
            return redirect(url_for('login'))
        except Exception as e: conn.rollback(); flash(f"Database Error: {str(e)}")
        finally: cur.close(); conn.close()
    return render_template('forgot.html')

@app.route('/logout')
def logout():
    session.clear(); return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
