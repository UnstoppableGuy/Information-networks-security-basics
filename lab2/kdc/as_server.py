import struct
import time

import des

from kdc.exceptions import AuthorizationError


class AS:
    def __init__(self, client_keys, as_tgs, tgs_id, ticket_len=60):
        self._client_keys = client_keys
        self._as_tgs = as_tgs
        self._tgs_id = tgs_id
        self._ticket_len = ticket_len

    def get_ticket(self, client_id):
        print(f'KDC(AS): Request from client with id={client_id}')
        print(f'KDC(AS): Received client id={client_id}', end='\n\n')

        if client_id not in self._client_keys:
            raise AuthorizationError(f'Client is not registered')

        tm = int(time.time())
        k_c_tgs = des.get_random_key()
        tgt = struct.pack("QQQQQ", client_id, self._tgs_id, tm, self._ticket_len, k_c_tgs)
        tgt = des.encrypt(tgt, self._as_tgs)

        response = bytearray(tgt + struct.pack("Q", k_c_tgs))
        response = des.encrypt(response, self._client_keys[client_id])
        return response
