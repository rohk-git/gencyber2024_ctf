from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

# Dummy log entries for the admin dashboard
log_entries = [
    {"id": 1, "entry": "User login detected"},
    {"id": 2, "entry": "Failed login attempt"},
    {"id": 3, "entry": "Password change request"},
    {"id": 4, "entry": "2FA Code Sent"},
    {"id": 5, "entry": "Authentication Policy '2FA Required'"},
    {"id": 6, "entry": "GenCyber Activated"},
    {"id": 7, "entry": "User login detected"},
    {"id": 8, "entry": "User login detected"},
    {"id": 9, "entry": "Ratelimit reached"},
    {"id": 10, "entry": "Error"},
    {"id": 11, "entry": "Failed login attempt"},
    {"id": 12, "entry": "Password change request"},
    {"id": 13, "entry": "Password change failed"},
    {"id": 14, "entry": "Q1RGIEZsYWcgaXMuLiBuaWNlLiB0cnkuIEl0J3Mgbm90IHRoYXQgZWFzeS4="},
    {"id": 15, "entry": "Password change request"},
    {"id": 16, "entry": "Failed login attempt"},
    {"id": 17, "entry": "Failed login attemptt"},
    {"id": 18, "entry": "Failed login attempt"},
]

# CTF flag
CTF_FLAG = "CTF_FLAG"

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'user' and password == 'password':
        resp = make_response(redirect(url_for('dashboard')))
        resp.set_cookie('admin', 'false')
        resp.set_cookie('enduser', 'true')
        return resp
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    enduser = request.cookies.get('enduser')
    if enduser == 'true':
        return render_template('user_dashboard.html')
    return "Access denied."

@app.route('/admin_dashboard')
def admin_dashboard():
    admin = request.cookies.get('admin')
    enduser = request.cookies.get('enduser')
    if enduser == 'true':
        if admin == 'true':
            return render_template('admin_dashboard.html', logs=log_entries)
        return "Access denied. You are not an admin."
    return "Access denied."

@app.route('/logs')
def logs():
    admin = request.cookies.get('admin')
    enduser = request.cookies.get('enduser')
    if enduser == 'true':
        if admin == 'true':
            log_id = request.args.get('id', type=int)
            if log_id == 1337:
                return f"Flag: {CTF_FLAG}"
            return "Normal log entry. Keep looking!"
        return "Access denied. You are not an admin."
    return "Access denied."

if __name__ == '__main__':
    app.run(debug=False)
