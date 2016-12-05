"""
Background task handler combining Celery and Flask.

:copyright: (c) 2016 Pinn Technologies, Inc.
:license: All rights reserved
"""

import celery
from dock import worker
# If you have application modules, say in a common folder,
# you can now import and use within containers


celery = celery.Celery(broker=worker.default.broker_url)
celery.config_from_object(worker.default)


@celery.task()
def sample(x):
    """Sample."""
    print x
    return x
