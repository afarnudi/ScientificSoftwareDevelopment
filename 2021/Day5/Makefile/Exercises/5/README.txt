1 - Write a Makefile that generates raw data files using the following rule:
	python3 dataGen.py
2 - It should generate foo.data/bar.data using the following rule(s):
	python3 dataWrap.py foo0.rawdata foo1.rawdata foo2.rawdata
	python3 dataWrap.py bar0.rawdata bar1.rawdata bar2.rawdata
3 - It should  generate bar.png or foo.png using the following rule(s):
	python3 plot.py foo.data	
	python3 plot.py bar.data
4 - The paper pdf is then built using pipeline.tex. 
5 - create a dummy target that cleans pdflatex artifacts.
6 - Setup the dependancies such that the paper is built whenever the following files are modified:
pipeline.tex
foo.png
foo.data
foo#.rawdata
bar.png
bar.data
plot.py

Try deleting the dependancies to make sure the makefile recovers everything.
Check if makefile automatically deletes some of your intermediate files.
