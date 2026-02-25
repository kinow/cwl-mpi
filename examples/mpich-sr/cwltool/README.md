# cwltool

<https://cwltool.readthedocs.io/en/latest/>

CWLTool version: 3.1.20260108082146.dev10+g544f108b9 (commit 544f108b906c179520b0a6d64c3c21d168b48fa2)

## Prerequisites

```bash
pip install cwltool
```

## Local Tests

### Tool to compile sr.c

```bash
$ cwltool compile-sr.cwl compile-sr-job.yml
```

This will create the binary `./a.out`.

### Tool to run sr with mpirun

It uses `mpirun` as base command.

```bash
$ cwltool run-sr-mpirun.cwl run-sr-mpirun-job.yml
```

This will create the files `sr.out` and `sr.err`.

### Tool to run sr with MPIRequirement and Docker

This would be a natural change for a user that has an existing workflow
as in the example in the previous section, using `DockerRequirement`.
But, as per documentation, you cannot use `DockerRequirement` and
`cwltool:MPIRequirement` together ⚠️.

It is possible to try with the CWL tool `run-sr-mpireq.cwl`.

```bash
$ cwltool --enable-ext run-sr-mpireq.cwl --executable sr --msg_size 0 --niter 1 --np 2
INFO /home/kinow/Development/python/workspace/cwltool/venv/bin/cwltool 3.1.20260108082146.dev10+g544f108b9
INFO Resolved 'run-sr-mpireq.cwl' to 'file:///home/kinow/Development/python/workspace/cwl-mpi/examples/mpich-sr/run-sr-mpireq.cwl'
ERROR Workflow or tool uses unsupported feature:
No support for DockerRequirement and MPIRequirement both being required, unless Singularity or uDocker is being used.
```

### Tool to run sr with MPIRequirement and without Docker

The `run-sr-mpireq-nodocker.cwl` contains the same tool defined above, but without
using the `DockerRequirement`. This means this will use the system `mpirun`. If you
use the `compile-sr.cwl` tool to compile `sr`, you will probably have issues due to the
different MPI version used to compile and run ⚠️. So first use `mpicc` to compile your
`sr` program, and then launch this tool like this:

```bash
$ cwltool --enable-ext run-sr-mpireq-nodocker.cwl --executable ./sr --msg_size 0 --niter 100 --np 6
```

The logs show the generated command line with `mpirun`.

```bash
$ cwltool --enable-ext run-sr-mpireq-nodocker.cwl --executable ./sr --msg_size 0 --niter 100 --np 6
INFO /home/kinow/Development/python/workspace/cwltool/venv/bin/cwltool 3.1.20260108082146.dev10+g544f108b9
INFO Resolved 'run-sr-mpireq-nodocker.cwl' to 'file:///home/kinow/Development/python/workspace/cwl-mpi/examples/mpich-sr/run-sr-mpireq-nodocker.cwl'
INFO [job run-sr-mpireq-nodocker.cwl] /tmp/x4sjlafr$ mpirun \
    -n \
    6 \
    /tmp/z_h43sej/stg9fb84079-23dc-421e-bf1a-af390f79f145/sr \
    0 \
    100 > /tmp/x4sjlafr/sr.out 2> /tmp/x4sjlafr/sr.err
INFO [job run-sr-mpireq-nodocker.cwl] completed success
{
    "stderr_file": {
        "location": "file:///home/kinow/Development/python/workspace/cwl-mpi/examples/mpich-sr/sr.err",
        "basename": "sr.err",
        "class": "File",
        "checksum": "sha1$da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "size": 0,
        "path": "/home/kinow/Development/python/workspace/cwl-mpi/examples/mpich-sr/sr.err"
    },
    "stdout_file": {
        "location": "file:///home/kinow/Development/python/workspace/cwl-mpi/examples/mpich-sr/sr.out",
        "basename": "sr.out",
        "class": "File",
        "checksum": "sha1$55336983b3d0085fe66a66bed94398013139e319",
        "size": 302,
        "path": "/home/kinow/Development/python/workspace/cwl-mpi/examples/mpich-sr/sr.out"
    }
}INFO Final process status is success
```

## Workflow

```bash
$ cwltool sr-workflow.cwl sr-workflow-job.yml
```

This will run the workflow using `compile-sr.cwl` to compile `sr.c`, and
`run-sr.cwl` to run the binary generated. The input and output are written
to the disk.

You can watch the output log and change the `sr.c` parameters to use
different values for processors, message size, and iterations.

```bash
$ cwltool sr-workflow.cwl sr-workflow-job.yml --np=6 --msg_size=10 --niter=8 --source=./sr.c
```

## HPC Tests

CWLTool does not provide batch schedulers integration. While it can
be used in an HPC environment, for running workflows it will probably
require containers with Singularity and some work to make it work with
MPI, OpenMP, CUDA.

## Container Tests

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

