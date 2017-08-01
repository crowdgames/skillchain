# skillchain

Reads a JSON skill chain description from stdin and produces output suitable for use in Graphviz dot.

Example usage:
	python makechain.py < chain-example.json | dot -Tpdf > chain-example.pdf
