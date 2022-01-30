import arrpc
import db.ops as db

db.patch_psycopg2()
db.connect()

# def rpc_handler(request):
#     return ""

# server = arrpc.Server("0.0.0.0", 8443, rpc_handler, metrics=True,
#                       tls_certfile="tls.crt", tls_keyfile="tls.key",
#                       auth_secret="")
# server.start()