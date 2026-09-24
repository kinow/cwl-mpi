# Changelog

## 1.x.x -- unreleased

* **Slides** used in the thesis presentation have been added to this
  Git repository -- https://github.com/kinow/cwl-mpi/pull/28 &
  https://github.com/kinow/cwl-mpi/pull/27.
* CWL Conformance Tests using CWL version 1.0, Toil, executed on CESGA
  FinisTerrae III and a **dev branch of cwltest**, producing improved results
  (near perfect, against <50% from the thesis). There were new failures
  on LUMI, and a regression was identified in the new Toil 9.5.0 with
  a fix already in the works -- https://github.com/kinow/cwl-mpi/pull/31.
* CWL Conformance Tests using CWL version 1.0, cwltool, executed on
  **RIKEN Fugaku HPC** successfully on the x86 login node, and on a **PJM**
  ARM compute node -- https://github.com/kinow/cwl-mpi/pull/32.
* CWL workflow that runs MPICH `sr.c` test case tested successfully on
  RIKEN Fugaku using PJM and the **Fujitsu MPI** implementation
  -- https://github.com/kinow/cwl-mpi/pull/35.
* The thesis Zenodo dataset was evaluated with **F-UJI**, producing a
  **FAIRness score of 92%**, considered **"advanced"**; project README
  file updated with screenshots -- https://github.com/kinow/cwl-mpi/pull/33.
* Added this changelog -- https://github.com/kinow/cwl-mpi/pull/36.
* Handle from the **Universidade de Santiago de Compostela (USC)** 🥳🎉:
  https://hdl.handle.net/10347/48623.

## 1.0.0 -- 2026-06-25

* CWL Conformance Tests using CWL version 1.0, 1.1, and 1.2; runners **cwltool**,
  **Toil**, and **StreamFlow**; HPC's **CESGA FinisTerrae III**,
  **BSC MareNostrum 5**, and **CSC LUMI**.
* MPI Workflows using runners cwltool and Toil; HPC's CESGA FinisTerrae III,
  BSC MareNostrum 5, and CSC LUMI; a simple **MPICH** test case, and **FALL3D**
  workflow; **Intel MPI**, **Open MPI**, and **MPICH**; **Slurm**.
* Results report and analysis on use of CWL on HPC's, CWL with MPI and the
  **`cwltool:MPIRequirement`**, and **Singularity** containers.
* **Git Tag**: https://github.com/kinow/cwl-mpi/releases/tag/1.0.0.
* **Zenodo DOI**: https://zenodo.org/records/20348637 (includes **RO-Crate**).
* Thesis project delivered, and defended successfully 🥳🎉.
