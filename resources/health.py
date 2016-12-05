"""
A health check endpoint for the application.

:copyright: (c) 2016 Pinn Technologies, Inc.
:license: All rights reserved
"""

from flask_restful import Resource


class Health(Resource):
    """
    Check the health of the server.

    Used to determine if the web service is running and healthy. Under
    the hood also checks health of dependancies, namely the database layer.
    """

    def get(self):
        """
        Perform a health check on the server.
        """
        # Check health of database layer
        import dock.worker.tasks as tasks
        rr = tasks.sample.delay('hello world')
        return {'Hello': 'World!',
                'success': True,
                'result': rr.get()}
