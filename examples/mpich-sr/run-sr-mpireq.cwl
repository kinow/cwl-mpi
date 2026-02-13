#!/usr/bin/env cwltool
cwlVersion: v1.2
class: CommandLineTool

# Refs:
# - https://cwltool.readthedocs.io/en/latest/index.html#running-mpi-based-tools-that-need-to-be-launched

$namespaces:
  cwltool: "http://commonwl.org/cwltool#"
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

label: Run compiled sr using mpirun

requirements:
  DockerRequirement:
    dockerPull: mfisherman/mpich:4.3.2
  cwltool:MPIRequirement:
    processes: $(inputs.np)

baseCommand: [$(inputs.executable.path)]

inputs:
  np:
    type: int
    default: 2
  executable:
    type: File
  msg_size:
    type: int
    default: 0
    inputBinding:
      position: 1
  niter:
    type: int
    default: 1
    inputBinding:
      position: 2

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
