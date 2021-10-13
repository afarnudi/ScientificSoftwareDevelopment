CC=pdflatex
FLAGS=-interaction="batchmode"

pipeline.pdf : pipeline.tex foo.png bar.png
	$(CC) $(FLAGS) pipeline.tex
	$(CC) $(FLAGS) pipeline.tex

clean:
	rm *.log *.aux
