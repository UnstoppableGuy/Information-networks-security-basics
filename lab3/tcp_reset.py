from tcp_ip_protocol import Client, register


class Hacker:
    def __init__(self, hacker_client, client):
        self._hacker_client = hacker_client
        self._hacker_client.tcp_client.ip_client._ip = client.ip
        self._hacker_client.tcp_client._ports = client.ports
        self._client = client

    def send_rst_flag(self, ip, port):
        print(f'{self}: send rst to server with ip={ip} port={port}')
        from_port = self._client.ports[0]
        datagram = self._client.tcp_client.create_datagram(from_port, port)
        flags = self._client._tcp_client._sn_ac_flags[(from_port, ip, port)]
        datagram['sn'] = flags[0]
        datagram['as'] = flags[1]
        datagram.set_rst()
        self._client.tcp_client.ip_client.send(ip, datagram)

    def __str__(self):
        return f'Hacker ip={self._hacker_client.ip} ports={self._hacker_client.ports[0]} ' \
               f'(spurious ip={self._client.ip} port={self._client.ports[0]})'


def main():
    server_ip = '192.75.0.1'
    hacker_ip = '192.72.0.1'
    client_ip = '192.78.0.1'
    client_port = 8000
    server_port = 8000

    server = Client(server_ip, (server_port, 9000), is_server=True)
    register(server)

    client = Client(client_ip, (client_port,))
    register(client)

    hacker_client = Client(hacker_ip, (8000,))
    register(hacker_client)
    hacker = Hacker(hacker_client, client)

    client.connect(server_ip, server_port)
    client.send(server_ip, server_port, 'message1')
    client.send(server_ip, server_port, 'message2')
    hacker.send_rst_flag(server_ip, server_port)
    client.send(server_ip, server_port, 'message4')


if __name__ == '__main__':
    main()
