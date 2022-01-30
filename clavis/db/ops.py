import logging

from gevent.socket import wait_read, wait_write
from psycopg2 import extensions

from clavis.db.models import db, Clavis, Secrets, Audit

logger = logging.getLogger("clavis")

def patch_psycopg2():
    extensions.set_wait_callback(_psycopg2_gevent_callback)

def _psycopg2_gevent_callback(conn, timeout=None):
    while True:
        state = conn.poll()
        if state == extensions.POLL_OK:
            break
        elif state == extensions.POLL_READ:
            wait_read(conn.fileno(), timeout=timeout)
        elif state == extensions.POLL_WRITE:
            wait_write(conn.fileno(), timeout=timeout)
        else:
            raise ValueError('poll() returned unexpected result')

def connect():
    db.connect(reuse_if_open=True)
    db.create_tables([Clavis, Secrets, Audit])