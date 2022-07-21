version=$(shell cat VERSION)

default: build release
build:
	echo $(version)
	docker build --progress plain -t pytorch .
clean-build:
	docker build -t pytorch . --no-cache=true
run:
	docker run pytorch
release:
	docker tag pytorch episodeyang/pytorch:$(version)
	docker push episodeyang/pytorch:$(version)
	docker tag pytorch episodeyang/pytorch:latest
	docker push episodeyang/pytorch:latest
