# Example: MPICH's sr.c (test)

`sr.c` from MPICH source code.

https://github.com/pmodels/mpich/blob/a0f6d778bb864774ef9cdd29b1bd6004adc6cf64/test/basic/sr.c

## Tools

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
different MPI version used to compile and run ⚠️ . So first use `mpicc` to compile your
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
