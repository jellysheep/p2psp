#!/usr/bin/env python3

from port_prediction_test import avg_skip_number, test_success_rate

number_of_runs = 10000

incorporated_peers = 1
skip_likeliness_monitor = 1
skip_likeliness_peer = 5
max_predicted_ports = 10

f = open("results5.txt", 'w')
for port_step in range(1, 11):
    success_percentage_0_mon = test_success_rate(number_of_runs, 0, port_step,
            incorporated_peers, max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer)
    success_percentage_1_mon = test_success_rate(number_of_runs, 1, port_step,
            incorporated_peers, max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer)
    success_percentage_2_mon = test_success_rate(number_of_runs, 2, port_step,
            incorporated_peers, max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer)
    f.write("{0}\t{1}\t{2}\t{3}\n".format(port_step, success_percentage_0_mon, success_percentage_1_mon, success_percentage_2_mon))
f.close()
