#!/usr/bin/env bash

echo "[HPC] Loading BSC MareNostrum5 environment"

module purge

# Singularity
module load singularity/4.1.5
# Python (MN5 module needs HDF5)
module load intel impi hdf5 mkl python/3.12.1
# NOTE: This is disabled because this module requires EasyBuild and Conda,
#       and pre-loads an EBMN5 conda env.
# NodeJS (so the CWL tests do not have to pull a Docker container for that)
# module load nodejs/20.9.0-GCCcore-13.2.0

# Other site-specific tweaks
# export TMPDIR=/scratch/$USER/tmp
# mkdir -p "$TMPDIR"
