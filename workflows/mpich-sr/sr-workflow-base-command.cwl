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

id: sr-workflow
class: Workflow
label: sr-workflow
doc: >
  A CWL workflow that runs the MPI `sr` program.
  
  It uses the `mpicc.cwl` and `mpirun-base-command.cwl` tools.
  
  The MPI program (`sr`) is executed with the `mpirun` base command.

steps:
  mpicc:
    run: mpicc.cwl
    in:
      source: source
    out:
      [ executable ]
  mpirun:
    run: sr-base-command.cwl
    in:
      executable: mpicc/executable
      np: np
      msg_size: msg_size
      niter: niter
    out: [ stdout_file, stderr_file ]

inputs:
  source:
    type: File
    default:
      class: File
      path: sr.c
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
    outputSource: mpirun/stdout_file
  stderr:
    type: File
    outputSource: mpirun/stderr_file
