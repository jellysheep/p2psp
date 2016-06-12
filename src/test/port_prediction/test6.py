#!/usr/bin/env python3

from port_prediction_test import avg_skip_number, test_success_rate

number_of_runs = 10000

incorporated_peers = 1
skip_likeliness_monitor = 1
skip_likeliness_peer = 5
max_predicted_ports = 4

f = open("results6.txt", 'w')
for port_step in range(1, 11):
    success_percentage = test_success_rate(number_of_runs, 1, port_step,
            incorporated_peers, max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer)
    success_percentage_simple = test_success_rate(number_of_runs, 2, port_step,
            incorporated_peers, max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer, 1)
    f.write("{0}\t{1}\t{2}\n".format(port_step, success_percentage, success_percentage_simple))
f.close()
