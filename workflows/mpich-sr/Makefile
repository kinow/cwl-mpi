# SPDX-License-Identifier: CC-BY-4.0
#
# This file is licensed under CC BY 4.0
# https://creativecommons.org/licenses/by/4.0/
#
# Copyright (c) 2026 Bruno de Paula Kinoshita

CWL_RUNNER ?= cwltool

# Enable with: make SINGULARITY=1
SINGULARITY ?= 0
ifeq ($(SINGULARITY),1)
	CWL_SINGULARITY = --singularity
else
	CWL_SINGULARITY = --no-container
endif

DEBUG ?= 0
ifeq ($(DEBUG),1)
	CWL_DEBUG = --debug
else
	CWL_DEBUG =
endif

CWLTOOL_ARGS = --strict-cpu-limit --strict-memory-limit
CWLTOOL_EXT = --enable-ext

ifneq ($(findstring streamflow,$(CWL_RUNNER)),)
	CWLTOOL_ARGS =
	CWLTOOL_EXT =
endif

CWL_MPICC = mpich-mpicc.cwl
# Uses mpirun as base command.
CWL_MPIRUN_BASE = mpich-mpirun-base-command.cwl
# Uses MPIRequirement.
CWL_MPIRUN_REQ = mpich-mpirun-mpi-requirement.cwl
# Workflow that calls mpich-mpirun-base-command.cwl
CWL_WORKFLOW_BASE = workflow-base-command.cwl
# Workflow that calls mpich-mpirun-mpi-requirement.cwl
CWL_WORKFLOW_REQ = workflow-mpi-requirement.cwl

BINARY = sr \
	a.out

OUT_FILES = \
	$(BINARY) \
	*.out \
	*.err

.PHONY: all build run clean mpicc mpirun-base mpirun-requirement

all: build

build: clean mpicc

mpicc:
	@echo "→ $@"
	$(CWL_RUNNER) $(CWL_SINGULARITY) $(CWL_DEBUG) $(CWLTOOL_ARGS) $(CWL_MPICC)

mpirun-base:
	@echo "→ $@"
	$(CWL_RUNNER) $(CWL_SINGULARITY) $(CWL_DEBUG) $(CWLTOOL_ARGS) $(CWL_MPIRUN_BASE) --np 2

mpirun-req:
	@echo "→ $@"
	$(CWL_RUNNER) $(CWL_SINGULARITY) $(CWL_DEBUG) $(CWLTOOL_EXT) $(CWLTOOL_ARGS) $(CWL_MPIRUN_REQ) --np 2

workflow-base:
	@echo "→ $@"
	$(CWL_RUNNER) $(CWL_SINGULARITY) $(CWL_DEBUG) $(CWLTOOL_EXT) $(CWLTOOL_ARGS) $(CWL_WORKFLOW_BASE) --np 2

workflow-req:
	@echo "→ $@"
	$(CWL_RUNNER) $(CWL_SINGULARITY) $(CWL_DEBUG) $(CWLTOOL_EXT) $(CWLTOOL_ARGS) $(CWL_WORKFLOW_REQ) --np 2

clean:
	rm -f $(OUT_FILES)
