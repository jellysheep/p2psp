
import errno
import socket
import threading
import time

SPLITTER_ADDRESS = '127.0.0.1'
SPLITTER_PORT = 8080
running = True

def udp_splitter():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SPLITTER_ADDRESS, SPLITTER_PORT))

    while running:
        try:
            data, addr = sock.recvfrom(1024, socket.MSG_DONTWAIT)
            print 'received peer message "%s" from %s' % (data, addr)
            sock.sendto('reply from splitter', addr)
        except socket.error as e:
            if e.errno == errno.EAGAIN:
                time.sleep(0.1)
            else:
                raise

    sock.close()

def udp_peer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_address = (SPLITTER_ADDRESS, SPLITTER_PORT)

    while running:
        time.sleep(0.5)
        sock.sendto('hello from peer', send_address)
        time.sleep(0.5)

        try:
            while True:
                data, addr = sock.recvfrom(1024, socket.MSG_DONTWAIT)
                print 'received splitter message "%s" from %s' % (data, addr)
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
