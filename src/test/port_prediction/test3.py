#!/usr/bin/env python3

from port_prediction_test import avg_skip_number, test_success_rate

number_of_runs = 10000

port_step = 1
incorporated_peers = 1
skip_likeliness_monitor = 1
max_predicted_ports = 20

f = open("results3.txt", 'w')
skip_likeliness_peer = 0.1
while skip_likeliness_peer < 20:
    skip_likeliness_peer += max(0.8, skip_likeliness_peer*0.1)
    success_percentage_1_mon = test_success_rate(number_of_runs, 1, port_step,
            incorporated_peers, max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer)
    success_percentage_2_mon = test_success_rate(number_of_runs, 2, port_step,
            incorporated_peers, max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer)
    f.write("{0}\t{1}\t{2}\n".format(avg_skip_number(number_of_runs, skip_likeliness_peer), success_percentage_1_mon, success_percentage_2_mon))
f.close()
