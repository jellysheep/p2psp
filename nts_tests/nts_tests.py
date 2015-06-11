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

    # connect to splitter
    time.sleep(0.5)  # wait for splitter to start
    sock.sendto(MSG_PEER_HELLO, (SPLITTER_ADDRESS, SPLITTER_PORT))
    data = sock.recv(1024)
    assert data == MSG_SPLITTER_HELLO

    # get public address and port of this peer
    data = sock.recv(1024)
    assert data.startswith(MSG_SPLITTER_SEND_ADDR)
    public_address = string_to_address(data[len(MSG_SPLITTER_SEND_ADDR):])
    print 'peer: got public address %s' % (public_address,)

    # receive other peer's address
    data = sock.recv(1024)
    assert data.startswith(MSG_SPLITTER_NEW_PEER)
    peer = string_to_address(data[len(MSG_SPLITTER_NEW_PEER):])
    print 'peer %s: new peer %s' % (public_address, peer)

    time.sleep(0.5)
    # connect to peer
    sock.sendto(MSG_PEER_HELLO, peer)
    data, reply_peer = sock.recvfrom(1024)
    print 'peer %s: received "%s" from %s' % (public_address, data, reply_peer)

    sock.close()


splitter_thread = threading.Thread(target=udp_splitter)
splitter_thread.start()
peer_threads = [threading.Thread(target=udp_peer), threading.Thread(target=udp_peer)]
for thread in peer_threads:
    thread.start()

for thread in peer_threads:
    thread.join()
running = False
splitter_thread.join()
