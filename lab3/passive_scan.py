from tcp_ip_protocol import Client, register


class Hacker:
    def __init__(self, client):
        self._client = client
        self._ip = client.ip
        self._port = client.ports[0]
        self._client.tcp_client.get = lambda datagram, from_ip: self.get(self._client.tcp_client, datagram, from_ip)
        self._ports = []

    def check_ports(self, ip, lport, rport):
        print(f'{self}: start check ports from {lport} to {rport} with ip={ip}')
        for port in range(lport, rport):
            self._client._tcp_client.connect(ip, port, self._port)
        print(f'{self}: server with ip={ip} has ports={self._ports}')

    def __str__(self):
        return f'Hacker ip={self._client.ip} port={self._port}'

    def get(self, tcp_client, datagram, from_ip):
        from_port = datagram.sender_port
        to_port = datagram.receive_port
        answer_datagram = tcp_client.create_datagram(to_port, from_port)
        answer_datagram.set_rst()
        answer_datagram['sn'] = datagram['as']
        answer_datagram['as'] = datagram['sn'] + 1
        tcp_client._ip_client.send(from_ip, answer_datagram)

        self._ports.append(from_port)
        print(f'{self}: server found with ip={from_ip} port={from_port}')


def main():
    server_ip = '192.75.0.1'
    hacker_ip = '192.72.0.1'

    server = Client(server_ip, (8000, 8015, 8050, 8075, 8100), is_server=True)
    register(server)

    hacker_client = Client(hacker_ip, (8000,))
    register(hacker_client)
    hacker = Hacker(hacker_client)

    hacker.check_ports(server_ip, 8000, 8090)


if __name__ == '__main__':
    main()
