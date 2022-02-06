import logging
import os
import pykube

logger = logging.getLogger("clavis")

api = pykube.HTTPClient(pykube.KubeConfig.from_env())

try:
    with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as ns:
        k8s_namespace = ns.read().strip()
except FileNotFoundError:
    logger.debug("Namespace file not found, not in Kubernetes pod")
    mode = os.environ.get("CLAVIS_MODE")
    if mode and mode.lower() == "release":
        k8s_namespace = None
    else:
        # local testing
        k8s_namespace = "default"