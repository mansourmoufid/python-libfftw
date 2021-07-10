.PHONY: test
test:
	py.test

.PHONY: cleanup
cleanup:
	rm -f *.pyc libfftw/*.pyc

.PHONY: clean
clean: cleanup
