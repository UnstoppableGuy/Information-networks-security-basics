import struct
import time

import des

from kdc.exceptions import AuthenticationError


class Client:
    def __init__(self, kdc):
        self._kdc = kdc
        self._id, self._key = kdc.register_client()
        self._tgs = None

    def connect(self, server):
        print(f'Client id={self._id}: Try to connect to server with id={server.id}', end='\n\n')

        try:
            response = self._kdc.get_tgt((self._id,))
            print(f'Client id={self._id}: From KDC(AC) received tgt and c_tgs: {response}', end='\n\n')
            response = des.decrypt(response, self._key)
            tgt = response[:-8]
            c_tgs, = struct.unpack("Q", response[-8:])

            now = int(time.time())
            aut = struct.pack("QQ", self._id, now)
            aut = des.encrypt(aut, c_tgs)

            response = self._kdc.get_tgs((tgt, aut, server.id))
            print(f'Client id={self._id}: From KDC(TGS) received tgs and k_c_ss: {response}', end='\n\n')
            response = des.decrypt(response, c_tgs)
            tgs = response[:-8]
            k_c_ss, = struct.unpack("Q", response[-8:])

            now = int(time.time())
            aut = struct.pack("QQ", self._id, now)
            aut = des.encrypt(aut, k_c_ss)

            response = server.start_session((tgs, aut))
            print(f'Client id={self._id}: From server received increment time: {response}', end='\n\n')
            response = des.decrypt(response, k_c_ss)
            inc_time, = struct.unpack("Q", response)

            if inc_time != now + 1:
                raise AuthenticationError('Server failed authentication')

            print(f'Client id={self._id}: Success connect to server with id={server.id}')

        except Exception as e:
            print(e)
