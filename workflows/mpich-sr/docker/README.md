# Docker containers for MPICH sr.c

All these containers compile and run the MPI test program `sr.c`
from the MPICH code repository. They are used for testing containers
and MPI. Especially Singularity and Apptainer containers.

## Building

```bash
make all
# or
make intelmpi
make mpich
make openmpi
```

```bash
$ docker image list | grep "mpich-sr:"
kinow/mpich-sr:intelmpi                       3b1d5c9569da       17.7GB         4.38GB        
kinow/mpich-sr:mpich                          aef7ff7696a5        756MB          192MB        
kinow/mpich-sr:openmpi                        ae26d2fff542        725MB          186MB
```

## Running with Docker

```bash
$ docker run --rm -ti $USER/mpich-sr:intelmpi 
sr: size 2 rank 0
msg_sz=0, niter=1
sr: process 0 finished
sr: size 2 rank 1
All messages successfully received!
sr: process 1 finished

$docker run --rm -ti kinow/mpich-sr:mpich
sr: size 2 rank 0
msg_sz=0, niter=1
sr: size 2 rank 1
sr: process 0 finished
All messages successfully received!
sr: process 1 finished

$ docker run --rm -ti kinow/mpich-sr:openmpi
sr: size 2 rank 1
sr: size 2 rank 0
msg_sz=0, niter=1
sr: process 0 finished
All messages successfully received!
sr: process 1 finished
```

## Running with Singularity

One can convert the Docker image to a Singularity image and run it
locally. For example:

```bash
$ docker save kinow/mpich-sr:openmpi -o mpich-sr-openmpi.tar
$ singularity build mpich-sr-openmpi.sif docker-archive://mpich-sr-openmpi.tar
$ singularity exec mpich-sr-openmpi.sif mpirun -np 2 /app/sr
INFO:    squashfuse not found, will not be able to mount SIF or other squashfs files
INFO:    gocryptfs not found, will not be able to use gocryptfs
INFO:    Converting SIF file to temporary sandbox...
sr: size 2 rank 1
All messages successfully received!
sr: process 1 finished
sr: size 2 rank 0
msg_sz=0, niter=1
sr: process 0 finished
INFO:    Cleaning up image...
```

It is also possible to run the Singularity image with the `docker://` protocol
to have Singularity pull the image from Docker Hub, convert it to a Singularity
image and run it.

This example does that on CESGA FT3. The job executes `mpirun` inside an Slurm
job:

```bash
#!/bin/bash

#SBATCH --job-name=streamflow_cwl_mpi_1
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --partition=small
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH -t 00:05:00

mpirun -np 4 singularity exec docker://kinow/mpich-sr:openmpi /app/sr
```

The error logs should contain normal output about the MPI daemon process, and
the output logs should contain something similar to the following:

```bash
slurmstepd: info: Setting TMPDIR to /scratch/5489757. Previous errors about TMPDIR can be discarded
sr: size 4 rank 0
msg_sz=0, niter=1
sr: process 0 finished
sr: size 4 rank 2
sr: process 2 finished
sr: size 4 rank 1
All messages successfully received!
sr: process 1 finished
sr: size 4 rank 3
sr: process 3 finished

*****************************************************************************
*                                                                           *
*                    JOB EFFICIENCY REPORT (seff 5489757)                   *
*                                                                           *
*****************************************************************************
...
...
```

## Publishing

```bash
$ docker login
$ docker push $USER/mpich-sr:intelmpi
$ docker push $USER/mpich-sr:mpich
$ docker push $USER/mpich-sr:openmpi
```
