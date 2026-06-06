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
    ifneq ($(findstring streamflow,$(CWL_RUNNER)),)
        CWL_SINGULARITY =
    else
        CWL_SINGULARITY = --no-container
    endif
endif

DEBUG ?= 0
ifeq ($(DEBUG),1)
    ifneq ($(findstring toil,$(CWL_RUNNER)),)
        CWL_DEBUG = --logDebug
    else
        CWL_DEBUG = --debug
    endif
else
    CWL_DEBUG =
endif

ifneq ($(findstring streamflow,$(CWL_RUNNER)),)
    CWLTOOL_ARGS =
    CWLTOOL_EXT =
else
	CWLTOOL_ARGS = --strict-cpu-limit --strict-memory-limit
	CWLTOOL_EXT = --enable-ext
endif

CWL_MPICC = mpicc.cwl
# Uses mpirun as base command.
CWL_MPIRUN_BASE = sr-base-command.cwl
# Uses MPIRequirement.
CWL_MPIRUN_REQ = sr-mpi-requirement.cwl
# Workflow that calls sr-workflow-base-command.cwl
CWL_WORKFLOW_BASE = sr-workflow-base-command.cwl
# Workflow that calls sr-workflow-mpi-requirement.cwl
CWL_WORKFLOW_REQ = sr-workflow-mpi-requirement.cwl

BINARY = sr \
    a.out

.PHONY: all build clean \
    mpicc mpirun-base mpirun-req \
    workflow-base workflow-req \
    run-all

ifeq ($(SINGULARITY),1)
    LOGDIR = logs/$(CWL_RUNNER)/singularity
else
    LOGDIR = logs/$(CWL_RUNNER)/nosingularity
endif

all: build

build: mpicc

# ------------------------
# Helper macro for logging
# ------------------------
define run_cwl
	@echo "→ $(1)"
	@mkdir -p "$(LOGDIR)"
	@bash -c 'set -o pipefail; \
	   $(CWL_RUNNER) $(CWL_SINGULARITY) $(CWL_DEBUG) $(CWLTOOL_ARGS) $(2) \
	   > "$(LOGDIR)/$(1).out" 2> "$(LOGDIR)/$(1).err"; \
	   STATUS=$$?; \
	   echo $$STATUS > "$(LOGDIR)/$(1).exit"; \
	   exit $$STATUS'
endef

# ------------------------
# Targets (With Explicit Dependencies)
# ------------------------

# mpicc generates the local 'sr' binary
mpicc:
	$(call run_cwl,mpicc,$(CWL_MPICC))

# Standalone runs must depend on mpicc so the 'sr' binary exists
mpirun-base: mpicc
	$(call run_cwl,mpirun-base,$(CWL_MPIRUN_BASE) --np 2)

mpirun-req: mpicc
	$(call run_cwl,mpirun-req,$(CWLTOOL_EXT) $(CWL_MPIRUN_REQ) --np 2)

# Workflows compile internally, so they can run independently
workflow-base:
	$(call run_cwl,workflow-base,$(CWLTOOL_EXT) $(CWL_WORKFLOW_BASE) --np 2)

workflow-req:
	$(call run_cwl,workflow-req,$(CWLTOOL_EXT) $(CWL_WORKFLOW_REQ) --np 2)

# ------------------------
# Run all
# ------------------------
run-all:
	@echo "→ running all tests without Singularity"
	-$(MAKE) SINGULARITY=0 CWL_RUNNER=$(CWL_RUNNER) DEBUG=$(DEBUG) mpicc
	-$(MAKE) SINGULARITY=0 CWL_RUNNER=$(CWL_RUNNER) DEBUG=$(DEBUG) mpirun-base
	-$(MAKE) SINGULARITY=0 CWL_RUNNER=$(CWL_RUNNER) DEBUG=$(DEBUG) mpirun-req
	-$(MAKE) SINGULARITY=0 CWL_RUNNER=$(CWL_RUNNER) DEBUG=$(DEBUG) workflow-base
	-$(MAKE) SINGULARITY=0 CWL_RUNNER=$(CWL_RUNNER) DEBUG=$(DEBUG) workflow-req

	@echo "→ running all tests with Singularity"
	-$(MAKE) SINGULARITY=1 CWL_RUNNER=$(CWL_RUNNER) DEBUG=$(DEBUG) mpicc
	-$(MAKE) SINGULARITY=1 CWL_RUNNER=$(CWL_RUNNER) DEBUG=$(DEBUG) mpirun-base
	-$(MAKE) SINGULARITY=1 CWL_RUNNER=$(CWL_RUNNER) DEBUG=$(DEBUG) mpirun-req
	-$(MAKE) SINGULARITY=1 CWL_RUNNER=$(CWL_RUNNER) DEBUG=$(DEBUG) workflow-base
	-$(MAKE) SINGULARITY=1 CWL_RUNNER=$(CWL_RUNNER) DEBUG=$(DEBUG) workflow-req

	@echo "→ run-all complete"

clean:
	rm -f $(BINARY) *.out *.err
	rm -rf logs/
