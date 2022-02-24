import time

db = {}


def register(client):
    ip_client = client.tcp_client.ip_client
    db[ip_client.ip] = ip_client


def send(datagram, is_wait=False):
    ip = datagram.receive_ip
    if ip in db:
        ip_client = db[ip]
        ip_client.get(datagram)
    elif is_wait:
        time.sleep(0.3)
