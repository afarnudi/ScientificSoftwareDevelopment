1 - Write a Makefile that generates foo.data using the following rule:
	python3 dataWrap.py foo0.rawdata foo1.rawdata foo2.rawdata
2 - It should  generate bar.png or foo.png using the following rule(s):
	python3 plot.py foo.data	
	python3 plot.py bar.data
3 - The paper pdf is then built using pipeline.tex. 
4 - create a dummy target that cleans pdflatex artifacts.
5 - Setup the dependancies such that the paper is built whenever the following files are modified:
pipeline.tex
foo.png
foo.data
foo#.rawdata
bar.png
bar.data
plot.py

Try deleting foo.png and/or bar.png and/or foo.data to make sure the makefile recovers everything
