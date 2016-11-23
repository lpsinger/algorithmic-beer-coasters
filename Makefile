all: gosper.svg hilbert.svg

%.svg: %.py
	python $< > $@
