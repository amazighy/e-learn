from flask import render_template, request, Blueprint
from flaskblog.models import Post
from flask_login import login_required
import requests

import requests
url = "https://raw.githubusercontent.com/amazighy/files/main/lectures.txt"
data = requests.get(url).content
data = data.decode("utf-8")
lectu = data.split("\n")
lectu.pop()


main = Blueprint('main', __name__)


@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/lectures")
@login_required
def lectures():
    return render_template('lectures.html', title='Lectures', lectu=lectu)


@main.route("/")
def syllabus():
    return render_template('syllabus.html', title='Syllabus')
