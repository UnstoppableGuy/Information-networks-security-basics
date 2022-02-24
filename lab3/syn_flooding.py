import time

from threading import Thread

from tcp_ip_protocol import Client, register


class Hacker:
    def __init__(self, client, ip, port):
        self._client = client
        self._client.tcp_client.ip_client._ip = ip
        self._client.tcp_client._ports = (port,)
        self._spurious_ip = ip
        self._spurious_port = port

    def syn_flood(self, ip, port):
        print(f'{self}: syn flood server with ip={ip} port={port}')
        self._client.tcp_client.connect(ip, port, self._spurious_port)

    def __str__(self):
        return f'Hacker ip={self._client.ip} ports={self._client.ports} ' \
               f'(spurious ip={self._spurious_ip} port={self._spurious_port})'


def main():
    server_ip = '192.75.0.1'
    hacker_ip = '192.72.0.1'
    spurious_hacker_ip = '192.72.0.3'
    client_ip = '192.78.0.1'

    hacker_client = Client(hacker_ip, (8000,))
    register(hacker_client)
    hacker = Hacker(hacker_client, spurious_hacker_ip, 8000)

    server = Client(server_ip, (8000, 9000), is_server=True)
    register(server)

    thread = Thread(target=lambda: hacker.syn_flood(server_ip, 8000))
    thread.start()
    time.sleep(0.1)

    client = Client(client_ip, (8000,))
    register(client)

    i = 1
    while not client.connect(server_ip, 8000):
        i += 1
    print(f'{client.to_str()}: connect to server with {i} attempt')

    client.send(server_ip, 8000, 'Hello server!')


if __name__ == '__main__':
    main()
