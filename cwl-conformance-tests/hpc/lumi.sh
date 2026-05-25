#!/usr/bin/env bash

echo "[HPC] Loading CSC LUMI environment"

module purge

# Singularity
# Loaded by default!
# Python
# module load cray-python/3.11.7
eval "$(micromamba shell hook -s bash)"
micromamba activate python-3.13
# No NodeJS module on LUMI
# module load node...

# Other site-specific tweaks
# export TMPDIR=/scratch/$USER/tmp
# mkdir -p "$TMPDIR"
