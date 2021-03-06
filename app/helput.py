# -*- coding: utf-8 -*-
import os
import uuid
from functools import reduce
from random import sample
from string import digits
from string import ascii_lowercase as letters

import six
from markdown import markdown
from six.moves import html_parser


class MLStripper(html_parser.HTMLParser):
    def __init__(self):
        if six.PY3:
            super(MLStripper, self).__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def get_list_of_files(directory, ext='', full_path=True):
    """
    Return list of files in directory specified
    :param directory: path to directory you want to perform search in. Not
    work with nested directories, just files that are present directly here
    :param ext: if set then only files with this extension will be matched
    :param full_path: if True that full path for each file will be as result
    :return: list of files that matched query
    """
    files = []
    for file_name in os.listdir(directory):
        if file_name.endswith(ext):
            file_path = os.path.join(directory, file_name) \
                if full_path else file_name
            files.append(file_path)
    return files


def get_files_under_dir(directory, ext='', case_sensitive=False):
    """
    Perform recursive search in directory to match files with one of the
    extensions provided
    :param directory: path to directory you want to perform search in.
    :param ext: list of extensions of simple extension for files to match
    :param case_sensitive: is case of filename takes into consideration
    :return: list of files that matched query
    """
    if isinstance(ext, (list, tuple)):
        allowed_exensions = ext
    else:
        allowed_exensions = [ext]

    if not case_sensitive:
        allowed_exensions = map(str.lower, allowed_exensions)

    result = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            check_filename = filename if case_sensitive else filename.lower()
            if any(map(check_filename.endswith, allowed_exensions)):
                result.append(filename)
    return result


def get_all_dirs(directory, full_path=True):
    dirs = []
    for file_name in os.listdir(directory):
        path = os.path.join(directory, file_name)
        if os.path.isdir(path):
            dirs.append(path) if full_path else dirs.append(file_name)
    return dirs


def join_all_path(path):
    # todo: make it normpath
    if isinstance(path, (list, tuple)):
        return reduce(os.path.join, path)
    else:
        raise ValueError('Give the list of folders to join')


def unique_filename(filename):
    """
    The same files have the same filenames
    """
    if six.PY2:
        filename = filename.encode('utf-8')
    name, ext = os.path.splitext(filename)
    new_name = uuid.uuid3(uuid.NAMESPACE_OID, filename).hex
    return new_name + ext


def generate_filename(prefix='', suffix='', length=5):
    """
    Generate random filename with given parameters
    """
    chars = letters + digits
    f_name = ''.join(sample(chars, length))
    return '{prefix}{f_name}{suffix}'.format(prefix=prefix, f_name=f_name,
                                             suffix=suffix)


def distort_filename(filename):
    """
    Generate modified filename based on the original filename
    """
    name, ext = os.path.splitext(filename)
    return '{original_name}_{appendix}{extension}'.format(
            original_name=name,
            appendix=generate_filename(length=4),
            extension=ext)


def strip_tags(html):
    html_from_markdown = markdown(html)
    s = MLStripper()
    s.feed(html_from_markdown)
    return s.get_data()


def shorten_text(text):
    text = strip_tags(text)
    if len(text) > 500:
        text = u'{}...'.format(text[:500])
    return text


def translit_text(text=u'', lowercase=True):
    """
    Generate a correct url based on static page title
    """
    if lowercase:
        text = text.lower()
    char_table = {
        u'а': 'a',
        u'б': 'b',
        u'в': 'v',
        u'г': 'h',
        u'ґ': 'g',
        u'д': 'd',
        u'ё': 'e',
        u'э': 'e',
        u'е': 'e',
        u'є': 'je',
        u'ж': 'zh',
        u'з': 'z',
        u'и': 'u',
        u'ы': 'u',
        u'і': 'i',
        u'ї': 'ji',
        u'й': 'ji',
        u'к': 'k',
        u'л': 'l',
        u'м': 'm',
        u'н': 'n',
        u'о': 'o',
        u'п': 'p',
        u'р': 'r',
        u'с': 's',
        u'т': 't',
        u'у': 'y',
        u'ф': 'f',
        u'х': 'kh',
        u'ц': 'c',
        u'ч': 'ch',
        u'ш': 'sh',
        u'щ': 'sch',
        u'ь': '',
        u'ъ': '',
        u'ю': 'ju',
        u'я': 'ja',
        u' ': '_'
    }

    allowed = '-_'
    result = ''
    for char in text:
        if char in char_table:
            result += char_table[char]
        elif char.isalnum() or char in allowed:
            result += char
    return result


def create_slug(title):
    """
    Generates an alias url for the article by its title.
    """
    only_latin = translit_text(title.replace(' ', '-'))
    is_allowed = lambda ch: ch.isalpha() or ch.isdigit() or ch == '-'
    if not only_latin:
        return ''

    leave_allowed = reduce(lambda acc, ch: acc + ch if is_allowed(ch) else acc,
                           only_latin, '')
    if not leave_allowed:
        return ''

    remove_duplicates = reduce(
        lambda acc, ch: acc + ch if ch != '-' or ch != acc[-1] else acc,
        leave_allowed)

    remove_leading = remove_duplicates.strip('-')

    return remove_leading
