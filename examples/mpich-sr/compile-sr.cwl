cwlVersion: v1.2
class: CommandLineTool

$namespaces:
  s: https://schema.org/

$schemas:
 - https://schema.org/version/latest/schemaorg-current-http.rdf

s:author:
  - class: s:Person
    s:identifier: https://orcid.org/0000-0001-8250-4074
    s:email: mailto:sharpie-owl-frame@duck.com
    s:name: Bruno P. Kinoshita

s:codeRepository: https://github.com/kinow/cwl-mpi
s:dateCreated: "2026-02-13"
# s:license:

label: Compile sr.c with mpicc

requirements:
  DockerRequirement:
    dockerPull: mfisherman/mpich:4.3.2

baseCommand: mpicc

inputs:
  source:
    type: File
    inputBinding:
      position: 1
  output_name:
    type: string
    default: a.out
    inputBinding:
      prefix: -o
      position: 2

outputs:
  executable:
    type: File
    outputBinding:
      glob: $(inputs.output_name)
