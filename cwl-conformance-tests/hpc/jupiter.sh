#!/usr/bin/env bash

echo "[HPC] Loading JSC JUPITER BOOSTER environment"

# Singularity is already loaded
# Micromamba
eval "$(micromamba shell hook -s bash)"
micromamba activate python-3.13
