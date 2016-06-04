#!/usr/bin/env python3

from functools import reduce
from math import ceil, floor, log
from fractions import gcd
import sys
from random import random

def random_skips_number(skip_likeliness):
    return int(floor(-log(random()*0.99 + 0.01)*skip_likeliness))

def get_divisors(n):
    return sorted(set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))))

def count_product_combinations(factors):
    return reduce(lambda a, b: a + b, factors)

def get_guessed_ports(max_predicted_ports, peer_number, max_port_step, splitter_port):
    divisors = get_divisors(max_port_step)
    num_combinations = count_product_combinations(divisors)
    count_factor = max_predicted_ports/float(num_combinations)
    return sorted(set(reduce(list.__add__, (list(
        splitter_port + (peer_number + skips) * port_step
        for skips in range(int(ceil(max_port_step/port_step*count_factor))))
        for port_step in divisors))))[:max_predicted_ports]
    #~ return sorted(set(reduce(list.__add__, (list(
        #~ splitter_port + (peer_number + skips) * port_step
        #~ for skips in range(max_predicted_ports))
        #~ for port_step in [1]))))[:max_predicted_ports]

def update_port_step(probable_port_step, source_port1, source_port2):
    # Skip check if measured port step is 0
    if probable_port_step == 0:
        return
    if probable_port_step < 0:
        probable_port_step = 0
    # Update source port information
    port_diff = abs(source_port1 - source_port2)
    probable_port_step = gcd(probable_port_step, port_diff)
    return probable_port_step

def testrun(max_predicted_ports, port_step, num_monitors, skips_splitter_monitor,
        skips_monitor_monitor, skips_monitor_peer):
    src_port_to_splitter = 1000
    src_port_to_monitor1 = src_port_to_splitter + port_step * (1 + skips_splitter_monitor)
    if num_monitors > 1:
        src_port_to_monitor2 = src_port_to_monitor1 + port_step * (1 + skips_monitor_monitor)
        src_port_to_peer1 = src_port_to_monitor2 + port_step * (1 + skips_monitor_peer)
        #~ print("Source ports: " + ", ".join([str(src_port_to_splitter), str(src_port_to_monitor1), str(src_port_to_monitor2), str(src_port_to_peer1)]))
    else:
        src_port_to_peer1 = src_port_to_monitor1 + port_step * (1 + skips_monitor_peer)
        #~ print("Source ports: " + ", ".join([str(src_port_to_splitter), str(src_port_to_monitor1), str(src_port_to_peer1)]))

    # Port prediction at peer 1:
    probable_port_step = -1
    probable_port_step = update_port_step(probable_port_step, src_port_to_splitter, src_port_to_monitor1)
    if num_monitors > 1:
        probable_port_step = update_port_step(probable_port_step, src_port_to_monitor1, src_port_to_monitor2)
    #~ print("Probable port step: " + str(probable_port_step))

    #~ peer_number = num_monitors + 1 # splitter is 0, monitor1 is 1, monitor2 is 2
    #~ probable_src_ports = get_guessed_ports(max_predicted_ports, peer_number, probable_port_step, src_port_to_splitter)
    peer_number = 1
    if num_monitors > 1:
        probable_src_ports = get_guessed_ports(max_predicted_ports, peer_number, probable_port_step, src_port_to_monitor2)
    else:
        probable_src_ports = get_guessed_ports(max_predicted_ports, peer_number, probable_port_step, src_port_to_monitor1)

    #~ print(str(max_predicted_ports) + str(probable_src_ports))
    success = src_port_to_peer1 in probable_src_ports
    return success

def test_success_rate(number_of_runs, num_monitors, port_step, num_peers, max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer):
    successful_runs = 0
    for _ in range(number_of_runs):
        skips_splitter_monitor = random_skips_number(skip_likeliness_monitor)
        if num_monitors > 1:
            skips_monitor_monitor = random_skips_number(skip_likeliness_monitor)
        else:
            skips_monitor_monitor = -1000
        skips_monitor_peer = random_skips_number(skip_likeliness_peer)
        success = testrun(max_predicted_ports, port_step, num_monitors, skips_splitter_monitor, skips_monitor_monitor, skips_monitor_peer)
        if success:
            successful_runs += 1
    success_percentage = successful_runs / number_of_runs
    return success_percentage


number_of_runs = 10000

num_monitors = int(sys.argv[1])
port_step = 1
num_peers = 2
max_number_guessed_ports = 10
skip_likeliness_monitor = 1
skip_likeliness_peer = 5

avg_monitor_skips = 0
avg_peer_skips = 0
for _ in range(number_of_runs):
    avg_monitor_skips += random_skips_number(skip_likeliness_monitor)/number_of_runs
    avg_peer_skips += random_skips_number(skip_likeliness_peer)/number_of_runs
print("Average number of skips between splitter and monitor: " + str(avg_monitor_skips), file=sys.stderr)
print("Average number of skips between monitor and peer: " + str(avg_peer_skips), file=sys.stderr)

for max_predicted_ports in range(1, max_number_guessed_ports+1):
    success_percentage = test_success_rate(number_of_runs, num_monitors, port_step,
            num_peers, max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer)
    print(str(max_predicted_ports) + " " + str(success_percentage))
