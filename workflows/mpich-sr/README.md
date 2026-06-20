# sr.c – A MPICH test

These examples use the [
`sr.c`](https://github.com/pmodels/mpich/blob/a0f6d778bb864774ef9cdd29b1bd6004adc6cf64/test/basic/sr.c)
test from the MPICH source code.

Use the [Makefile](./Makefile) to build and run the CWL tools and workflows.
Example usage:

```bash
$ make clean
# Runs mpicc
$ make SINGULARITY=1 build
$ # Runs the sr tool using mpirun as baseCommand
$ make mpirun-base
$ # Runs the sr tool using MPIRequirement
$ make mpirun-mpi
$ # Runs the complete workflow (mpicc + mpirun) with mpirun as baseCommand
$ make workflow-base
$ # Runs the complete workflow (mpicc + mpirun) with MPIRequirement
$ make workflow-req
```

By default, CWL runs with `--no-container`. You can enable Singularity with
`SINGULARITY=1`, e.g., `make SINGULARITY=1 mpicc`.

We use a test case from the MPICH source code as an example.
The test is executed on multiple HPC systems and can run with
different MPI implementations (e.g., Open MPI, Intel MPI),
depending on the system configuration.

The CWL workflow and tool defined here are used in the master's
thesis as the simplest test of CWL + MPI.

> On LUMI, `srun --pmi=pmi2` worked with `srun` directly in the terminal, but
> when used within a Slurm job, it failed. Further tests are required.

## Main files

- [`mpicc.cwl`](mpicc.cwl)
    - A CWL `CommandLineTool` that compiles C programs with MPICH `mpicc`.
    - By default, compiles `sr.c` and produces `sr` binary.
    - Example usage: `cwltool mpicc.cwl`, then verify you now have the binary `sr`.

- [`mpirun-base-command.cwl`](./sr-workflow-base-command.cwl)
    - A CWL `CommandLineTool` that runs an MPI program with MPICH `mpirun`.
    - `mpirun` is the base command.
    - Use `--singularity` on HPC systems.
    - You can disable containers with `--no-container`, assuming you have a compatible
      MPI launcher installed on your system.
    - By default, runs `sr`, and produces two log files, `sr-mpirun-base-command.out`
      and `sr-mpirun-base-command.err`.
    - Example usage:
      `cwltool --singularity --enable-ext  mpirun-base-command.cwl --msg_size 10 --niter 10 --np 2`

- [`mpirun-mpi-requirement.cwl`](sr-workflow-mpi-requirement.cwl)
    - A CWL `CommandLineTool` that runs an MPI program with MPICH `mpirun`.
    - The base command is empty.
    - `MPIRequirement` is used to specify the MPI launcher as base command.
    - Use `--singularity` on HPC systems
      (requires https://github.com/common-workflow-language/cwltool/pull/2216)
    - You can disable containers with `--no-container`, assuming you have a compatible
      MPI launcher installed on your system.
    - By default, runs `sr`, and produces two log files, `sr-mpirun-mpi-requirement.out`
      and `sr-mpirun-mpi-requirement.err`.
    - Note **you must enable `--enable-ext`** to use `MPIRequirement`.
    - Example usage:
      `cwltool --singularity --enable-ext  sr-mpirun-mpi-requirement.cwl --msg_size 10 --niter 10 --np 2`

- [`sr-workflow-base-command.cwl`](sr-workflow-base-command.cwl)
    - A Workflow that runs `mpicc.cwl` and `mpirun-base-command.cwl`.

- [`sr-workflow-mpi-requirement.cwl`](sr-workflow-mpi-requirement.cwl)
    - A Workflow that runs `mpicc.cwl` and `mpirun-mpi-requirement.cwl`.

## Other files

- [`sr.c`](sr.c)
    - The MPICH `sr.c` test program, copied from the MPICH source code
      commit `a0f6d778bb864774ef9cdd29b1bd6004adc6cf64`.
- [`Makefile`](Makefile)
    - Build script.
- [`mpi-config-file.yml`](mpi-config-file.yml)
    - Example MPI configuration file. Used by the `MPIRequirement` to
      load MPI settings to be used in a specific platform (e.g., use `srun` instead of `mpirun`).
- [`mpicc-job.yml`](mpicc-job.yml)
    - Example job file for `mpicc.cwl`.
    - Example usage: `cwltool mpicc.cwl mpicc-job.yml`
    - The example above causes the output to be `a.out` (specified in the job file) instead of `sr`.

## License

The contents in this directory are licensed under the CC 4.0 BY International. The
`sr.c` is a copy from the MPICH project, and it licensed under their license,
https://github.com/pmodels/mpich/blob/31d76832cf01e3ad2fccabd3cf25bfb359696aed/COPYRIGHT
(permissive).
