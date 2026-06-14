#!/usr/bin/env bash
set -euo pipefail

#############################################
# Recursively redact HPC_USER and HPC_PROJECT
# in all text files under a directory.
# Replaces matches with: [REDACTED]
#############################################

##############################
# Logging
##############################
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# -----------------------------
# Check required environment
# -----------------------------
if [[ -z "${HPC_USER:-}" ]]; then
    log "ERROR: HPC_USER is not set"
    exit 1
fi

if [[ -z "${HPC_PROJECT:-}" ]]; then
    log "ERROR: HPC_PROJECT is not set"
    exit 1
fi

# -----------------------------
# Check arguments
# -----------------------------
if [[ $# -ne 1 ]]; then
    log "Usage: $0 <directory>"
    exit 1
fi

INPUT_DIR="$1"

if [[ ! -d "$INPUT_DIR" ]]; then
    log "ERROR: Not a directory: $INPUT_DIR"
    exit 1
fi

REDACT="[REDACTED]"

log "Redacting in: $INPUT_DIR"
log "Replacing: HPC_USER and HPC_PROJECT -> $REDACT"

# -----------------------------
# Safe escaping for sed
# -----------------------------
escape_sed() {
    printf '%s' "$1" | sed -e 's/[\/&|]/\\&/g'
}

USER_ESCAPED=$(escape_sed "$HPC_USER")
PROJ_ESCAPED=$(escape_sed "$HPC_PROJECT")

# -----------------------------
# Process files
# -----------------------------
find "$INPUT_DIR" -type f -print0 | while IFS= read -r -d '' file; do

    # Skip binary files (basic heuristic)
    if grep -Iq . "$file"; then
        sed -i \
            -e "s|$USER_ESCAPED|$REDACT|g" \
            -e "s|$PROJ_ESCAPED|$REDACT|g" \
            "$file"
    fi

done

log "Done."
