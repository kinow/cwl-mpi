# sr.c – Running with StreamFlow

StreamFlow has a different command-line interface than cwltool or Toil.
This directory contains a wrapper script, [`streamflow-run-wrapper.sh`](./streamflow-run-wrapper.sh)
that creates the StreamFlow input file and runs the workflow.

This is an example StreamFlow input file:

```yaml
version: v1.0
workflows:
  workflow_name:
    type: cwl
    config:
      file: "/home/kinow/Development/python/workspace/cwl-mpi/workflows/mpich-sr/mpich-mpirun-base-command.cwl"
      docker:
        - step: /
          deployment:
            type: singularity
            config: {}
```

The wrapper script, `streamflow-run-wrapper.sh` takes a mandatory argument,
the path to the StreamFlow input file. A second optional argument is the
path to the job file. Another optional argument is the flag `--singularity`,
which adds the `docker:` YAML section above.

The [`Makefile`](./Makefile) build script can be used to run the tests with
StreamFlow by setting the `CWL_RUNNER` variable to `streamflow-run-wrapper.sh`.

Example usage:

```bash
$ make CWL_RUNNER=./streamflow-run-wrapper.sh mpicc
$ make CWL_RUNNER=./streamflow-run-wrapper.sh DEBUG=1 mpirun-base  # this adds --debug
```
