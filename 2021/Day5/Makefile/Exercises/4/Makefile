CC=pdflatex
FLAGS=-interaction="batchmode"
PYCC=python3


pipeline.pdf: pipeline.tex foo.png bar.png
	$(CC) $(FLAGS) pipeline.tex
	$(CC) $(FLAGS) pipeline.tex

%.png: plot.py %.data
	$(PYCC) $^

foo.data: dataWrap.py foo0.rawdata foo1.rawdata foo2.rawdata
	$(PYCC) $^

clean:
	rm *.log *.aux
