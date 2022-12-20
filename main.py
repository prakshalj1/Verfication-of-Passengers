
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from pyzbar.pyzbar import decode
import cv2
import qrcode
import pyqrcode
import time
import png
from pyqrcode import QRCode
import webbrowser






app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #track and emit
app.config['PROPAGATE_EXCEPTIONS'] = True #error handler
db = SQLAlchemy(app)
app.app_context().push()





class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))





@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]

        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            cap=cv2.VideoCapture(0)
            cap.set(5,640)
            cap.set(6,480)

            while True:
                _,img=cap.read()
                for i in decode(img):
                    k=i.data.decode('utf-8')
                    if k == uname:
                        return render_template("access granted.html")
                    else:
                        return render_template("access denies.html")
                    time.sleep(3)

                    # k=user.query.filter_by(username=a).first()
                    # if a == k :
                    #     print('access granted')
                    #     break




                cv2.imshow('Scanner app',img)


                cv2.waitKey(2)


            # b=webbrowser.open(str(a))



            # return redirect(url_for("index"))


    return render_template("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username=uname, email=mail, password=passw)
        db.session.add(register)
        db.session.commit()

        pic=f'{uname}'
        dpic=pyqrcode.create(pic)
        dpic.png(f'{uname}.png',scale=6)



        # img=qrcode.make(f"{uname}")
        # img.save(f"{uname}.jpg")
        # img = cv2.imread(r'C:\Users\parth\minor_project2\prakshal216.jpg')
        # print(decode(img))

        return ("Qr Code generated")

        # return redirect(url_for("login"))
    return render_template("register.html")


if __name__ == "__main__":
    db.create_all()



    app.run(debug=True)
