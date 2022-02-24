import tcp_ip_protocol.router as router


class IpClient:
    def __init__(self, tcp_client, ip):
        self._ip = ip
        self._tcp_client = tcp_client

    @property
    def ip(self):
        return self._ip

    def get(self, datagram):
        if self._ip != datagram.receive_ip:
            raise Exception

        from_ip = datagram.sender_ip
        tcp_datagram = datagram.tcp_datagram
        self._tcp_client.get(tcp_datagram, from_ip)

    def send(self, to_ip, datagram, is_wait=False):
        datagram = self.create_datagram(self._ip, to_ip, datagram)
        router.send(datagram, is_wait)

    @staticmethod
    def create_datagram(from_ip, to_ip, tcp_datagram):
        return Datagram(from_ip, to_ip, tcp_datagram)


class Datagram:
    def __init__(self, from_ip, to_ip, tcp_datagram):
        self._data = {
            'version_number': 4,
            'header_len': 160,
            'service_type': 0,
            'packet_len': 1500,
            'fragment_id': 1,
            'df': 0,
            'mf': 0,
            'fragment_shift': 0,
            'life_time': 10,
            'protocol_type': 6,
            'control_sum': 12345,
            'sender_ip': from_ip,
            'receive_ip': to_ip,
            'tcp_datagram': tcp_datagram,
        }

    @property
    def sender_ip(self):
        return self._data['sender_ip']

    @property
    def receive_ip(self):
        return self._data['receive_ip']

    @property
    def tcp_datagram(self):
        return self._data['tcp_datagram']
