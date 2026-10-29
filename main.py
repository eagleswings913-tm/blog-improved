from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor = CKEditor(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

class NewBlogForm(FlaskForm):
    blog_title = StringField('blog_title', validators=[DataRequired()])
    blog_subtitle = StringField('blog_subtitle', validators=[DataRequired()])
    blog_author = StringField('blog_author', validators=[DataRequired()])
    blog_img_url = StringField('blog_img_url', validators=[DataRequired()])
    blog_content = TextAreaField('blog_content', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@app.route('/',methods=['GET'])
def get_all_posts():
    result = db.session.execute(db.select(BlogPost).order_by(BlogPost.date))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)

@app.route('/show_post/<int:post_id>',methods=['GET'])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)

# TODO: add_new_post() to create a new blog post
@app.route("/new_post", methods=["GET","POST"])
def new_post():
    form = NewBlogForm()
    if request.method == 'GET':
        return render_template("make-post.html", form=form)
    else:
        return "Form Submitted"

# TODO: edit_post() to change an existing blog post

# TODO: delete_post() to remove a blog post from the database

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
