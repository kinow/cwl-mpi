#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: CommandLineTool

$namespaces:
  s: https://schema.org/
  xsd: http://www.w3.org/2001/XMLSchema#

$schemas:
 - https://schema.org/version/latest/schemaorg-current-http.rdf

s:author:
  class: s:Person
  s:identifier:
    "@type": "@id"
    "@value": "https://orcid.org/0000-0001-8250-4074"
  s:email:
    "@type": "@id"
    "@value": "mailto:sharpie-owl-frame@duck.com"
  s:name:
    "@type": "xsd:string"
    "@value": "Bruno P. Kinoshita"

s:codeRepository:
  "@type": "@id"
  "@value": "https://github.com/kinow/cwl-mpi"
s:dateCreated:
  "@type": "xsd:date"
  "@value": "2026-02-13"
s:license:
  "@type": "xsd:string"
  "@value": "private"
#s:license:
#  "@type": "@id"
#  "@value": "https://opensource.org/licenses/MIT"

requirements:
  ShellCommandRequirement: {}
  InlineJavascriptRequirement: {}
  ResourceRequirement:
    coresMin: 2
  DockerRequirement:
    dockerPull: mfisherman/mpich:4.3.2

label: Run compiled sr using mpirun

baseCommand: []

inputs:
  launcher:
    type: string
    default: mpirun  # mpirun, srun, ...
    inputBinding:
      position: 1
  np:
    type: int?
    inputBinding:
      prefix: "-np"
      position: 2
  executable:
    type: File
    inputBinding:
      position: 3
  msg_size:
    type: int
    default: 0
    inputBinding:
      position: 4
  niter:
    type: int
    default: 1
    inputBinding:
      position: 5

stdout: sr.out
stderr: sr.err

outputs:
  stdout_file:
    type: File
    outputBinding:
      glob: sr.out
  stderr_file:
    type: File
    outputBinding:
      glob: sr.err
