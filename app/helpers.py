from HTMLParser import HTMLParser
import os
import bottle
from functools import wraps
from app import env, config
from helput import unique_filename


def view(tpl_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tplvars = func(*args, **kwargs)
            template = env.get_template(tpl_name)
            if tplvars is not None:
                return template.render(**tplvars)
            else:
                return template.render()
        return wrapper
    return decorator

def only_ajax(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if bottle.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return func(*args, **kwargs)
        return bottle.abort(404)
    return decorated


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def shorten_text(text):
    text = strip_tags(text)
    if len(text) > 500:
        text = text[:500] + "..."
    return text


def postd():
    return bottle.request.forms


def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()


def redirect(where=None):
    if where is not None:
        return bottle.redirect(where)
    """
    back=None
    if hasattr(bottle.request.headers, 'Referer'):
        back = bottle.request.headers['Referer']
    print('refferer:', back)
    if back is not None:
        return bottle.redirect(back)
    """
    return bottle.redirect('/')


def save_file(file_obj, where='uploaded'):
    """
    Saves file to where directory on the server
    """
    #todo: check for errors, types or file_obj properties
    folder = os.path.join(config.ROOT_FOLDER, where)
    new_filename = unique_filename(file_obj.filename)
    file_path = os.path.join(folder, new_filename)
    with open(file_path, 'wb') as open_file:
        open_file.write(file_obj.file.read())
    return new_filename  # returns new filename
    # ? returns relative to browser path to file
