cwlVersion: v1.2
class: CommandLineTool

baseCommand: bash

arguments:
  - -c
  - |
    echo "USER=`whoami`"
    echo "HOME=$HOME"
    pwd

    ls -la ~/.pmix || true
    cat ~/.pmix/mca-params.conf || true

    echo
    echo "=== MPI TEST ==="
    mpirun --display-map -np 8 hostname 2>&1

stdout: out.txt

inputs: []
outputs:
  out:
    type: stdout