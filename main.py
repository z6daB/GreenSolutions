import flask

app = flask.Flask(__name__)


@app.route('/')
def start():
    return flask.render_template('start.html')


if __name__ == '__main__':
    app.run(debug=True)
