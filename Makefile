all: build install fmt test

.PHONY: build
build:
	docker build -t clavis .

.PHONY: install
install:
	pip3 install --user .

.PHONY: fmt
fmt:
	black clavis/

.PHONY: test
test:
	python3 -m unittest