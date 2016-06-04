
all: plot.png

results_1_monitor.txt: port_prediction_test.py
	$(SHELL) -c "./$< 1 > $@"

results_2_monitors.txt: port_prediction_test.py
	$(SHELL) -c "./$< 2 > $@"

plot.png: gnuplot.txt results_1_monitor.txt results_2_monitors.txt
	gnuplot $<
