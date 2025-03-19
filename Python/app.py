from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Cấu hình database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Model người dùng
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=0.0)

# Model email Yahoo
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_sold = db.Column(db.Boolean, default=False)

# Model giao dịch
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    email_id = db.Column(db.Integer, db.ForeignKey('email.id'), nullable=False)
    status = db.Column(db.String(50), default='completed')

# Đăng ký người dùng
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Tên đăng nhập đã tồn tại'}), 400
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Đăng ký thành công'}), 201

# Đăng nhập người dùng
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Đăng nhập thành công', 'balance': user.balance})
    return jsonify({'message': 'Sai tài khoản hoặc mật khẩu'}), 401

# Lấy danh sách email Yahoo chưa bán
@app.route('/emails', methods=['GET'])
def get_emails():
    emails = Email.query.filter_by(is_sold=False).all()
    return jsonify([{'id': e.id, 'email': e.email, 'price': e.price} for e in emails])

# Xử lý mua email Yahoo
@app.route('/buy', methods=['POST'])
def buy_email():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    email = Email.query.filter_by(id=data['email_id'], is_sold=False).first()
    
    if not user or not email:
        return jsonify({'message': 'Người dùng hoặc email không tồn tại'}), 400
    
    if user.balance < email.price:
        return jsonify({'message': 'Số dư không đủ'}), 400
    
    user.balance -= email.price
    email.is_sold = True
    transaction = Transaction(user_id=user.id, email_id=email.id)
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({'message': f'Bạn đã mua {email.email}', 'new_balance': user.balance})

# Nạp tiền vào tài khoản
@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    
    if not user:
        return jsonify({'message': 'Người dùng không tồn tại'}), 400
    
    user.balance += data['amount']
    db.session.commit()
    
    return jsonify({'message': 'Nạp tiền thành công', 'new_balance': user.balance})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
