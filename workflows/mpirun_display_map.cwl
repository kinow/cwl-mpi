cwlVersion: v1.2

class: CommandLineTool
baseCommand: 'mpirun'
arguments:
  - -np
  - "8"
  - --display-map
  - hostname

inputs: []
outputs: []
