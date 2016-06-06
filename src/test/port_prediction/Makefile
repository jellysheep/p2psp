
all: plot.png plot.pdf

clean:
	rm -f results.txt results2.txt results3.txt results4.txt results5.txt plot.png plot.pdf

results.txt: test1.py port_prediction_test.py
	./$<
results2.txt: test2.py port_prediction_test.py
	./$<
results3.txt: test3.py port_prediction_test.py
	./$<
results4.txt: test4.py port_prediction_test.py
	./$<
results5.txt: test5.py port_prediction_test.py
	./$<

plot.pdf: gnuplot.txt results.txt results2.txt results3.txt results4.txt results5.txt
	gnuplot $<

plot.png: plot.pdf
	pdftocairo -png -r 80 -singlefile $< > $@
