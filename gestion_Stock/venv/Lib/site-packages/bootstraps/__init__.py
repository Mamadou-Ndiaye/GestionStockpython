import os
import bootstraps.macros
import jinja2


def BootstrapMacros(app):
    extra_folders = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(os.path.dirname(macros.__file__)),
    ])
    app.jinja_loader = extra_folders