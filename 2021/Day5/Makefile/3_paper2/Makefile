PAPER=paper2
PYCC=python3
LATEXCC=pdflatex
LATEXFLAGS= -interaction="batchmode"


#all: $(PAPER).pdf

$(PAPER).pdf: $(PAPER).tex Fig1.pdf
	$(LATEXCC) $(LATEXFLAGS) $(PAPER)

Fig1.pdf: Fig1gen.py funcs.py
	$(PYCC) Fig1gen.py

clean:
	rm *.toc *.log *.aux 
