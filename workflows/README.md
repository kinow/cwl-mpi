# CWL+MPI Workflows

This folder contains CWL workflows and tools written for the thesis.

These CWL workflows and tools are written using CWL, validated
using `cwltool`, and run on different platforms.

They are meant to be used as a reference as introduction for CWL, and
for the integration of MPI in CWL.

## hello_world

A Hello World CWL program. This is the Hello World CWL example used in
an appendix of the thesis, linked from the Background section.

## mpich-sr

This is the Simple Workflow example used in the thesis. It runs MPICH
`sr.c` test program. It contains different versions of the tools and
workflows. One version runs `baseCommand: mpirun`, whereas the other
version uses `cwltool:MPIRequirement`.

## FALL3D

This folder does not contain an original workflow. In the thesis, FALL3D
(a volcanic ash model) was used as a scientific application use case.
We used the FALL3D workflow from the GEO3BCN
[getit-workflows](https://gitlab.geo3bcn.csic.es/fall3d/getit-workflows).
The original workflow uses `baseCommand: mpirun`. The version created
in this folder uses `cwltool:MPIRequirement`. It was sent via a merge
request to the original repository and kept here for traceability in
the thesis.

## Other files

- [`probe.cwl`](./probe.cwl) A CWL tool that uses bash to print MPI system information.
- [`mpirun_display_map.cwl`](./mpirun_display_map.cwl) A CWL tool that runs `hostname` with `mpirun`,
  showing the host mapping.
- [`mpirun_hostname.cwl`](./mpirun_hostname.cwl) A CWL tool that runs `hostname` with `mpirun`,
  shows the host mapping and other system information (useful with multi-node runs).
