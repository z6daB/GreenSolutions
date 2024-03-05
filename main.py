from flask import Flask, render_template
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


def main():
    db_session.global_init('db/blogs.sqlite')
    app.run(debug=True, port=5001)


if __name__ == '__main__':
    main()
