# SPDX-License-Identifier: CC-BY-4.0
#
# This file is licensed under CC BY 4.0
# https://creativecommons.org/licenses/by/4.0/
#
# Copyright (c) 2026 Bruno de Paula Kinoshita

SHELL := /bin/bash

TIMEOUT ?= 30

CWL_RUNNER ?= cwltool
DEBUG ?= 0

# Set the platform to be used. Laptop is for bare-metal,
# mn5, lumi, and ft3 are HPCs, and cloud is the cloud provider (herzog, etc.).
VALID_PLATFORMS := laptop mn5 lumi ft3 cloud
PLATFORM ?=
ifndef PLATFORM
	$(error PLATFORM is not set. Example: make PLATFORM=mn5 CONTAINER=none run-all)
endif
ifeq ($(filter $(PLATFORM),$(VALID_PLATFORMS)),)
	$(error Invalid PLATFORM=$(PLATFORM))
endif

# Set the container to be used. Valid values are Docker or Singularity.
# If using Apptainer, set to Singularity is Apptainer ships with a Singularity
# binary. none means to use the local environment files (i.e. no container used).
CONTAINER ?= none
ifeq ($(PLATFORM),laptop)
	VALID_CONTAINERS := none docker singularity
else ifeq ($(PLATFORM),cloud)
	VALID_CONTAINERS := none docker
else
	VALID_CONTAINERS := none singularity
endif
ifeq ($(filter $(CONTAINER),$(VALID_CONTAINERS)),)
	$(error Invalid CONTAINER=$(CONTAINER) for PLATFORM=$(PLATFORM))
endif
# NOTE: cwltool and Toil both default to using Docker when the requirement
#       or hint is used. --singularity enables Singularity in both.
#       StreamFlow requires a deployment with the correct type. So out
#       wrapper script takes a --container=? argument for that.
ifneq ($(findstring streamflow,$(CWL_RUNNER)),)
	CWL_CONTAINER_ARGS := --container=$(CONTAINER)
else
	ifeq ($(CONTAINER),singularity)
		CWL_CONTAINER_ARGS := --singularity
	else ifeq ($(CONTAINER),none)
		CWL_CONTAINER_ARGS := --no-container
	else
		CWL_CONTAINER_ARGS :=
	endif
endif

# Set the debugging level to be used. Toil expects --logDebug.
# StreamFlow and cwltool accept --debug.
ifeq ($(DEBUG),1)
	ifneq ($(findstring toil,$(CWL_RUNNER)),)
		CWL_DEBUG := --logDebug
	else
		CWL_DEBUG := --debug
	endif
else
	CWL_DEBUG :=
endif

# Set the CWL runner arguments (similar to EXTRA in the CWL Conformance Tests).
# The RUNNER_NAME variable is set for convenience, to save the log output directory
# with a name like toil, instead of toil-cwl-runner.
ifneq ($(findstring streamflow,$(CWL_RUNNER)),)
	RUNNER_NAME := streamflow
	CWLTOOL_ARGS =
else ifneq ($(findstring toil,$(CWL_RUNNER)),)
	RUNNER_NAME := toil
	CWLTOOL_ARGS = --strict-cpu-limit --strict-memory-limit --enable-ext --bypass-file-store --disable-streaming --retryCount 0 --mpi-config-file mpi-config-file.yml
else
	RUNNER_NAME := $(CWL_RUNNER)
	CWLTOOL_ARGS = --strict-cpu-limit --strict-memory-limit --enable-ext --mpi-config-file mpi-config-file.yml
endif

# Set the log output directory. This is where we keep the outputs of
# the tools and workflows. This directory is Git-ignored. After the
# runs complete, they are manually inspected and then copied to the
# final directory output/, where these files are finally archived
# for posterity.
LOGDIR := logs/$(RUNNER_NAME)/$(PLATFORM)/$(CONTAINER)
ifneq ($(findstring toil,$(CWL_RUNNER)),)
	CWLTOOL_ARGS += --outdir=$(LOGDIR) --workDir=$(LOGDIR) --writeLogs=$(LOGDIR) --jobStore=$(LOGDIR)/$(shell uuidgen) --writeLogs=$(LOGDIR)
else
	CWLTOOL_ARGS += --outdir=$(LOGDIR)
endif

# CWL files used by Make target.
CWL_MPICC = mpicc.cwl
CWL_MPIRUN_BASE = sr-base-command.cwl
CWL_MPIRUN_REQ = sr-mpi-requirement.cwl
CWL_WORKFLOW_BASE = sr-workflow-base-command.cwl
CWL_WORKFLOW_REQ = sr-workflow-mpi-requirement.cwl

BINARY := sr a.out

.PHONY: run-all mpicc mpirun-base mpirun-req workflow-base workflow-req clean prepare

# The run_cwl function has a "Poor man's walltime checker similar to Slurm, using
# the Linux timeout utility.
define run_cwl
	@echo "→ $(1)"
	@mkdir -p "$(LOGDIR)"
	@echo "COMMAND: $(CWL_RUNNER) $(CWL_CONTAINER_ARGS) $(CWL_DEBUG) $(CWLTOOL_ARGS) $(2)" \
		> "$(LOGDIR)/$(1).cmd"
	START=$$(date +%s); \
	timeout --kill-after=30s $(TIMEOUT)s $(CWL_RUNNER) \
		$(CWL_CONTAINER_ARGS) \
		$(CWL_DEBUG) \
		$(CWLTOOL_ARGS) \
		$(2) \
	> "$(LOGDIR)/$(1).log" 2>&1 ; \
	EXIT=$$? ; \
	END=$$(date +%s); \
	DURATION=$$((END - START)); \
	echo "$$DURATION" > "$(LOGDIR)/$(1).time"; \
	if [ $$EXIT -eq 124 ]; then \
		echo "timeout" > "$(LOGDIR)/$(1).exit"; \
	elif [ $$EXIT -eq 137 ]; then \
		echo "killed" > "$(LOGDIR)/$(1).exit"; \
	else \
		echo $$EXIT > "$(LOGDIR)/$(1).exit"; \
	fi
endef

# --- Makefile targets
#     These simply resolve to a CWL file, and call the run_cwl function.

mpicc:
	$(call run_cwl,mpicc,$(CWL_MPICC))

mpirun-base: mpicc
	$(call run_cwl,mpirun-base,$(CWL_MPIRUN_BASE) --executable $(LOGDIR)/sr --np 6)

mpirun-req: mpicc
	$(call run_cwl,mpirun-req,$(CWL_MPIRUN_REQ) --executable $(LOGDIR)/sr --np --np 6)

workflow-base:
	$(call run_cwl,workflow-base,$(CWL_WORKFLOW_BASE) --np 6)

workflow-req:
	$(call run_cwl,workflow-req,$(CWL_WORKFLOW_REQ) --np 6)

# These extra targets are used for testing the environment health (run-all),
# and for running the tests in each environment (run-workflows)

run-all:
	@echo "Platform=$(PLATFORM) Container=$(CONTAINER) Runner=$(CWL_RUNNER)"
	-$(MAKE) mpicc
	-$(MAKE) mpirun-base
	-$(MAKE) mpirun-req
	-$(MAKE) workflow-base
	-$(MAKE) workflow-req
	@echo ""
	@echo "================ REPORT ================"
	@$(MAKE) report

run-workflows:
	@echo "Platform=$(PLATFORM) Container=$(CONTAINER) Runner=$(CWL_RUNNER)"
	-$(MAKE) workflow-base
	-$(MAKE) workflow-req
	@echo ""
	@echo "================ REPORT ================"
	@$(MAKE) report

# A handy target that summarizes and prints the experiment statuses.

report:
	@echo "===================================================="
	@echo " Experiment report (with timing)"
	@echo "===================================================="
	@printf "%-20s %-10s %-10s\n" "TEST" "RESULT" "TIME(s)"
	@echo "----------------------------------------------------"
	@find "$(LOGDIR)" -name "*.exit" | sort | while read f; do \
		name=$$(basename "$$f" .exit); \
		status=$$(cat "$$f"); \
		timefile="$(LOGDIR)/$$name.time"; \
		if [ -f "$$timefile" ]; then \
			time=$$(cat "$$timefile"); \
		else \
			time="-"; \
		fi; \
		printf "%-20s %-10s %-10s\n" "$$name" "$$status" "$$time"; \
	done

clean:
	rm -rf logs $(BINARY)
