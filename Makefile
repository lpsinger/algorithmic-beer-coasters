all: gosper.svg hilbert.svg hilbert2.svg

%.svg: %.py
	python $< > $@
