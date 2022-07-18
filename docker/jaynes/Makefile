version=$(shell cat VERSION)

default: build release
build:
	cp ../../VERSION .
	echo $(version)
	docker build -t jaynes .
build-m1:
	docker build -t jaynes . --platform=linux/amd64
run:
	docker run -it jaynes /bin/bash
test-aws:
	docker run -it jaynes aws --version
release:
	docker image tag jaynes episodeyang/jaynes:$(version)
	docker push episodeyang/jaynes:$(version)
	docker image tag jaynes episodeyang/jaynes:latest
	docker push episodeyang/jaynes:latest
