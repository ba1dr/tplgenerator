# -*- coding: utf-8 -*-

import jinja2

from settings import TEMPLATES_DIR


def render(template_name, data):
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
        autoescape=False)
    rtemplate = jinja_env.get_template(template_name)
    retval = rtemplate.render(**data)
    return retval
