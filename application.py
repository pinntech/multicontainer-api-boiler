#!/usr/bin/env python

"""
Main application file which defines resource endpoint and project config.

The main flask application file which configures the applications runtime
environment, sets up all endpoints as well as database connectors.

:copyright: (c) 2016 Pinn Technologies, Inc.
:license: All rights reserved
"""

from flask import Flask
from flask_restful import Api

from resources.health import Health

application = Flask(__name__)

# Flask Restful Configuration
api = Api(application)

# Resource Endpoints
api.add_resource(Health, '/', '/health')


if __name__ == '__main__':
    application.run(host='0.0.0.0')
