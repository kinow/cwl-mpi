#!/usr/bin/env bash

echo "[HPC] Loading CESGA FinisTerrae III environment"

module purge

# Singularity
module load cesga/2020 singularity/4.2.2
# Python, with the CESGA FT3 module, cwltool works, but Toil fails with
# ModuleNotFoundError: No module named '_curses'
# module load python/3.10.8
eval "$(micromamba shell hook -s bash)"
micromamba activate python-3.13
# NodeJS (faster than CWL downloading the NodeJS Singularity containers)
# module load nodejs/20.9.0

# Other site-specific tweaks
# export TMPDIR=/scratch/$USER/tmp
# mkdir -p "$TMPDIR"
