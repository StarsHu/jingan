# coding=utf-8

import threading
import jinja2
import settings
from tornado import template, web


def get_page_range(cur, mn, mx):
    page_range_len = int(settings.default_page_range_length)
    cur = int(cur)
    mn = int(mn)
    mx = int(mx)
    res_min = max(mn, cur - page_range_len + 1)
    res_max = min(mx, cur + page_range_len)
    if res_min == mn:
        if res_max != mx:
            res_max = min(mx, res_min + 2 * page_range_len - 1)
    elif res_max == mx:
        if res_min != mn:
            res_min = max(mn, res_max - 2 * page_range_len + 1)
    return res_min, res_max


class JinjaTemplate(object):
    def __init__(self, template_instance):
        self.template_instance = template_instance

    def generate(self, **kwargs):
        return self.template_instance.render(**kwargs)


class JinjaLoader(template.BaseLoader):
    def __init__(self, root_directory, **kwargs):
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(root_directory), **kwargs)
        self.jinja_env.globals['get_page_range'] = get_page_range
        self.templates = {}
        self.lock = threading.RLock()

    def resolve_path(self, name, parent_path=None):
        return name

    def _create_template(self, name):
        template_instance = JinjaTemplate(self.jinja_env.get_template(name))
        return template_instance
