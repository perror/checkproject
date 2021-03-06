
all:

doc:
	epydoc --output doc/html --html checkproject/

check:
	@(cd test && ./check.sh)

clean:
	@rm -rf ./doc/html

distclean: clean
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +

help:
	@echo "Usage:"
	@echo "  make [all]\t\tNothing"
	@echo "  make doc\t\tBuild the documentation"
	@echo "  make check\t\tRun all the tests"
	@echo "  make clean\t\tRemove all files generated by make"
	@echo "  make distclean\t\tRemove all unnecessary files"
	@echo "  make help\t\tDisplay this help"

.PHONY:	doc clean help
