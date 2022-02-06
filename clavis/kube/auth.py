import pykube
import logging
import json
import warnings
from contextlib import suppress
from clavis.kube import api
from expiring_dict import ExpiringDict

logger = logging.getLogger("clavis")

warnings.filterwarnings(
    "ignore", "Your application has authenticated using end user credentials"
)

user_cache = ExpiringDict(ttl=600, interval=30)


class TokenReview(pykube.objects.APIObject):
    version = "authentication.k8s.io/v1"
    endpoint = "tokenreviews"
    kind = "TokenReview"

    def create(self) -> dict:
        r = self.api.post(**self.api_kwargs(data=json.dumps(self.obj), obj_list=True))
        self.set_obj(r.json())
        return r.request.headers


def get_user(token: str) -> str:
    if token in user_cache:
        return user_cache[token]

    tokenreview = TokenReview(api, _tokenreview_obj(token))
    tokenreview.create()
    with suppress(KeyError):
        user = tokenreview.obj["status"]["user"]["username"]
        if len(user) > 0:
            user_cache[token] = user
            return user

    return None


def get_local_user_token() -> str:
    tokenreview = TokenReview(api, _tokenreview_obj("dummy"))
    headers = tokenreview.create()
    token = None
    try:
        token = headers["authorization"].replace("Bearer ", "", 1)
    except KeyError:
        with suppress(KeyError):
            token = headers["Authorization"].replace("Bearer ", "", 1)
    if not token:
        return None

    return token


def _tokenreview_obj(token: str) -> dict:
    return {
        "apiVersion": "authentication.k8s.io/v1",
        "kind": "TokenReview",
        "spec": {"token": token},
    }
