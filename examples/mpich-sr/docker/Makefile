IMAGE_MPICH      = sr-mpich
IMAGE_OPENMPI    = sr-openmpi
IMAGE_INTELMPI   = sr-intelmpi
# IMAGE_CRAY       = sr-cray

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

clean:
	docker rmi $(IMAGE_MPICH) \
	           $(IMAGE_OPENMPI) \
	           $(IMAGE_INTELMPI) || true
	           # $(IMAGE_CRAY) || true
