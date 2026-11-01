from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.file import FileRequired, FileAllowed
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
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
    blog_title = StringField('Blog Post Title', validators=[DataRequired()])
    blog_subtitle = StringField('Blog Post Subtitle', validators=[DataRequired()])
    blog_author = StringField('Post Author', validators=[DataRequired()])
    blog_img_url = StringField('Blog Post Image URL')
    # blog_image = FileField('Blog Post Image', validators=[FileRequired(), FileAllowed(['jpg'])])
    blog_content = TextAreaField('Blog Post Content', validators=[DataRequired()])
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
        blog_title = form.blog_title.data
        blog_subtitle = form.blog_subtitle.data
        blog_author = form.blog_author.data
        blog_img_url = form.blog_img_url.data
        if blog_img_url:
            blog_img_url = 'assets/img/' + blog_img_url
        else:
            blog_img_url = 'assets/img/default.jpg'
        image_url = url_for('static', filename=blog_img_url)
        blog_content = form.blog_content.data
        today = date.today().strftime("%B %d, %Y")
        new_blog_post = BlogPost(title=blog_title, subtitle=blog_subtitle, author=blog_author, img_url=image_url, body=blog_content, date=today)
        db.session.add(new_blog_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))

# TODO: edit_post() to change an existing blog post
@app.route("/edit_post/<int:post_id>",methods=['GET','POST'])
def edit_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    edit_form = NewBlogForm(
        blog_title=requested_post.title,
        blog_subtitle=requested_post.subtitle,
        blog_author=requested_post.author,
        blog_img_url=requested_post.img_url,
        blog_content=requested_post.body
    )
    if edit_form.validate_on_submit():
        requested_post.title = edit_form.blog_title.data or requested_post.title
        requested_post.subtitle = edit_form.blog_subtitle.data or requested_post.subtitle
        requested_post.author = edit_form.blog_author.data or requested_post.author
        requested_post.img_url = edit_form.blog_img_url.data or requested_post.img_url
        # requested_post.image_url = url_for('static', filename=img_url)
        requested_post.body = edit_form.blog_content.data or requested_post.body
        db.session.commit()
        return redirect(url_for('show_post', post_id=requested_post.id))
    return render_template("make-post.html", form=edit_form, action="edit")

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
