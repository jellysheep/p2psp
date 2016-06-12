
all: plot.png plot.pdf

clean:
	rm -f results.txt results2.txt results3.txt results4.txt results5.txt results6.txt plot.png plot.pdf

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
results6.txt: test6.py port_prediction_test.py
	./$<
results7.txt: test7.py port_prediction_test.py
	./$<

plot.pdf: gnuplot.txt results.txt results2.txt results3.txt results4.txt results5.txt results6.txt results7.txt
	gnuplot $<

plot.png: plot.pdf
	pdftocairo -png -r 80 -singlefile $< > $@
