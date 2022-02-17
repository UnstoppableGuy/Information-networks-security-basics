from kdc import KDC
from client import Client
from server import Server


kdc = KDC()
client = Client(kdc)
server = Server(kdc)
client.connect(server)
