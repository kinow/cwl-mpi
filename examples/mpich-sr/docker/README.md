# Docker containers for MPICH sr.c

```bash
make mpich
make openmpi
make intelmpi
make all
```

```bash
$ docker image list | grep "sr-"
WARNING: This output is designed for human readability. For machine-readable output, please use --format.
sr-intelmpi:latest                            972192f1ff5a       17.7GB         4.38GB        
sr-mpich:latest                               3c3ca59a27e6        756MB          192MB        
sr-openmpi:latest                             37fad9d86cf6        725MB          186MB
```

```bash
$ docker run --rm -ti sr-openmpi
sr: size 2 rank 0
msg_sz=0, niter=1
sr: process 0 finished
sr: size 2 rank 1
All messages successfully received!
sr: process 1 finished

$docker run --rm -ti sr-mpich:latest
sr: size 2 rank 0
msg_sz=0, niter=1
sr: size 2 rank 1
sr: process 0 finished
All messages successfully received!
sr: process 1 finished

$ docker run --rm -ti sr-intelmpi:latest
sr: size 2 rank 1
sr: size 2 rank 0
msg_sz=0, niter=1
sr: process 0 finished
All messages successfully received!
sr: process 1 finished
```