CC=pdflatex
FLAGS=-interaction="batchmode"
PYCC=python3


pipeline.pdf: pipeline.tex foo.png bar.png
	$(CC) $(FLAGS) pipeline.tex
	$(CC) $(FLAGS) pipeline.tex

%.png: plot.py %.data
	$(PYCC) $^
clean:
	rm *.log *.aux
