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
