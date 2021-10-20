1 - Write a Makefile that generates bar.png or foo.png using the following rule(s):
	python3 plot.py foo.data	
	python3 plot.py bar.data
2 - The paper pdf is then built using pipeline.tex. 
3 - create a dummy target that cleans pdflatex artifacts.
4 - Setup the dependancies such that the paper is built whenever the following files are modified:
pipeline.tex
foo.png
foo.data
bar.png
bar.data
plot.py

Try deleting foo.png and/or bar.png to make sure the makefile recovers everything
