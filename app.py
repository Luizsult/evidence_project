from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evidence.db'
db = SQLAlchemy(app)


class Evidence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    number_case = db.Column(db.Integer, nullable=False)
    date_find = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Evidence %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        number_case = request.form['number_case']
        date_str = request.form['date_find']
        date_find = datetime.strptime(date_str, '%Y-%m-%d')

        evidence = Evidence(title=title, description=description, number_case=number_case, date_find=date_find)

        try:
            db.session.add(evidence)
            db.session.commit()
            return redirect('/catalog')
        except:
            return "При добавлении произошла ошибка"

    else:
        return render_template("index.html")


@app.route('/catalog')
def catalog():
    list = Evidence.query.order_by(Evidence.id.desc()).all()
    return render_template("catalog.html", list=list)


@app.route('/redact/<int:id>')
def redact(id):
    evidence_id = Evidence.query.get(id)
    return render_template("redact.html", evidence_id=evidence_id)


@app.route('/redact/<int:id>', methods=['POST', 'GET'])
def update(id):
    evidence_id = Evidence.query.get(id)
    if request.method == "POST":
        evidence_id.title = request.form['title']
        evidence_id.description = request.form['description']
        evidence_id.number_case = request.form['number_case']
        evidence_id.date_str = request.form['date_find']
        evidence_id.date_str = datetime.strptime(evidence_id.date_str, '%Y-%m-%d')

        try:
            db.session.commit()
            return redirect('/catalog')
        except:
            return "При редактировании произошла ошибка"

    else:
        return render_template("redact.html", evidence_id=evidence_id)


@app.route('/redact/<int:id>/del')
def delete(id):
    evidence_del = Evidence.query.get_or_404(id)

    try:
        db.session.delete(evidence_del)
        db.session.commit()
        return redirect('/catalog')
    except:
        return "При удалении произошла ошибка"


if __name__ == "__main__":
    app.run(debug=True)