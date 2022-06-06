build:
	docker build -t jaynes .
build-m1:
	docker build -t jaynes . --platform=linux/amd64
run:
	docker run -it jaynes /bin/bash
test-aws:
	docker run -it jaynes aws --version
release:
	docker image tag jaynes episodeyang/jaynes:$(VERSION)
	docker push episodeyang/jaynes:$(VERSION)
