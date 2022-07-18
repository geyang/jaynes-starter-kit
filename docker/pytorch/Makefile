version=$(shell cat VERSION)

default: build release
build:
	echo $(version)
	docker build -t pytorch .
run:
	docker run pytorch
release:
	docker tag pytorch episodeyang/pytorch:$(version)
	docker push episodeyang/pytorch:$(version)
	docker tag pytorch episodeyang/pytorch:latest
	docker push episodeyang/pytorch:latest
