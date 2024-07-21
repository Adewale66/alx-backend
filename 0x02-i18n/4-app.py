from flask import Flask, render_template, request
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
    return render_template("4-index.html",
                           home_title=_("Welcome to Holberton"),
                           home_header=_("Hello world!"))


if __name__ == "__main__":
    app.run(debug=True)
