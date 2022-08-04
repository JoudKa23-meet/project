from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase
app = Flask(__name__, template_folder="templates", static_folder="statics")

config = {
  "apiKey": "AIzaSyA63JulIUqGmYGI9Ga2eWfccYlpvHYaztg",
  "authDomain": "dating-website-47d57.firebaseapp.com",
  "projectId": "dating-website-47d57",
  "storageBucket": "dating-website-47d57.appspot.com",
  "messagingSenderId": "504034470000",
  "appId": "1:504034470000:web:2ba9ed6b361d5c5cbf2cb5",
  "measurementId": "G-NJZQR1748N",
  "databaseURL":"https://dating-website-47d57-default-rtdb.europe-west1.firebasedatabase.app/"
}

app.config['SECRET_KEY'] = 'super-secret-key'
firebase = pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

@app.route('/', methods=['GET','POST'])
def login():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)              
        try:
            
            return redirect(url_for('index'))
        except:
            error = "Authentication failed"
    print(error)
    return render_template('login.html')
 
@app.route('/signup', methods=['GET','POST'])
def signup():
    error = ""
    if request.method == 'POST' and request.form['signup_password']==request.form['repeat_password']:
        username=request.form['signup_username']
        email = request.form['email']
        password = request.form['signup_password']
        repeat_password=request.form['repeat_password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('index'))
        except:
            error = "Authentication failed"
    return render_template("login.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/rock')
def rock():
    # db.child("Users").child(login_session['user']['localId']).
    return render_template("rock.html")

@app.route('/favorite/<string:name>',)
def favorite(name):
    error=''
    try:
        db.child("Users").child(login_session['user']['localId']).child('songs').update({name:True})
        return redirect(url_for('favorites'))
    except:
        error="jfdkls"
    return render_template("rock.html")

@app.route('/favorites')
def favorites():
    error=''
    try:
        songs=db.child("Users").child(login_session['user']['localId']).child('songs').get().val()
        return redirect(url_for('abc'))
    except:
        error="fdsf"
    return render_template('favorite.html', songs=songs)

@app.route('/abc')
def abc():
    return render_template('favorite.html')

if __name__ == "__main__":
    app.run(debug = True)