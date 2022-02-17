import struct
import time

import des

from kdc.exceptions import AuthenticationError, TimeLimitError


class Server:
    def __init__(self, kdc):
        self._kdc = kdc
        self._id, self._key = kdc.register_server()

    @property
    def id(self):
        return self._id

    def start_session(self, packet):
        tgs, aut = packet
        print(f'Server id={self.id}: From client received tgs={tgs} and aut={aut}', end='\n\n')

        tgs = des.decrypt(tgs, self._key)
        client_id, server_id, ticket_time, server_ticket_length, k_c_ss = struct.unpack("QQQQQ", tgs)

        now = int(time.time())
        if server_id != self._id:
            AuthenticationError('Client failed authentication')

        if now - ticket_time > server_ticket_length:
            raise TimeLimitError('Time of ticket is over')

        aut = des.decrypt(aut, k_c_ss)
        copy_client_id, tm2 = struct.unpack("QQ", aut)

        if client_id != copy_client_id:
            AuthenticationError('Client failed authentication')

        if now - tm2 > server_ticket_length:
            raise TimeLimitError('Time of ticket is over')

        response = struct.pack("Q", tm2 + 1)
        response = des.encrypt(response, k_c_ss)
        return response
