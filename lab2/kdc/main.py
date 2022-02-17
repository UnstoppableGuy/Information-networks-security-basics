import logging
import random

import des

from kdc.as_server import AS
from kdc.tgs_server import TGS


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class KDC:
    def __init__(self):
        self._client_keys = {}
        self._server_keys = {}
        self._as_tgs = des.get_random_key()
        self._tgs_id = des.get_random_key()
        self._as = AS(self._client_keys, self._as_tgs, self._tgs_id)
        self._tgs = TGS(self._server_keys, self._as_tgs, self._tgs_id)

    def register_client(self):
        client_id, client_key = self._register(self._client_keys)
        print(f'Register client id={client_id} key={client_key}', end='\n\n')
        return client_id, client_key

    def register_server(self):
        server_id, server_key = self._register(self._server_keys)
        print(f'Register server id={server_id} key={server_key}', end='\n\n')
        return server_id, server_key

    def _register(self, db):
        new_id = random.randint(0, 255)
        key = des.get_random_key()
        db[new_id] = key
        return new_id, key

    def get_tgt(self, packet):
        return self._as.get_ticket(*packet)

    def get_tgs(self, packet):
        return self._tgs.get_ticket(*packet)
