import flask
from flask import Flask, render_template, redirect, request, make_response, abort
from data import db_session
from forms.user import RegisterForm, LoginForm
from data.users import User
from data.topic import Topic
from data.comment import Comment
from data.articles import Article
from sqlalchemy import orm
from flask_login import LoginManager, login_user, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('profile.html')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html')


@app.route('/forum', methods=['POST', 'GET'])
def forum():
    db_sess = db_session.create_session()
    if request.method == 'POST':
        topic = Topic(
            title=request.form['title'],
            description=request.form['description']
        )
        db_sess.add(topic)
        db_sess.commit()
    topics = db_sess.query(Topic).all()
    return render_template('forum.html', topics=topics)


@app.route('/forum/<int:id>', methods=['GET', 'POST'])
def topic(id):
    db_sess = db_session.create_session()
    if request.method == 'POST':
        if current_user.is_authenticated:
            user_name = current_user.name
        else:
            user_name = 'Anonymous'

        comment = Comment(
            user=user_name,
            text=request.form['comment'],
            topicId=id
        )
        db_sess.add(comment)
        db_sess.commit()
    topic = db_sess.query(Topic).filter(Topic.id == id).scalar()
    comments = db_sess.query(Comment).filter(Comment.topicId == id).all()
    return render_template('topic.html', topic=topic, comments=comments)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', user=current_user)
    else:
        abort(404)


@app.route('/blogs')
def blogs():
    db_sess = db_session.create_session()
    articles = db_sess.query(Article).all()
    return render_template('blogs.html', articles=articles)


@app.errorhandler(404)
def error404(error):
    return render_template('404.html')


def main():
    db_session.global_init('db/blogs.sqlite')
    app.run(debug=True, port=5001)


if __name__ == '__main__':
    main()
