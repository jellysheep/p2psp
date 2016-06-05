
all: plot.png

results.txt: port_prediction_test.py
	./$<

plot.png: gnuplot.txt results.txt
	gnuplot $<
