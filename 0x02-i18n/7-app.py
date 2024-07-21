from flask import g, Flask, render_template, request
from flask_babel import Babel
from flask_babel import gettext as _
import pytz

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


def parse_accept_language(accept_language):
    if not accept_language:
        return []
    languages = []
    for lang in accept_language.split(','):
        parts = lang.split(';')
        languages.append(parts[0].strip())
    return languages


def get_locale_query(lang):
    if lang is None:
        return None
    languages = lang.replace("[", "").replace("]", "").split("|")
    for language in languages:
        if language in Config.LANGUAGES:
            return language
    return None


def get_supported_lang(headers):
    if headers is None:
        return None
    for header in headers:
        if header in Config.LANGUAGES:
            return header
    return None


def verify_timezone(zone):
    if zone is None:
        return None
    try:
        time = pytz.timezone(zone)
        return time
    except pytz.exceptions.UnknownTimeZoneError:
        return None


@app.before_request
def before_request():
    id = request.args.get("login_as")
    details = get_user(id)
    g.user = details


def get_locale():
    locale = get_locale_query(request.args.get("locale"))
    if locale is not None:
        return locale
    user = getattr(g, 'user', None)
    if user is not None:
        return user['locale']
    header = parse_accept_language(request.headers.get("Accept-Language"))
    get_supported = get_supported_lang(header)
    if get_supported is not None:
        return get_supported
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_timezone():
    zone = verify_timezone(request.args.get("timezone"))
    if zone is not None:
        return zone
    user = getattr(g, 'user', None)
    if user is not None:
        user_time = verify_timezone(user['timezone'])
        if user_time is not None:
            return user_time
    return Config.BABEL_DEFAULT_TIMEZONE


babel.init_app(app, locale_selector=get_locale, timezone_selector=get_timezone)


@app.route("/")
def hello():
    user = getattr(g, 'user', None)
    return render_template("6-index.html",
                           home_title=_("Welcome to Holberton"),
                           home_header=_("Hello world!"),
                           user=user)


if __name__ == "__main__":
    app.run(debug=True)
