#!/usr/bin/env cwl-runner

# SPDX-License-Identifier: CC-BY-4.0
#
# This file is licensed under CC BY 4.0
# https://creativecommons.org/licenses/by/4.0/
#
# Copyright (c) 2026 Bruno de Paula Kinoshita

cwlVersion: v1.2

# --- Metadata ---

$namespaces:
  s: https://schema.org/
  xsd: http://www.w3.org/2001/XMLSchema#

$schemas:
  - https://schema.org/version/latest/schemaorg-current-http.rdf

s:author:
  class: s:Person
  s:identifier: https://orcid.org/0000-0001-8250-4074
  s:email: mailto:bruno.depaulakinoshita@bsc.es
  s:name: Bruno de Paula Kinoshita

s:dateCreated:
  "@type": "xsd:date"
  "@value": "2026-02-13"

s:license: https://creativecommons.org/licenses/by/4.0/

s:codeRepository: https://github.com/kinow/cwl-mpi

# --- CWL Tool ---

id: mpich-mpicc
class: CommandLineTool
label: mpich-mpicc
baseCommand: mpicc
doc: >
  An example CWL tool that compiles a C program using the `mpicc`
  compiler wrapper.
  
  By default, it compiles the `sr.c` source file using the `mpicc`
  compiler wrapper. The tool can also be used to compile other
  C programs by providing a different value for source.
  
  It uses the MPICH 4.3.2 Docker image as a hint.

hints:
  DockerRequirement:
    dockerPull: mfisherman/mpich:4.3.2

requirements:
  InlineJavascriptRequirement: { }
  NetworkAccess:
    networkAccess: false
  ResourceRequirement:
    coresMin: 2
    ramMin: 512

inputs:
  source:
    type: File
    inputBinding:
      position: 1
    default:
      class: File
      path: sr.c
  output_name:
    type: string
    default: sr
    inputBinding:
      prefix: -o
      position: 2

outputs:
  executable:
    type: File
    outputBinding:
      glob: $(inputs.output_name)
