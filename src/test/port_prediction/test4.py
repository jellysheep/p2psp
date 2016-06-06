#!/usr/bin/env python3

from port_prediction_test import avg_skip_number, test_success_rate

number_of_runs = 10000

port_step = 1
num_peers = 2
skip_likeliness_monitor = 1
skip_likeliness_peer = 5
max_predicted_ports = 10

f = open("results4.txt", 'w')
for num_monitors in range(1, 11):
    success_percentage_port_step_1 = test_success_rate(number_of_runs, num_monitors, 1,
            num_peers, max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer)
    success_percentage_port_step_2 = test_success_rate(number_of_runs, num_monitors, 2,
            num_peers, max_predicted_ports, skip_likeliness_monitor, skip_likeliness_peer)
    f.write("{0}\t{1}\t{2}\n".format(num_monitors, success_percentage_port_step_1, success_percentage_port_step_2))
f.close()
