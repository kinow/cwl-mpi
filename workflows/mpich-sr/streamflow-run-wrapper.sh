#!/usr/bin/env bash

# SPDX-License-Identifier: CC-BY-4.0
#
# This file is licensed under CC BY 4.0
# https://creativecommons.org/licenses/by/4.0/
#
# Copyright (c) 2026 Bruno de Paula Kinoshita

# A StreamFlow wrapper to match the cwltool and toil-cwl-runner command-line API.

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 [--debug] WORKFLOW.cwl [SETTINGS.yml] [--singularity]"
    exit 1
fi

cwl_file=""
settings=""
use_singularity=false
debug=false

# Loop through all arguments dynamically
for arg in "$@"; do
    case "$arg" in
    --singularity)
        use_singularity=true
        ;;
    --debug)
        debug=true
        ;;
    *.cwl)
        cwl_file="$(realpath "$arg")"
        ;;
    *.yml | *.yaml)
        settings="$(realpath "$arg")"
        ;;
    *)
        # Strict fallback: Only assign the CWL file if we don't have one yet.
        # Everything else (like --np, or standalone numbers like 2) is ignored.
        if [[ -z "$cwl_file" ]]; then
            cwl_file="$(realpath "$arg")"
        fi
        ;;
    esac
done

# Safety check to ensure a CWL file was actually provided
if [[ -z "$cwl_file" ]]; then
    echo "Error: No CWL workflow file provided."
    exit 1
fi

wrapper=$(mktemp)
trap 'rm -f "$wrapper"' EXIT

cat >"$wrapper" <<EOF
version: v1.0
workflows:
  workflow_name:
    type: cwl
    config:
      file: "$cwl_file"
EOF

# This will now remain empty and clean unless a true .yml/.yaml file was passed
if [[ -n "$settings" ]]; then
    cat >>"$wrapper" <<EOF
      settings: "$settings"
EOF
fi

if [[ "$use_singularity" == true ]]; then
    cat >>"$wrapper" <<'EOF'
      docker:
        - step: /
          deployment:
            type: singularity
            config: {}
EOF
fi

printf "StreamFlow file:\n\n"
cat "$wrapper"
printf "\n\n"

# Construct the streamflow command dynamically
cmd=(streamflow run)
if [[ "$debug" == true ]]; then
    cmd+=(--debug)
fi

# Add only the wrapper generated file
cmd+=("$wrapper")

# Execute the clean command
echo "Executing: ${cmd[*]}"
"${cmd[@]}"
