from flask import render_template, request, Blueprint
from flaskblog.models import Post
from flask_login import login_required
from flask_paginate import Pagination, get_page_args

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


@main.route("/")
def syllabus():
    return render_template('syllabus.html', title='Syllabus')


users = lectu


def get_users(offset=0, per_page=1):
    return users[offset: offset + per_page]


@main.route("/lectures")
@login_required
def lectures():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(users)
    pagination_users = get_users(offset=1, per_page=1)
    pagination = Pagination(page=page, per_page=1, total=total,
                            css_framework='bootstrap4')
    return render_template('lectures.html',
                           users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )
