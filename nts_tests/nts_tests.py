import errno
import socket
import struct
import threading
import time

import ipaddress

SPLITTER_ADDRESS = '127.0.0.1'
SPLITTER_PORT = 8080

MSG_PEER_HELLO = 'hello from peer'
MSG_SPLITTER_HELLO = 'hello from splitter'
MSG_SPLITTER_SEND_ADDR = 'public address:'
MSG_SPLITTER_NEW_PEER = 'new peer:'
MSG_PACK = '4si'

running = True

def address_to_string(addr):
    return struct.pack(MSG_PACK, ipaddress.ip_address(unicode(addr[0])).packed, addr[1])

def string_to_address(string):
    data = struct.unpack(MSG_PACK, string)
    return (str(ipaddress.ip_address(data[0]).exploded), data[1])

def udp_splitter():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SPLITTER_ADDRESS, SPLITTER_PORT))
    peers = []

    while running:
        try:
            data, new_peer = sock.recvfrom(1024, socket.MSG_DONTWAIT)
            if data != MSG_PEER_HELLO:
                continue
            # print 'received peer message "%s" from %s' % (data, addr)
            if new_peer not in peers:
                print 'splitter: new peer %s' % (new_peer,)
                sock.sendto(MSG_SPLITTER_HELLO, new_peer)
                new_peer_addr = address_to_string(new_peer)
                sock.sendto("%s%s" % (MSG_SPLITTER_SEND_ADDR, new_peer_addr), new_peer)
                for old_peer in peers:
                    sock.sendto("%s%s" % (MSG_SPLITTER_NEW_PEER, address_to_string(old_peer)), new_peer)
                    sock.sendto("%s%s" % (MSG_SPLITTER_NEW_PEER, new_peer_addr), old_peer)
                peers.append(new_peer)
        except socket.error as e:
            if e.errno == errno.EAGAIN:
                time.sleep(0.1)
            else:
                raise

    sock.close()


def udp_peer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    peers = []

    # connect to splitter
    time.sleep(0.5)  # wait for splitter to start
    sock.sendto(MSG_PEER_HELLO, (SPLITTER_ADDRESS, SPLITTER_PORT))
    data = sock.recv(1024)
    assert data == MSG_SPLITTER_HELLO

    # get public address and port
    data = sock.recv(1024)
    assert data.startswith(MSG_SPLITTER_SEND_ADDR)

    # receive other peers' addresses
    while running:
        try:
            while True:
                data = sock.recv(1024, socket.MSG_DONTWAIT)
                assert data.startswith(MSG_SPLITTER_NEW_PEER)
                new_peer = string_to_address(data[len(MSG_SPLITTER_NEW_PEER):])
                print 'peer: new peer %s' % (new_peer,)
        except socket.error as e:
            if e.errno != errno.EAGAIN:
                raise

    sock.close()


threads = [threading.Thread(target=udp_peer),
           threading.Thread(target=udp_peer),
           threading.Thread(target=udp_splitter)]
for thread in threads:
    thread.start()
time.sleep(5)
running = False
for thread in threads:
    thread.join()
