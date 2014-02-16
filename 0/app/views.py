from flask import render_template, url_for
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template("layout.html")

@app.route('/wtf')
def wtf():
    return url_for('static', filename='css/style.css')