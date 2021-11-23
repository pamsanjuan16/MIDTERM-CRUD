# Add to this file for the sample app lab
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
 

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template('login.html')
    



#@app.route("/login", methods =['GET', 'POST'])
#def login():
#    if request.method == 'POST':
#        user=request.form.get("user")
#        password=request.form.get("pass")
#        confirm=request.form.get("confirm")
#        return redirect(url_for('/index'))
#        return render_template('login.html')
   
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
