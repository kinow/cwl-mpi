# sr.c – Running with cwltool

The [`Makefile`](./Makefile) build script will run CWL tools and
workflows, by default, using `cwltool`.

The tests conducted in the master's thesis used:

- cwltool 3.2.20260413085819
- cwltool built from this pull request that improves
  Singularity + MPI, https://github.com/common-workflow-language/cwltool/pull/2216

The Make targets that use `cwltool:MPIRequirement` will fail with
cwltool 3.2.20260413085819 when using Singularity.

To run the targets with `cwltool:MPIRequirement`, `mpirun-mpireq` and `workflow-req`,
you will need to build cwltool from the pull request above.

Example usage:

```bash
$ make mpicc
$ make SINGULARITY=1 mpicc  # this adds --singularity
$ make clean build mpicc
$ make DEBUG=1 mpirun-base  # this adds --debug
$ make workflow-base
$ make SINGULARITY=1 mpirun-req
$ make SINGULARITY=1 workflow-req
```

You can also call the tools and workflows directly:

```bash
$ cwltool --quiet --strict-memory-limit --strict-cpu-limit --enable-ext workflow-base-command.cwl 
{
    "stderr": {
        "location": "file:///home/kinow/Development/python/workspace/cwl-mpi/workflows/mpich-sr/mpirun-base-command.err",
        "basename": "mpirun-base-command.err",
        "class": "File",
        "checksum": "sha1$da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "size": 0,
        "path": "/home/kinow/Development/python/workspace/cwl-mpi/workflows/mpich-sr/mpirun-base-command.err"
    },
    "stdout": {
        "location": "file:///home/kinow/Development/python/workspace/cwl-mpi/workflows/mpich-sr/mpirun-base-command.out",
        "basename": "mpirun-base-command.out",
        "class": "File",
        "checksum": "sha1$a35b82266acdebbdbd718f82b24a2d197f0ab3d7",
        "size": 136,
        "path": "/home/kinow/Development/python/workspace/cwl-mpi/workflows/mpich-sr/mpirun-base-command.out"
    }
}
```

And then inspect the output of the command.

```bash
$ cat mpirun-base-command.{out,err}
sr: size 2 rank 0
msg_sz=0, niter=1
sr: size 2 rank 1
All messages successfully received!
sr: process 1 finished
sr: process 0 finished
```

And clean the environment:

```bash
$ make clean
```
