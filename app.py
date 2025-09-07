from flask import Flask, request, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from time import sleep
import os

app = Flask(__name__)

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'mydatabase.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    message = db.Column(db.Text)
    services = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return f"<Request {self.firstname}, {self.lastname}, {self.email}, {self.phone}, {self.message}, {self.services}, {self.created_at}>"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password', '')
        sleep(0.5)
        if password == ADMIN_PASSWORD:
            requests = Request.query.order_by(Request.created_at.desc()).all()
            return render_template('admin.html', requests=requests)
        else:
            return render_template('login.html', error="Password errata")
    return render_template('login.html')


@app.route('/<string:name>')
def page(name):
    path = os.path.join(app.template_folder, f"{name}.html")
    if os.path.exists(path):
        return render_template(f"{name}.html")
    else:
        abort(404)

@app.route('/new_request', methods=['POST'])
def new_request():
    data = request.json
    services_list = data.get('services', [])
    services_str = ", ".join(services_list)
    record = Request(
        firstname=data.get('firstname', ''),
        lastname=data.get('lastname', ''),
        email=data.get('email', ''),
        phone=data.get('phone', ''),
        message=data.get('message', ''),
        services=services_str
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({"message": ""})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# COSE DA FARE
# 2 - adatta a smartphone !!!!!
# 4 - fai ultime schermate della home page !!!!!
