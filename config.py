import os
import logging
import json

# Get configuration from environment
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://gswncbve:1n4JGHLrb0dVst_PgDrr92DyP87RgOYu@batyr.db.elephantsql.com/gswncbve"
)

if 'VCAP_SERVICES' in os.environ:
    print('Getting database from VCAP_SERVICES')
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    DATABASE_URI = vcap_services['user-provided'][0]['credentials']['database_uri']


# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret for session management
SECRET_KEY = os.getenv("SECRET_KEY", "sup3r-s3cr3t")
LOGGING_LEVEL = logging.INFO
