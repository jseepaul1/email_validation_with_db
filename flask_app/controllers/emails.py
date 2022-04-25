from flask_app import app
from flask import render_template, redirect, request

from flask_app.models.email import Email


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/process', methods=['POST'])
def process():
    print("email-", request.form)
    if not Email.validate_email(request.form):
        return redirect('/')
    Email.save(request.form)
    return redirect('/results')


@app.route('/results')
def results():
    return render_template("success.html", emails=Email.get_all())


@app.route('/delete/<int:email_id>')
def delete(email_id):
    data = {
        'id': email_id,
    }
    print("data-", data)
    Email.destroy(data)
    return redirect('/results')
