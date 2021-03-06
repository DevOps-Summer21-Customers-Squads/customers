# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

### -----------------------------------------------------------
###  Modified by DevOps Course Summer 2021 Customer Team
###  Members:
###     Du, Li | ld2342@nyu.edu | Nanjing | GMT+8
###     Cai, Shuhong | sc8540@nyu.edu | Shanghai | GMT+8
###     Zhang, Teng | tz2179@nyu.edu | Ningbo | GMT+8
###     Zhang, Ken | sz1851@nyu.edu | Shanghai | GMT+8
###     Wang,Yu-Hsing | yw5629@nyu.edu | Taiwan | GMT+8
### -----------------------------------------------------------

"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""

import os
import sys
import logging
from flask import Flask

# Create Flask application
app = Flask(__name__)
app.config.from_object("config")

# Import the routes After the Flask app is created
from service import routes, models # pylint: disable=wrong-import-position

# Set up logging for production
print("Setting up logging for {}...".format(__name__))
app.logger.propagate = False
app.url_map.strict_slashes = False
app.config['LOGGING_LEVEL'] = logging.INFO


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    # Make all log formats consistent
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s", "%Y-%m-%d %H:%M:%S %z"
    )
    for handler in app.logger.handlers:
        handler.setFormatter(formatter)
    app.logger.info("Logging handler established")

# Banner
app.logger.info(70 * "*")
app.logger.info("  CUSTOMER SYSTEM  ".center(70, "*"))
app.logger.info("  NYU DevOps Summer 2021  ".center(70, "*"))
app.logger.info("  Du, Li | ld2342@nyu.edu   ".center(70, "*"))
app.logger.info("  Cai, Shuhong | sc8540@nyu.edu  ".center(70, "*"))
app.logger.info("  Zhang, Teng | tz2179@nyu.edu  ".center(70, "*"))
app.logger.info("  Zhang, Ken S. | sz1851@nyu.edu  ".center(70, "*"))
app.logger.info("  Wang, Yu-Hsing | yw5629@nyu.edu  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # make our sqlalchemy tables
except Exception as error: # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

app.logger.info("Service inititalized!")
    