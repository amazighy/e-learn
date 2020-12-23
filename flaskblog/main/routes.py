import json
import urllib.request
from flask import render_template, request, Blueprint
from flaskblog.models import Post
from flask_login import login_required
from flask_paginate import Pagination, get_page_args

main = Blueprint('main', __name__)

with urllib.request.urlopen("https://raw.githubusercontent.com/amazighy/files/main/lectures.json") as url:
    data = json.loads(url.read().decode())
title = list(data.keys())
values = list(data.values())


def get_users(offset=0, per_page=1):
    return values[offset: offset + per_page]


@main.route("/lectures")
@login_required
def lectures():
    page, _, _ = get_page_args(page_parameter='page',
                               per_page_parameter='per_page')
    total = len(values)
    pagination = Pagination(page=page, per_page=1, total=total,
                            css_framework='bootstrap4')
    return render_template('lectures.html',
                           values=values,
                           page=page,
                           title=title,
                           pagination=pagination,

                           )


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
