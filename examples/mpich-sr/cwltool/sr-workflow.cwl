#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: Workflow

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

label: Workflow to compile and run sr.c from mpich tests

inputs:
  source:
    type: File
  np:
    type: int
    default: 2
  msg_size:
    type: int
    default: 0
  niter:
    type: int
    default: 1

outputs:
  stdout:
    type: File
    outputSource: run/stdout_file
  stderr:
    type: File
    outputSource: run/stderr_file

steps:
  compile:
    run: compile-sr.cwl
    in:
      source: source
    out:
      [ executable ]
  run:
    run: run-sr-mpirun.cwl
    in:
      executable: compile/executable
      np: np
      msg_size: msg_size
      niter: niter
    out: [ stdout_file, stderr_file ]
