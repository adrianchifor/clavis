import arrpc
import os
import logging

from clavis.kube.secret import get_or_create_rpc_security

logger = logging.getLogger("clavis")


def _rpc_handler(request):
    logger.info(request)
    return "pong"

def run_server(gcp_kms: str):
    addr = "127.0.0.1"
    rpc_sec_path = "."
    mode = os.environ.get("CLAVIS_MODE")
    if mode and mode.lower() == "release":
        addr = "0.0.0.0"
        rpc_sec_path = "/rpc"

    arrpc.Server(
        addr, 8443, _rpc_handler, metrics=True,
        tls_keyfile=f"{rpc_sec_path}/tls.key",
        tls_certfile=f"{rpc_sec_path}/tls.crt", 
        auth_secret=get_or_create_rpc_security(rpc_sec_path)
    ).start()

