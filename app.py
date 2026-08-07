import os
import hashlib
import io
from datetime import datetime
from flask import Flask, render_template_string, request, session, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
from flask_jwt_extended import JWTManager
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "nsongwa-bank-super-secret-jwt-key") # Change in production
jwt = JWTManager(app)

# Registered API Blueprints

app.secret_key = os.getenv("FLASK_SECRET_KEY", "nsongwa_secure_2026")

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- 1. DATABASE MODELS ---
class User(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pin_hash = db.Column(db.String(128), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    transactions = db.relationship('Transaction', backref='owner', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20)) 
    amount = db.Column(db.Float)
    # THIS LINE ADDS THE TIME:
    timestamp = db.Column(db.DateTime, default=datetime.now) 
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'))

with app.app_context():
    db.create_all()

# --- 2. HTML TEMPLATES ---
LOGIN_HTML = '''
<body style="font-family: sans-serif; text-align: center; padding-top: 100px; background: #f0f2f5;">
    <div style="display: inline-block; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        <h2 style="color: #004a99;">🏦 Nsongwa Credit Union</h2>
        <form method="POST" action="/login">
            <input type="text" name="user_id" placeholder="Member ID" required style="display: block; width: 200px; margin: 10px auto; padding: 10px; border: 1px solid #ccc; border-radius: 5px;"><br>
            <input type="password" name="pin" placeholder="Secret PIN" required style="display: block; width: 200px; margin: 10px auto; padding: 10px; border: 1px solid #ccc; border-radius: 5px;"><br>
            <button type="submit" style="background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%;">Login</button>
        </form>
        <p>New member? <a href="/register">Create Account</a></p>
    </div>
</body>
'''

REGISTER_HTML = '''
<body style="font-family: sans-serif; text-align: center; padding-top: 100px; background: #f0f2f5;">
    <div style="display: inline-block; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        <h2 style="color: #28a745;">📝 Join Union</h2>
        <form method="POST">
            <input type="text" name="name" placeholder="Full Name" required style="display: block; width: 200px; margin: 10px auto; padding: 10px; border: 1px solid #ccc; border-radius: 5px;"><br>
            <input type="text" name="user_id" placeholder="ID (e.g. 1001)" required style="display: block; width: 200px; margin: 10px auto; padding: 10px; border: 1px solid #ccc; border-radius: 5px;"><br>
            <input type="password" name="pin" placeholder="PIN" required style="display: block; width: 200px; margin: 10px auto; padding: 10px; border: 1px solid #ccc; border-radius: 5px;"><br>
            <button type="submit" style="background: #28a745; color: white; border: none; padding: 10px 20px; border-radius: 5px; width: 100%;">Register</button>
        </form>
    </div>
</body>
'''

DASHBOARD_HTML = '''
<body style="font-family: sans-serif; background: #f0f2f5;">
    <div style="max-width: 600px; margin: 30px auto; background: white; padding: 40px; border-radius: 10px; border-top: 10px solid #28a745; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h2>🏦 Nsongwa Credit Union <br><small>Welcome, {{ name }}!</small> <span style="float:right; font-size:0.5em; background:#eee; padding:5px; border-radius:5px;">ID: {{ uid }}</span></h2>
        <hr>
        <h1 style="color: #28a745; text-align: center;">{{ "{:,.0f}".format(balance) }} XAF</h1>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
            <div style="background: #fff9e6; padding: 15px; border-radius: 8px; border: 1px solid #ffeeba;">
                <strong>📱 MoMo Deposit</strong>
                <form action="/deposit" method="POST">
                    <input type="number" name="amount" placeholder="Amount" required style="width:90%; margin: 10px 0; padding:8px;">
                    <button type="submit" style="background:#ffcc00; border:none; padding:10px; width:100%; border-radius:5px; cursor:pointer;">Deposit</button>
                </form>
            </div>
            <div style="background: #f8d7da; padding: 15px; border-radius: 8px; border: 1px solid #f5c6cb;">
                <strong>💸 Withdrawal</strong>
                <form action="/withdraw" method="POST">
                    <input type="number" name="amount" placeholder="Amount" required style="width:90%; margin: 10px 0; padding:8px;">
                    <button type="submit" style="background:#dc3545; color:white; border:none; padding:10px; width:100%; border-radius:5px; cursor:pointer;">Withdraw</button>
                </form>
            </div>
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h4>Recent Activity</h4>
            <a href="/download_statement" style="font-size: 0.8em; text-decoration:none;">📥 Download Statement</a>
        </div>
        
        <ul style="list-style: none; padding: 0; max-height: 200px; overflow-y: auto; border: 1px solid #eee; padding: 10px; border-radius: 5px;">
            {% for tx in transactions|reverse %}
            <li style="border-bottom: 1px solid #eee; padding: 10px 0; display: flex; justify-content: space-between;">
                <span>
                    <strong>{{ tx.type }}</strong> <br>
                    <small style="color: #888;">{{ tx.timestamp.strftime('%b %d, %H:%M') }}</small>
                </span>
                <span style="font-weight:bold; color: {{ '#28a745' if tx.type == 'Deposit' else '#dc3545' }};">
                    {{ '+' if tx.type == 'Deposit' else '-' }}{{ "{:,.0f}".format(tx.amount) }}
                </span>
            </li>
            {% endfor %}
        </ul>
        <p style="text-align: center; margin-top: 20px;"><a href="/logout" style="color: #dc3545; text-decoration: none; font-size: 0.9em;">Logout Securely</a></p>
    </div>
</body>
'''

# --- 3. ROUTES ---
@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return render_template_string(DASHBOARD_HTML, name=user.name, balance=user.balance, uid=user.id, transactions=user.transactions)
    return render_template_string(LOGIN_HTML)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uid, name, pin = request.form.get('user_id'), request.form.get('name'), request.form.get('pin')
        hashed = hashlib.sha256(pin.encode()).hexdigest()[:12]
        new_user = User(id=uid, name=name, pin_hash=hashed, balance=0.0)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template_string(REGISTER_HTML)

@app.route('/login', methods=['POST'])
def login():
    uid, pin = request.form.get('user_id'), request.form.get('pin')
    user = db.session.get(User, uid)
    if user and hashlib.sha256(pin.encode()).hexdigest()[:12] == user.pin_hash:
        session['user_id'] = uid
        return redirect(url_for('index'))
    return "Login Failed. <a href='/'>Try again</a>", 401

@app.route('/deposit', methods=['POST'])
def deposit():
    user = User.query.get(session['user_id'])
    amt = float(request.form.get('amount'))
    user.balance += amt
    db.session.add(Transaction(type="Deposit", amount=amt, owner=user))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/withdraw', methods=['POST'])
def withdraw():
    user = User.query.get(session['user_id'])
    amt = float(request.form.get('amount'))
    if amt <= user.balance:
        user.balance -= amt
        db.session.add(Transaction(type="Withdrawal", amount=amt, owner=user))
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/download_statement')
def download_statement():
    user = User.query.get(session['user_id'])
    output = io.StringIO()
    output.write(f"Nsongwa Statement: {user.name}\n" + "="*30 + "\n")
    for tx in user.transactions:
        output.write(f"{tx.timestamp.strftime('%Y-%m-%d %H:%M')} | {tx.type}: {tx.amount} XAF\n")
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    return send_file(mem, mimetype='text/plain', as_attachment=True, download_name=f'statement_{user.id}.txt')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Register Blueprints Once
from api import api_bp
from momo_api import momo_bp
app.register_blueprint(api_bp)
app.register_blueprint(momo_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# Register MoMo API

# Register APIs

