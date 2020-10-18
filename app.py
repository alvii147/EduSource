from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from ocr import getString

app = Flask(__name__)
app.secret_key = "c9l3n5b1"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    fname = db.Column(db.String(150))
    lname = db.Column(db.String(150))
    email = db.Column(db.String(150))
    pword = db.Column(db.String(150))
    uni = db.Column(db.String(150))
    psets = db.relationship("Pset", backref = "user")

    def __init__(self, fname, lname, email, pword, uni):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.pword = pword
        self.uni = uni

class Pset(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(150))
    course = db.Column(db.String(150))
    desc = db.Column(db.String(5000))
    questions = db.relationship("Question", backref = "question")

    def __init__(self, userid, name, course, desc):
        self.userid = userid
        self.name = name
        self.course = course
        self.desc = desc

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    psetid = db.Column(db.Integer, db.ForeignKey("pset.id"))
    description = db.Column(db.String(5000))
    notes = db.Column(db.String(5000))
    answers = db.relationship("Answer", backref = "answer")

    def __init__(self, psetid, description):
        self.psetid = psetid
        self.description = description

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    questionid = db.Column(db.Integer, db.ForeignKey("question.id"))
    ans = db.Column(db.String(150))
    kudos = db.Column(db.Integer)

    def __init__(self, questionid, ans, kudos):
        self.questionid = questionid
        self.ans = ans
        self.kudos = kudos


@app.route("/")
def home():
    if "email" in session:
        fname = session["fname"]
        lname = session["lname"]
        email = session["email"]
        foundUser = User.query.filter_by(email = email).first()
        return render_template("home.html", fname = fname, lname = lname, email = email, psets = foundUser.psets)
    else:
        return redirect(url_for("login"))

@app.route("/login/", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["em"]
        pword = request.form["pw"]
        
        foundUser = User.query.filter_by(email = email).first()
        if foundUser:
            if pword == foundUser.pword:
                session["fname"] = foundUser.fname
                session["lname"] = foundUser.lname
                session["email"] = foundUser.email
                return redirect(url_for("home"))
            else:
                flash("Incorrect email or password!")
                return redirect(url_for("login"))
        else:
            flash("Incorrect email or password!")
            return redirect(url_for("login"))
    else:
        return render_template("login.html")

@app.route("/signup/", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        fname = request.form["fn"]
        lname = request.form["ln"]
        email = request.form["em"]
        pword = request.form["pw"]
        rpword = request.form["rpw"]
        uni = request.form["uni"]

        if pword != rpword:
            flash("Passwords do not match!", "error")
            return redirect(url_for("signup"))
        
        foundUser = User.query.filter_by(email = email).first()
        if foundUser:
            flash("An account already exists under this email!")
        
        newuser = User(fname, lname, email, pword, uni)
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return render_template("signup.html")

@app.route("/newpset/", methods = ["GET", "POST"])
def newpset():
    if not "email" in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["nm"]
        course = request.form["cs"]
        description = request.form["ds"]
        
        foundUser = User.query.filter_by(email = session["email"]).first()
        newpset = Pset(foundUser.id, name, course, description)
        db.session.add(newpset)
        foundUser.psets.append(newpset)
        db.session.commit()
        return redirect(url_for("pset", pset_id = newpset.id))
    return render_template("newpset.html")

@app.route("/pset<pset_id>/", methods = ["GET", "POST"])
def pset(pset_id):
    foundPset = Pset.query.filter_by(id = pset_id).first()
    foundUser = User.query.filter_by(id = foundPset.userid).first()
    if request.method == "POST":
        if "ds" in request.form:
            desc = request.form["ds"]
            newquestion = Question(pset_id, desc)
            db.session.add(newquestion)
            foundPset.questions.append(newquestion)
            db.session.commit()
        if "an" in request.form:
            ans = request.form["an"]
    return render_template("pset.html", userfname = foundUser.fname, userlname = foundUser.lname, name = foundPset.name, course = foundPset.course, desc = foundPset.desc, questions = foundPset.questions)

@app.route("/pset<pset_id>/question<question_id>/", methods = ["GET", "POST"])
def newanswer(pset_id, question_id):
    if request.method == "POST":
        foundQuestion = Question.query.filter_by(id = question_id).first()
        ans = request.form["an"]
        newanswer = Answer(question_id, ans, 0)
        db.session.add(newanswer)
        foundQuestion.answers.append(newanswer)
        db.session.commit()
    return redirect(url_for("pset", pset_id = pset_id))

@app.route("/pset<pset_id>/answer<ans_id>/", methods = ["GET", "POST"])
def addkudos(pset_id, ans_id):
    foundAnswer = Answer.query.filter_by(id = ans_id).first()
    foundAnswer.kudos += 1
    db.session.commit()
    return redirect(url_for("pset", pset_id = pset_id))

@app.route("/equation/", methods = ["GET", "POST"])
def equation():
    if request.method == "POST":
        myfile = request.files["file"]
        if myfile.filename != '':
            myfile.save("static/img.jpg")
            ocrstr = getString()
            with open("eq.csv", "r") as readfile:
                lines = readfile.readlines()
            for i in range(len(lines)):
                if i == 0:
                    continue
                spl = lines[i].split(",")
                if spl[0] in ocrstr:
                    eq = spl[0]
                    fi = spl[1]
                    ds = spl[2]
                    break
            return render_template("equation.html", eq = eq, fi = fi, ds = ds)
    return render_template("equation.html", eq = "", fi = "", ds = "")

if __name__ == "__main__":
    db.create_all()
    app.run()