#!/usr/bin/env cwl-runner
cwlVersion: v1.2

# SPDX-License-Identifier: CC-BY-4.0
#
# This file is licensed under CC BY 4.0
# https://creativecommons.org/licenses/by/4.0/
#
# Copyright (c) 2026 Bruno de Paula Kinoshita

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

id: mpirun-base-command
class: CommandLineTool
label: mpirun-base-command
baseCommand: mpirun
doc: >
  An example CWL tool that uses the MPICH 4.3.2 Docker image.
  By default, it runs the `sr` MPI program using 2 MPI processes.
  The base command of this tool is `mpirun`. If using cwltool or
  Toil, you can disable the use of containers with the flag
  `--no-container`.

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
  np:
    type: int
    default: 2
    inputBinding:
      prefix: -np
      position: 1
  executable:
    type: File
    inputBinding:
      position: 2
  msg_size:
    type: int
    default: 0
    inputBinding:
      position: 3
  niter:
    type: int
    default: 1
    inputBinding:
      position: 4

stdout: mpirun-base-command.out
stderr: mpirun-base-command.err

outputs:
  stdout_file:
    type: File
    outputBinding:
      glob: mpirun-base-command.out
  stderr_file:
    type: File
    outputBinding:
      glob: mpirun-base-command.err
