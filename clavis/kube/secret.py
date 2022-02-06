import logging
import base64
import sys
import pykube
import secrets as pysecrets

from clavis.kube import api, k8s_namespace
from clavis.crypto.x509 import generate_tls_keys
from clavis.errors import ClavisFatalException

logger = logging.getLogger("clavis")


def get_or_create_rpc_security(rpc_sec_path: str) -> str:
    if not k8s_namespace:
        logger.error("Failed to create/get k8s TLS secret, cannot get clavis server namespace")
        raise ClavisFatalException()

    try:
        secret = pykube.Secret.objects(api).filter(namespace=k8s_namespace).get_or_none(name="clavis-tls")
        if not secret:
            tls_key, tls_cert = generate_tls_keys(k8s_namespace)
            integrity_secret = pysecrets.token_urlsafe(32)
            secret = {
                "apiVersion": "v1",
                "kind": "Secret",
                "metadata": {
                    "name": "clavis-tls",
                    "namespace": k8s_namespace
                },
                "type": "Opaque",
                "data": {
                    "tls.key": base64.b64encode(tls_key).decode("utf-8"),
                    "tls.crt": base64.b64encode(tls_cert).decode("utf-8"),
                    "integrity": base64.b64encode(integrity_secret.encode("utf-8")).decode("utf-8")
                }
            }
            pykube.Secret(api, secret).create()
        else:
            tls_key = base64.b64decode(secret.obj["data"]["tls.key"])
            tls_cert = base64.b64decode(secret.obj["data"]["tls.crt"])
            integrity_secret = base64.b64decode(secret.obj["data"]["integrity"]).decode("utf-8")

        with open(f"{rpc_sec_path}/tls.key", "wb") as f:
            f.write(tls_key)
        with open(f"{rpc_sec_path}/tls.crt", "wb") as f:
            f.write(tls_cert)
        with open(f"{rpc_sec_path}/integrity", "w") as f:
            f.write(integrity_secret)

        return integrity_secret
    except Exception as e:
        logger.error(f"Failed to create/get k8s TLS secret, {e}")
        raise ClavisFatalException()
