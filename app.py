from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import count
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password@localhost/height_collector'
db=SQLAlchemy(app)

## this is our database model 
class Data(db.Model):
    __tablename__ = "data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_= db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    # we want to capture the post values
    if request.method == 'POST':
        email=request.form["email_name"]
        height=request.form["height_name"]
      

        # we are querying our database model, filtering to see if values match
        if (db.session.query(Data).filter(Data.email_ == email).count() == 0):
            userinfo=Data(email, height)
            db.session.add(userinfo)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_).scalar())
            average_height=round(average_height, 1)
            count=db.session.query(Data.height_).count()
            # send email with statistics
            send_email(email, height, average_height, count)
            return render_template("success.html")

    return render_template('index.html', 
    text="Seems like we've got something from that email address already!")

if __name__ == '__main__':
    app.debug=True
    app.run()
