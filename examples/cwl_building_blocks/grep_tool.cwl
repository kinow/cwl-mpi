cwlVersion: v1.2
class: CommandLineTool

baseCommand: grep

inputs:
  pattern:
    type: string
    inputBinding:
      position: 1

  infile:
    type: File
    inputBinding:
      position: 2

stdout: grep.log

outputs:
  matches:
    type: File
    outputBinding:
      glob: grep.log
