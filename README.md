# CWL MPI

This repository contains CWL MPI workflows. These workflows are used for
testing and demonstration purposes. They are part of a thesis written for
the [joint HPC Master at the universities of Santiago de Compostela and
da Coruña](https://www.usc.gal/en/studies/masters/engineering-and-architecture/master-high-performance-computing-online).

## CWL Conformance Tests

[Report](./cwl-conformance-tests/README.md)

## Workflows

These are some examples used for the tests.

### Simple MPI Workflow

`sr.c`: A test program from MPICH, that simply prints information about
the MPI ranks. Used to test that a MPI program is launched correctly on
HPCs with CWL.

[Report](./workflows/mpich-sr/README.md)

#### CWLTool

[Report](./workflows/mpich-sr/README-cwltool.md)

#### StreamFlow

[Report](./workflows/mpich-sr/README-streamflow.md)

#### Toil

[Report](./workflows/mpich-sr/README-toil.md)
