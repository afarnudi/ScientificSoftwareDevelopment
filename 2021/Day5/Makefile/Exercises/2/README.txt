1 - Write a Makefie that generates foo.png using the following rule:
	python3 plot.py foo.data
2 - The paper pdf is then built using pipeline.tex. 
3 - create a dummy target that cleans pdflatex artifacts.
4 - Setup the dependancies such that the paper is built whenever the following files are modified:
pipeline.tex
foo.png
foo.data
bar.png
plot.py
