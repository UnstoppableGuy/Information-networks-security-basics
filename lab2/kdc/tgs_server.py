import struct
import time

import des

from kdc.exceptions import AuthenticationError, AuthorizationError, TimeLimitError


class TGS:
    def __init__(self, server_keys, as_tgs, id, ticket_len=60):
        self._server_keys = server_keys
        self._as_tgs = as_tgs
        self._id = id
        self._ticket_len = ticket_len

    def get_ticket(self, tgt, aut, server_id):
        tgt = des.decrypt(tgt, self._as_tgs)
        client_id, tgs_id, tm1, ticket_length, c_tgs = struct.unpack("QQQQQ", tgt)
        print(f'KDC(TGS): Request from client with id={client_id}')
        print(f'KDC(TGS): Received tgt={tgt}, aut={aut}, server id={server_id}', end='\n\n')

        if server_id not in self._server_keys:
            raise AuthorizationError(f'Server with id={server_id} is not registered')

        now = int(time.time())
        if now - tm1 > ticket_length:
            raise TimeLimitError('Time of ticket is over')

        if tgs_id != self._id:
            raise AuthenticationError('TGS ids are not equal')

        aut = des.decrypt(aut, c_tgs)
        copy_client_id, tm2 = struct.unpack("QQ", aut)

        if now - tm2 > ticket_length:
            raise TimeLimitError('Time of ticket is over')

        if client_id != copy_client_id:
            raise AuthenticationError('Client ids are not equal')

        k_c_ss = des.get_random_key()

        tgs = struct.pack("QQQQQ", client_id, server_id, now, self._ticket_len, k_c_ss)
        tgs = des.encrypt(tgs, self._server_keys[server_id])

        response = bytearray(tgs + struct.pack("Q", k_c_ss))
        response = des.encrypt(response, c_tgs)
        return response
