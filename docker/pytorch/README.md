# Docker Image

This folder contains the docker image for these custom environments. To re-build the docker image, rum

```bash
make build
```

And to release this image to docker hub, so that our ec2 instances can read from it, run

```bash
make release
```

## ToDos

you need to fill in the [./Dockerfile](Dockerfile),  make build and make release script.



Content of the Makefile:

```makefile
#! Makefile
build:
	docker build -t geometric_vision .
run:
	docker run geometric_vision
release:
	docker tag geometric_vision improbableailab/geometric_vision
	docker push improbableailab/geometric_vision
```

