# Singularity with cwltool

Modifying the example CWL workflow `sr-workflow.cwl` from the `mpich-sr` example to use
`MPIRequirement` with `DockerRequirement` fails as they are not compatible:

```bash
$ cwltool --enable-ext sr-workflow.cwl sr-workflow-job.yml
...
INFO [workflow ] starting step run
INFO [step run] start
ERROR Exception on step 'run'
ERROR [step run] Cannot make job: No support for DockerRequirement and MPIRequirement both being required, unless Singularity or uDocker is being used.
INFO [workflow ] completed permanentFail
{
    "stderr": null,
    "stdout": null
}WARNING Final process status is permanentFail
```

We get a different error if we use Singularity or Apptainer instead:

```bash
$ cwltool --singularity --enable-ext sr-workflow.cwl sr-workflow-job.yml 
...
INFO [step run] start
WARNING MPIRequirement with containers is a beta feature
INFO Using local copy of Singularity image mfisherman_mpich:4.3.2.sif found in /home/kinow/Development/python/workspace/cwl-mpi/examples/openmpi-hello_nodename/singularity
...
INFO [job run] /tmp/vafotu7h$ mpirun \
    -n \
    2 \
    singularity \
    --quiet \
    run \
    --contain \
    --ipc \
    --cleanenv \
    --no-eval \
    --userns \
    --home \
    /tmp/vafotu7h:/MBIyoA \
    --mount=type=bind,source=/tmp/y1j1wduj,target=/tmp \
    --mount=type=bind,source=/tmp/iptrmzfw/a.out,target=/var/lib/cwl/stga070b955-23a7-4849-91f5-651a9850a531/a.out,readonly \
    --pwd \
    /MBIyoA \
    --net \
    --network \
    none \
    /home/kinow/Development/python/workspace/cwl-mpi/examples/openmpi-hello_nodename/singularity/mfisherman_mpich:4.3.2.sif \
    /var/lib/cwl/stga070b955-23a7-4849-91f5-651a9850a531/a.out \
    0 \
    1 > /tmp/vafotu7h/sr.out 2> /tmp/vafotu7h/sr.err
WARNING [job run] exited with status: 6
WARNING [job run] completed permanentFail
WARNING [step run] completed permanentFail
INFO [workflow ] completed permanentFail
{
    "stderr": {
        "location": "file:///home/kinow/Development/python/workspace/cwl-mpi/examples/openmpi-hello_nodename/singularity/sr.err",
        "basename": "sr.err",
        "class": "File",
        "checksum": "sha1$b732b9e3bce44a1acf6171fdb289b477ef8395f5",
        "size": 910,
        "path": "/home/kinow/Development/python/workspace/cwl-mpi/examples/openmpi-hello_nodename/singularity/sr.err"
    },
    "stdout": {
        "location": "file:///home/kinow/Development/python/workspace/cwl-mpi/examples/openmpi-hello_nodename/singularity/sr.out",
        "basename": "sr.out",
        "class": "File",
        "checksum": "sha1$cf60e11a4648fc37e83247c3427d0f469e04811f",
        "size": 162,
        "path": "/home/kinow/Development/python/workspace/cwl-mpi/examples/openmpi-hello_nodename/singularity/sr.out"
    }
}WARNING Final process status is permanentFail
``````

Looking at the `sr.out` and `sr.err` files, we see that `mpirun` is launching with Singularity
two processes, each with size 1 and rank 0.

`sr.err`:

```bash
Abort(943352582) on node 0 (rank 0 in comm 0): Fatal error in internal_Send: Invalid rank, error stack:
internal_Send(124): MPI_Send(buf=(nil), count=0, MPI_INT, 1, 0, MPI_COMM_WORLD) failed
internal_Send(78).: Invalid rank has value 1 but must be nonnegative and less than 1
Abort(943352582) on node 0 (rank 0 in comm 0): Fatal error in internal_Send: Invalid rank, error stack:
internal_Send(124): MPI_Send(buf=(nil), count=0, MPI_INT, 1, 0, MPI_COMM_WORLD) failed
internal_Send(78).: Invalid rank has value 1 but must be nonnegative and less than 1
--------------------------------------------------------------------------
prterun detected that one or more processes exited with non-zero status,
thus causing the job to be terminated. The first process to do so was:

   Process name: [prterun-ranma-147515@1,0]
   Exit code:    6
--------------------------------------------------------------------------
```

`sr.out`:

```bash
sr: size 1 rank 0
ERROR: needs to be run with at least 2 procs
msg_sz=0, niter=1
sr: size 1 rank 0
ERROR: needs to be run with at least 2 procs
msg_sz=0, niter=1
```

