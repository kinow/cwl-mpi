DOCKER_USER ?= $(USER)
IMAGE_NAME = mpich-sr

IMAGE_MPICH    = $(DOCKER_USER)/$(IMAGE_NAME):mpich
IMAGE_OPENMPI  = $(DOCKER_USER)/$(IMAGE_NAME):openmpi
IMAGE_INTELMPI = $(DOCKER_USER)/$(IMAGE_NAME):intelmpi
# IMAGE_CRAY   = $(DOCKER_USER)/$(IMAGE_NAME):cray

.PHONY: all mpich openmpi intelmpi cray clean

all: mpich openmpi intelmpi cray

mpich:
	docker build -f Dockerfile.mpich -t $(IMAGE_MPICH) .

openmpi:
	docker build -f Dockerfile.openmpi -t $(IMAGE_OPENMPI) .

intelmpi:
	docker build -f Dockerfile.intelmpi -t $(IMAGE_INTELMPI) .

#cray:
#	docker build -f Dockerfile.cray -t $(IMAGE_CRAY) .

publish:
	docker login
	docker push $(IMAGE_MPICH)
	docker push $(IMAGE_OPENMPI)
	docker push $(IMAGE_INTELMPI)

clean:
	docker rmi $(IMAGE_MPICH) \
	           $(IMAGE_OPENMPI) \
	           $(IMAGE_INTELMPI) || true
	           # $(IMAGE_CRAY) || true
