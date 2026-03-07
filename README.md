# CWL MPI

This repository contains CWL MPI workflows. These workflows are used for
testing and demonstration purposes. They are part of a thesis written for
the [joint HPC Master at the universities of Santiago de Compostela and
da Coruña](https://www.usc.gal/en/studies/masters/engineering-and-architecture/master-high-performance-computing-online).

## Examples

These are some examples used for the tests.

`sr.c`: A test program from MPICH, that simply prints information about
the MPI ranks. Used to test that a MPI program is launched correctly on
HPCs with CWL.

### CWLTool

[Report](./examples/mpich-sr/cwltool/README.md)

### StreamFlow

[Report](./examples/mpich-sr/streamflow/README.md)

### Toil

[Report](./examples/mpich-sr/toil/README.md)
