import os
import logging
import json

# Get configuration from environment
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

if 'VCAP_SERVICES' in os.environ:
    print('Getting database from VCAP_SERVICES')
    VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
    DATABASE_URI = VCAP_SERVICES['user-provided'][0]['credentials']['url']


# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret for session management
SECRET_KEY = os.getenv("SECRET_KEY", "sup3r-s3cr3t")
LOGGING_LEVEL = logging.INFO
