cwlVersion: v1.2
class: CommandLineTool

baseCommand: cat

inputs:
  infile:
    type: File
    inputBinding:
      position: 1

stdout: cat.log

outputs:
  text:
    type: File
    outputBinding:
      glob: cat.log
