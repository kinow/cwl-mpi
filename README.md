# CWL MPI

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20348637.svg)](https://doi.org/10.5281/zenodo.20348637)

This repository contains Common Workflow Language (CWL) workflows that use MPI.
They were developed for testing and demonstration purposes as part of the master's
thesis by [Bruno de Paula Kinoshita](https://orcid.org/0000-0001-8250-4074),
completed within the [Joint Master in High Performance Computing](https://www.usc.gal/en/studies/masters/engineering-and-architecture/master-high-performance-computing-online)
offered by the [Universities of Santiago de Compostela](https://www.usc.gal/)
and [A Coruña](https://udc.es/). The thesis, “CWL Workflows with MPI in Bare-Metal,
Containers, Cloud, and HPC Environments”, explores the use of MPI-enabled CWL workflows
across a range of computing platforms.

## CWL Conformance Tests

Results and reports for CWL conformance testing.

[Report](./cwl-conformance-tests/README.md)

## Workflows

Example workflows used throughout the tests and evaluations.

### Simple MPI Workflow

`sr.c`: is a test program from MPICH that prints information about MPI ranks.
It is used to verify that MPI applications can be launched correctly through
CWL on HPC systems.

* [cwltool](./workflows/mpich-sr/README-cwltool.md)
* [Toil](./workflows/mpich-sr/README-toil.md)
* [StreamFlow](./workflows/mpich-sr/README-streamflow.md)

For a description of the workflow and its files, see the main report:

[Workflow Report](./workflows/mpich-sr/README.md)

