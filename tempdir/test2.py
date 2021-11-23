from flask import Flask,request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sqlite3 as sql
from flask import render_template

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Users(db.Model):
    __tablename__ = "Users"
    user_id = db.Column(db.String(50), primary_key = True)
    user_name = db.Column(db.String(50))
    user_username = db.Column(db.String(50))
    user_password = db.Column(db.String(50))

    def __init__(self, user_id, user_name, user_username, user_password):
        self.user_id = user_id
        self.user_name = user_name
        self.user_username = user_username
        self.user_password = user_password

class UsersMeta(ma.Schema):
    class Meta:
        fields = ("user_id", "user_name", "user_name", "user_password")
    
user_meta = UsersMeta()
users_meta = UsersMeta(many=True)

#
@app.route("/")
def main():
    return render_template("index.html")

#

#SignUp #CREATE

@app.route("/#Signup", methods=['GET', 'POST'])
def Signup():
    if request.method == 'POST':
        user_fname = request.form.get("user_name")
        user_uname = request.form.get("user_username")
        user_pw = request.form.get("user_password")
        user_confirmpw = request.form.get("user_confirmpw")

        print(user_fname, user_uname, user_pw, user_confirmpw, (user_pw == user_confirmpw))

        if user_fname == "" or user_uname == "" or user_pw == "" or user_confirmpw == "":
            print("Empty fields")
            return redirect(url_for('main'))
        elif(user_pw != user_confirmpw):
            print("Password doesn't match")
            
        else: 
            print("Success")
            new_users = Users(user_fname, user_uname, user_pw)
            db.session.add(new_users)
            db.session.commit()
            return redirect(url_for('login'))
            return user_schema.jsonify(new_users)
    
    return render_template("login.html")

#Login
@app.route("/login", methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_username2 = request.form["username"]
        user_password2 = request.form["password"]

        con = sql.connect("Users.db")
        con.row_factory = sql.Row

        cur = con.cursor()

        cur.execute("select * from user where user_username ='{}' and user_password='{}';".format(user_username2, user_password2))

        user = cur.fetchone()

        if user is None:
            return render_template("login.html")
            
        else:
            if (len(user) > 0):
                return redirect(url_for("main"))

    return render_template("login.html")

#SUBJECT TO CHANGE '/'
#READ
#MULTIPLE USERS

@app.route('/users', methods =['GET'])
def read_all():
    users = Users.query.all()
    result = Users_Schema.dump(users)
    
    return Users_Schema.jsonify(result).data

#SUBJECT TO CHANGE '/'
#READ
#SINGLE USER

@app.route('/users/<user_id>', methods =['GET'])
def read_user(user_id):
    user = Users.query.get(user_id)
    result = User_Schema.dump(user)

    return User_Schema.jsonify(result)


#SUBJECT TO CHANGE '/'
#UPDATE

@app.route('/users/<user_id>', methods =['PUT'])
def update_username(user_username):
    user = Users.query.get(user_id)
    user_username = request.json.get('user_username')
    user_firstname = request.json.get('user_firstname')
    user_password = request.json.get('user_password')

    user.user_name = user_username
    user.user_firstname = user_firstname
    user.user_password = user_password

    db.session.commit()

    return User_Schema.jsonify(user)


#SUBJECT TO CHANGE '/'
#DELETE

@app.route('/users/<user_username>', methods = ['GET', 'POST'])
def delete_user(user_username):
    user = Users.query.get(user_username)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return User_Schema.jsonify(user)

    return render_template('delete.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)