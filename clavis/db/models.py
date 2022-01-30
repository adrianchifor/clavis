import os
import datetime

import peewee as pw
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL') or 'sqlite:///clavis.db')

class BaseModel(pw.Model):
    class Meta:
        database = db

class Clavis(BaseModel):
    root_key = pw.TextField(null=True)
    tls_key = pw.TextField()
    tls_cert = pw.TextField()
    integrity_secret = pw.TextField()
    created_at = pw.DateTimeField(default=datetime.datetime.now)

class Secrets(BaseModel):
    name = pw.CharField(primary_key=True, max_length=255)
    value = pw.TextField()
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    updated_at = pw.DateTimeField(default=datetime.datetime.now)
    created_by = pw.CharField(max_length=255)
    svc_account = pw.CharField(index=True, max_length=255)
    delete_at = pw.DateTimeField(null=True, index=True)
    first_read = pw.BooleanField(default=False)

class Audit(BaseModel):
    id = pw.BigAutoField(primary_key=True)
    event = pw.CharField(max_length=6)
    secret = pw.CharField(index=True, max_length=255)
    user = pw.CharField(index=True, max_length=255)
    created_at = pw.DateTimeField(default=datetime.datetime.now)

