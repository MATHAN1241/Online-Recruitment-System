from flask import Flask,render_template,redirect,url_for,request,session,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "made by humans"
app.permanent_session_lifetime = timedelta(days=7)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cms.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#Database Mapper
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(50),unique=True,nullable=False)
    fname = db.Column(db.String(20),nullable=True,default=None)
    lname = db.Column(db.String(20))
    pswd = db.Column(db.String(50),nullable=False,default=None)
    author = db.Column(db.String(40),nullable=True,default=None)
    title = db.Column(db.String(25),nullable=True,default=None)
    keywords = db.Column(db.String(100),nullable=True,default=None)
    paper = db.Column(db.String(550),nullable=True,default=None)
    comments = db.Column(db.String(550),nullable=True,default=None)
    status = db.Column(db.String(15),nullable=True,default=None)
    avenue = db.Column(db.String(40),nullable=True,default=None)
    timing = db.Column(db.String(40),nullable=True,default=None)
    hall = db.Column(db.Integer,nullable=True,default=None)


    def __init__(self,email,fname,lname,pswd,author,title,keywords,paper,comments,status,avenue,timing):
        self.email = email
        self.fname = fname
        self.lname = lname
        self.pswd = pswd
        self.author = author
        self.title =title
        self.keywords = keywords
        self.paper = paper
        self.comments = comments
        self.status = status
        self.avenue = avenue
        self.timing = timing
        

#Home Page
@app.route('/',methods = ["POST","GET"])
def home():
    if ("email" in session) and ("pswd" in session) and (session["pswd"] == User.query.filter_by(email = session["email"]).first().pswd ) :
        flash("Logged In Successfull")
        return render_template('home.html',user = User.query.filter_by(email=session["email"]).first())
    else:
        return redirect(url_for('login'))
#User Login Page
@app.route('/login',methods = ["POST","GET"])
def login():
    if request.method =="POST":
        email = request.form['email']
        pswd = request.form['pswd']
        
        if ((User.query.filter_by(email=email).first().email == email) and (User.query.filter_by(email=email).first().pswd == pswd)):
            session["email"] = User.query.filter_by(email=email).first().email
            session["pswd"] = User.query.filter_by(email=email).first().pswd
            
            session["admin"] = False
            if request.form.get('check') == "remember":
                session.permanent = True
            else:
                session.permanent = False
        else:
            flash("Incorrect Credentials")
        
        return redirect(url_for('home'))
    else:
        if ("email" in session) and ("pswd" in session) and (session["admin"]==False):
            flash("Already Logged In")
            return redirect(url_for('home'))
        return render_template('Login.html')

#Submit Paper Section Rout
@app.route('/submitPaper',methods = ["POST","GET"])
def submitPaper():
    if request.method =="POST":
        session["admin"] = False
        if (request.form['First Name'] and request.form['Last Name'] and request.form['Paper']):
            First Name = request.form['First Name']
            Last Name = request.form['Last Name']
            Keywords = request.form['Keywords']
            Paper = request.form['Paper']
        else:
            flash("Enter All Details")
            return redirect(url_for('submitPaper'))
        if User.query.filter_by(email=session["email"]).first():
            User.query.filter_by(email=session["email"]).first().author = Author
            User.query.filter_by(email=session["email"]).first().title = Title
            User.query.filter_by(email=session["email"]).first().paper = Paper
            User.query.filter_by(email=session["email"]).first().keywords = Keywords
            User.query.filter_by(email=session["email"]).first().comments = None
            User.query.filter_by(email=session["email"]).first().status = "In Progress"
            User.query.filter_by(email=session["email"]).first().avenue = None
            User.query.filter_by(email=session["email"]).first().timing = None
            User.query.filter_by(email=session["email"]).first().hall = None
            db.session.commit()
            return redirect(url_for('submitPaper'))
    else:
        session["admin"] = False
        if ("email" in session) and ("pswd" in session) and (session["pswd"] == User.query.filter_by(email=session["email"]).first().pswd):
            return render_template('submitPaper.html',user = User.query.filter_by(email=session["email"]).first())
        else:
            return redirect(url_for('login'))

#Delete Paper Logic
@app.route('/deletePaper')
def deletePaper():
    if User.query.filter_by(email=session["email"]).first():
        User.query.filter_by(email=session["email"]).first().author = None
        User.query.filter_by(email=session["email"]).first().title = None
        User.query.filter_by(email=session["email"]).first().paper = None
        User.query.filter_by(email=session["email"]).first().keywords = None
        User.query.filter_by(email=session["email"]).first().comments = None
        User.query.filter_by(email=session["email"]).first().status = None
        User.query.filter_by(email=session["email"]).first().avenue = None
        User.query.filter_by(email=session["email"]).first().timing = None
        User.query.filter_by(email=session["email"]).first().hall = None
        
        db.session.commit()    
    return redirect(url_for('submitPaper'))

#Sign Up Page Route
@app.route('/signup',methods = ["POST","GET"])
def signup():
    if request.method =="POST":
        if (request.form['fname'] and request.form['email'] and request.form['pswd']):
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            pswd = request.form['pswd']
        else:
            flash("Enter All Details")
            return redirect(url_for('signup')) 

        if not User.query.filter_by(email=email).first():
            #print(fname+" "+lname+"\n"+email)  
            usr = User(email=email,fname=fname,lname=lname,pswd=pswd,author=None,title=None,keywords=None,paper=None,comments=None,status=None,avenue=None,timing=None)
            print(usr)
            db.session.add(usr)
            db.session.commit() 
            flash(User.query.filter_by(email=email).first().email+" added successfully")
            return redirect(url_for('login'))  
        else:
            flash("User already Exist") 
            return redirect(url_for('signup'))      
    else:
        return render_template('signup.html')
@app.route('/resetpassword',methods = ["POST","GET"])

#Reset Password Logic
def reset():
    if request.method =="POST":
        if (request.form['email'] and request.form['npswd']):
            email = request.form['email']
            pswd = request.form['npswd']
        else:
            flash("Enter All Details")
            return redirect(url_for('reset')) 
        if User.query.filter_by(email=email).first():
            User.query.filter_by(email=email).first().pswd = pswd
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash("User Not Exist") 
            return redirect(url_for('reset'))
    else:
        return render_template('resetpassword.html')

#Admin Login Page Route
@app.route('/admin/login',methods = ["POST","GET"])
def adminLogin():
    if request.method =="POST":
        email = request.form['email']
        pswd = request.form['pswd']
        
        if (email == "nithinton@gmail.com") and (pswd == "12345"):
            session["adminEmail"] = email
            session["adminPswd"] = pswd
            return redirect(url_for('admin'))
        else:
            flash("Incorrect Credentials")        
            return redirect(url_for('adminLogin'))
    else:
        if ("adminEmail" in session) and ("adminPswd" in session):
            if (session["adminEmail"]== 'nithinton@gmail.com' and session["adminPswd"] == '12345'):
                flash("Already Logged In")
                return redirect(url_for('admin'))
        return render_template('adminlogin.html')

#Admin Page Route
@app.route('/admin',methods = ["POST","GET"])
def admin():
    if request.method =="POST":
        comments = request.form['Comments']

        avenue = request.form['avenue']
        hall = request.form['hall']
        timing= request.form['timing']

        Id = request.form['Id']
        try:
            if request.form['Accept'] == "Accept":
                User.query.filter_by(id=Id).first().comments = comments
                User.query.filter_by(id=Id).first().status = "Selected"
                User.query.filter_by(id=Id).first().avenue = avenue
                User.query.filter_by(id=Id).first().hall = hall
                User.query.filter_by(id=Id).first().timing = timing
                db.session.commit()
                return redirect(url_for('admin'))
        except:
            if request.form['Reject'] == "Reject":
                User.query.filter_by(id=Id).first().comments = comments
                User.query.filter_by(id=Id).first().status = "Rejected"
                User.query.filter_by(id=Id).first().avenue = None
                User.query.filter_by(id=Id).first().hall = None
                User.query.filter_by(id=Id).first().timing = None
                db.session.commit()
                return redirect(url_for('admin'))
    else:
        if ("adminEmail" in session) and ("adminPswd" in session):
            if (session["adminEmail"] == 'nithinton@gmail.com' and session["adminPswd"] == '12345'):
                flash("Logged In Successfull")
                count = 0
                for user in User.query.all():
                    if user.author and user.title and user.paper:
                        count = count + 1
                Data = {
                    "users": User.query.all(),
                    "papers": count,
                    "selected": len(User.query.filter_by(status="Selected").all()),
                    "rejected": len(User.query.filter_by(status="Rejected").all()),
                    "pending": len(User.query.filter_by(status="In Progress").all()),
                }
                return render_template('adminPortal.html',data = Data)
        else:
            return redirect(url_for('adminLogin'))

#Winners Page Route
@app.route('/winners',methods = ["POST","GET"])
def winners():
    if request.method =="POST":
        pass
    else:
        return render_template('winners.html')
        
#Logout Logic
@app.route('/logout')
def logout():
    session.pop("email",None)
    session.pop("pswd",None)
    flash("logged Out Successfull")
    return redirect(url_for('login'))

@app.route('/admin/logout')
def adminlogout():
    session.pop("adminEmail",None)
    session.pop("adminPswd",None)
    flash("Admin logged Out Successfull")
    return redirect(url_for('adminLogin'))



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)