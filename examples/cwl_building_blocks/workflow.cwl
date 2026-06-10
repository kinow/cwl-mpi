cwlVersion: v1.2
class: Workflow

inputs:
  poem:
    type: File

outputs:
  cat_log:
    type: File
    outputSource: cat_step/text

  grep_log:
    type: File
    outputSource: grep_step/matches

steps:

  cat_step:
    run: cat.cwl
    in:
      infile: poem
    out:
      - text

  grep_step:
    run: grep_tool.cwl
    in:
      infile: cat_step/text
      pattern:
        default: terra
    out:
      - matches
