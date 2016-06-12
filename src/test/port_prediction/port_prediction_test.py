#!/usr/bin/env python3

from functools import reduce
from math import ceil, floor, log, exp
from fractions import gcd
import sys
from random import random
from multiprocessing import Pool

def random_skips_number(skip_likeliness):
    return int(floor(-log(random()*0.9999 + 0.0001)*skip_likeliness))

def get_divisors(n):
    return sorted(set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))))

def count_product_combinations(factors):
    return reduce(lambda a, b: a + b, factors)

def get_guessed_ports(max_predicted_ports, peer_number, max_port_step, splitter_port, prediction_method):
    divisors = get_divisors(max_port_step)
    num_combinations = count_product_combinations(divisors)
    count_factor = max_predicted_ports/float(num_combinations)
    if prediction_method == 1: # simple method
        return sorted(set(list(
            splitter_port + (peer_number + skips) * 1
            for skips in range(max_predicted_ports))))[:max_predicted_ports]
    else: # default, advanced method
        return sorted(set(reduce(list.__add__, (list(
            splitter_port + (peer_number + skips) * port_step
            for skips in range(int(ceil(max_port_step/port_step*count_factor))))
            for port_step in divisors))))[:max_predicted_ports]

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

def testrun(max_predicted_ports, port_step, num_monitors, incorporated_peers, skip_likeliness_monitor, skip_likeliness_peer, prediction_method):
    src_port_to_splitter = 1000

    # Port prediction at peer 1:
    probable_port_step = -1
    last_known_src_port = src_port_to_splitter
    for _ in range(num_monitors):
        skips = random_skips_number(skip_likeliness_monitor)
        src_port_to_monitor = last_known_src_port + port_step * (1 + skips)
        probable_port_step = update_port_step(probable_port_step, last_known_src_port, src_port_to_monitor)
        last_known_src_port = src_port_to_monitor

    if probable_port_step < 0:
        probable_port_step = 1

    # Source port towards regular peers not used for port step determination
    src_port_to_peer = last_known_src_port
    for _ in range(incorporated_peers):
        skips = random_skips_number(skip_likeliness_peer)
        src_port_to_peer += port_step * (1 + skips)

    #~ peer_number = num_monitors + 1 # splitter is 0, monitor1 is 1, monitor2 is 2
    #~ probable_src_ports = get_guessed_ports(max_predicted_ports, peer_number, probable_port_step, src_port_to_splitter)
    peer_number = incorporated_peers
    if num_monitors > 1:
        probable_src_ports = get_guessed_ports(max_predicted_ports, peer_number, probable_port_step, last_known_src_port, prediction_method)
    else:
        probable_src_ports = get_guessed_ports(max_predicted_ports, peer_number, probable_port_step, last_known_src_port, prediction_method)

    success = src_port_to_peer in probable_src_ports
    return success

def test_success_rate(number_of_runs, num_monitors, port_step, incorporated_peers,
        max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer, prediction_method=2):
    successful_runs = 0
    for _ in range(number_of_runs):
        success = testrun(max_predicted_ports, port_step, num_monitors, incorporated_peers, skip_likeliness_monitor, skip_likeliness_peer, prediction_method)
        if success:
            successful_runs += 1
    success_percentage = successful_runs / number_of_runs
    return success_percentage

def avg_skip_number(number_of_runs, skip_likeliness):
    #~ avg_skips = 0
    #~ for _ in range(number_of_runs):
        #~ avg_skips += random_skips_number(skip_likeliness)
    #~ avg_skips /= number_of_runs
    #~ return avg_skips
    return 1/(exp(1/skip_likeliness)-1)
