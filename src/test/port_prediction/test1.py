#!/usr/bin/env python3

from port_prediction_test import avg_skip_number, test_success_rate

number_of_runs = 10000

port_step = 1
num_peers = 2
skip_likeliness_monitor = 1
skip_likeliness_peer = 5

f = open("results.txt", 'w')
for max_predicted_ports in range(1, 11):
    success_percentage_1_mon = test_success_rate(number_of_runs, 1, port_step,
            num_peers, max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer)
    success_percentage_2_mon = test_success_rate(number_of_runs, 2, port_step,
            num_peers, max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer)
    f.write("{0}\t{1}\t{2}\n".format(max_predicted_ports, success_percentage_1_mon, success_percentage_2_mon))
f.close()
