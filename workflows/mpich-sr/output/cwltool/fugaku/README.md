This directory contains tests performed on Fugaku HPC.

Fugaku was not included in the first tag of this repository, which includes
the tests performed for the CWL + MPI master's thesis.

Noteworthy:

- Everything was executed successfully without Singularity containers,
  showing that the integration of CWL with PJM, LLIO, and Fujitsu components
  (software and hardware) works fine, but containerisation with MPI still
  requires some further work;
- The `.err` and `.out` files are empty as these tests were executed in an
  interactive PJM session, and the MPI output is redirected to a local file
  under a subdirectory of the working directory, named `.output.$PJMJOBID`;
- `cwltool` had to be executed with `--preserve-entire-environment`, as it
  was not straightforward to identify which variables Fujitsu MPI required,
  just `LD_LIBRARY_PATH` and the `*MPI*` environment variables of the PJM
  session (allocated with `--mpi`) were not sufficient;
- Fugaku uses `mpifcc` as compiler, and `mpiexec` as MPI launcher, so the
  automation scripts and CWL workflows were adjusted manually;
- Singularity works for most cwltool commands, but it failed trying to
  pull the `docker://mfisherman/mpich:4.3.2` image, and placing the container
  manually in Fugaku did not work as cwltool tries to pull a new version.  
