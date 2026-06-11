# SPDX-License-Identifier: CC-BY-4.0
#
# This file is licensed under CC BY 4.0
# https://creativecommons.org/licenses/by/4.0/
#
# Copyright (c) 2026 Bruno de Paula Kinoshita

SHELL := /bin/bash

TIMEOUT ?= 300

CWL_RUNNER ?= cwltool
DEBUG ?= 0

VALID_PLATFORMS := laptop mn5 lumi ft3 aws
PLATFORM ?=

ifndef PLATFORM
	$(error PLATFORM is not set. Example: make PLATFORM=mn5 CONTAINER=none run-all)
endif

ifeq ($(filter $(PLATFORM),$(VALID_PLATFORMS)),)
	$(error Invalid PLATFORM=$(PLATFORM))
endif

CONTAINER ?= none

ifeq ($(PLATFORM),laptop)
	VALID_CONTAINERS := none docker singularity
else ifeq ($(PLATFORM),aws)
	VALID_CONTAINERS := none docker
else
	VALID_CONTAINERS := none singularity
endif

ifeq ($(filter $(CONTAINER),$(VALID_CONTAINERS)),)
	$(error Invalid CONTAINER=$(CONTAINER) for PLATFORM=$(PLATFORM))
endif

ifeq ($(CONTAINER),singularity)
	CWL_CONTAINER_ARGS := --singularity
else ifeq ($(CONTAINER),none)
	CWL_CONTAINER_ARGS := --no-container
else
	CWL_CONTAINER_ARGS :=
endif

ifeq ($(DEBUG),1)
	CWL_DEBUG := --debug
else
	CWL_DEBUG :=
endif

ifneq ($(findstring streamflow,$(CWL_RUNNER)),)
    CWLTOOL_ARGS =
else
	CWLTOOL_ARGS = --strict-cpu-limit --strict-memory-limit --enable-ext
endif

LOGDIR := logs/$(CWL_RUNNER)/$(PLATFORM)/$(CONTAINER)

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

mpicc:
	$(call run_cwl,mpicc,$(CWL_MPICC))

mpirun-base: mpicc
	$(call run_cwl,mpirun-base,$(CWL_MPIRUN_BASE) --np 6)

mpirun-req: mpicc
	$(call run_cwl,mpirun-req,$(CWL_MPIRUN_REQ) --np 6)

workflow-base:
	$(call run_cwl,workflow-base,$(CWL_WORKFLOW_BASE) --np 6)

workflow-req:
	$(call run_cwl,workflow-req,$(CWL_WORKFLOW_REQ) --np 6)

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