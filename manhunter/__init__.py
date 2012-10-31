import os
from flask import Flask


app = Flask(__name__)


def configure():
    here = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.dirname(here)
    app.config.from_pyfile(os.path.join(config_path, 'settings.py'))
    app.config.from_pyfile(os.path.join(config_path, 'local_settings.py',),
                           silent=True)

import util
import views
