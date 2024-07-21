from flask import g, Flask, render_template, request
from flask_babel import Babel
from flask_babel import gettext as _

app = Flask(__name__)


class Config(object):
    """Flask configs"""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(id):
    if id is None:
        return None
    for key in users:
        if int(id) == key:
            return users[key]
    return None


@app.before_request
def before_request():
    id = request.args.get("login_as")
    details = get_user(id)
    g.user = details


def get_locale():
    lang = request.args.get("locale")
    if lang is not None:
        languages = lang.replace("[", "").replace("]", "").split("|")
        for language in languages:
            if language in Config.LANGUAGES:
                return language
        return request.accept_languages.best_match(app.config['LANGUAGES'])
    return request.accept_languages.best_match(app.config['LANGUAGES'])


babel.init_app(app, locale_selector=get_locale)


@app.route("/")
def hello():
    user = getattr(g, 'user', None)
    return render_template("5-index.html",
                           home_title=_("Welcome to Holberton"),
                           home_header=_("Hello world!"),
                           user=user)


if __name__ == "__main__":
    app.run(debug=True)
