#!/usr/bin/env bash

echo "[HPC] Loading CESGA FinisTerrae III environment"

module purge

# Singularity
module load cesga/2020 singularity/4.2.2
# Python
module load python/3.10.8
# NodeJS (faster than CWL downloading the NodeJS Singularity containers)
module load nodejs/20.9.0

# Other site-specific tweaks
# export TMPDIR=/scratch/$USER/tmp
# mkdir -p "$TMPDIR"
