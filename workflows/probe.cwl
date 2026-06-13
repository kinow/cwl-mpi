cwlVersion: v1.2
class: CommandLineTool

doc: "A CWL tool to probe the MPI environment."

baseCommand: [ bash, -c ]

inputs: [ ]
outputs: [ ]

arguments:
  - |
    hostname
    which mpicc
    mpicc -show
    env | sort
