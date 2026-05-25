#!/usr/bin/env bash

set -u
set -o pipefail

##########################################################################################
# CWL repositories are cloned once.
# Python virtual environments are created once per tool.
# Test runs reuse both CWL repositories and Python virtual environments.
#
# This script requires Internet connection and at least Python, Git, and Singularity.
# See the ``./hpc/`` folder for reference scripts for each HPC tested. Those scripts
# contain the required ``module`` statements and any other site-specific tweaks.
##########################################################################################

# Ensures that unicode (including emojis🎉) is properly represented on the command line
export PYTHONIOENCODING=utf8

# Disables Python's fault handler to avoid harmless shutdown noise from CWL tools
# (prevents non-fatal destructor errors from appearing during interpreter shutdown on HPC systems)
# e.g., on MN5 this test consistently fails:
# cwltool --singularity --enable-dev \
#   --tmpdir-prefix=/gpfs/scratch/$bscproject/$bscuser \
#   runs/specs/v1.1/tests/optional-numerical-output-0.cwl \
#   runs/specs/v1.1/tests/empty.json
#
# with:
#
# 
export PYTHONFAULTHANDLER=0

##############################
# Logging
##############################
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

##############################
# HPC environment selection
##############################

if [ -z "${HPC:-}" ]; then
    log "ERROR: HPC environment not specified."
    log "Usage: HPC=<name> $0"
    log "Example: HPC=mn5 $0"
    exit 1
fi

HPC_FILE="$(pwd)/hpc/${HPC}.sh"

if [ ! -f "$HPC_FILE" ]; then
    log "ERROR: HPC config not found: $HPC_FILE"
    exit 1
fi

log "Loading HPC environment: $HPC"
# shellcheck disable=SC1090
source "$HPC_FILE"

if [ -z "${HPC_SCRATCH_DIR:-}" ]; then
    log "ERROR: HPC_SCRATCH_DIR not defined."
    log "Please define it in hpc/${HPC}.sh or export it before running this script"
    exit 1
fi

##############################
# Configuration
##############################

# CWL versions to test
CWL_VERSIONS=("v1.0" "v1.1" "v1.2")
#CWL_VERSIONS=("v1.0")

# How many tests we will run in parallel
N_TESTS_IN_PARALLEL=16

# CWL repo URLs
declare -A CWL_REPO
CWL_REPO[v1.0]="https://github.com/common-workflow-language/common-workflow-language"
CWL_REPO[v1.1]="https://github.com/common-workflow-language/cwl-v1.1"
CWL_REPO[v1.2]="https://github.com/common-workflow-language/cwl-v1.2"

# Exact tags to use
declare -A CWL_TAG
CWL_TAG[v1.0]="v1.0.2"
CWL_TAG[v1.1]="v1.1.0"
CWL_TAG[v1.2]="v1.2.1"

# Tools configuration
# TOOLS=("cwltool" "toil")
TOOLS=("cwltool")
#TOOLS=("streamflow")

# NOTE: We are using declare here, which will not work with MacOS'
#       default Shell (bash in MacOS may be an alias to another
#       Shell, or to a much older version of Bash than on Linux).

# Tool binaries
declare -A TOOL_BIN
TOOL_BIN[cwltool]="cwltool"
TOOL_BIN[toil]="toil-cwl-runner"
TOOL_BIN[streamflow]="toil-cwl-runner"

# Extra args passed to the binaries
declare -A TOOL_ARGS
TOOL_ARGS[cwltool]="--singularity --enable-dev --tmpdir-prefix=$HPC_SCRATCH_DIR"
TOOL_ARGS[toil]="--singularity --disableCaching --disableProgress"

# Base working directory
BASE_DIR=$(pwd)/runs
mkdir -p "$BASE_DIR"

RUN_ID=$(date '+%Y%m%d-%H%M%S')
SUMMARY_FILE="$BASE_DIR/summary-$RUN_ID.txt"

log "Run ID: $RUN_ID"
log "Base directory: $BASE_DIR"
log "HPC: $HPC"

##############################
# Python environment setup
##############################

setup_python_env() {
    TOOL="$1"
    ENV_DIR="$BASE_DIR/venv-$TOOL"

    if [ -d "$ENV_DIR" ]; then
        log "Reusing venv for $TOOL"
        return
    fi

    python3 -m venv "$ENV_DIR"
    "$ENV_DIR/bin/pip" install --upgrade pip
    "$ENV_DIR/bin/pip" install cwltest

    case "$TOOL" in
        cwltool)
            "$ENV_DIR/bin/pip" install cwltool
            ;;
        toil)
            "$ENV_DIR/bin/pip" install toil[cwl]
            ;;
    esac
}

##############################
# Clone CWL specs
##############################

clone_cwl_repo() {
    VERSION="$1"
    DEST="$BASE_DIR/specs/$VERSION"

    REPO="${CWL_REPO[$VERSION]}"
    TAG="${CWL_TAG[$VERSION]}"

    log "Preparing $VERSION ($TAG)"

    # If repo exists, force correct state
    if [ -d "$DEST/.git" ]; then
        log "Updating existing CWL $VERSION repo"

        git -C "$DEST" fetch --tags origin
        git -C "$DEST" checkout "$TAG"

        return
    fi

    # If folder exists but is NOT a git repo then remove it
    if [ -d "$DEST" ]; then
        log "Removing broken/partial repo for $VERSION"
        rm -rf "$DEST"
    fi

    log "Cloning $VERSION ($TAG)"

    # NOTE: HPCs (e.g. CESGA FT3) have a tight quota on file size and number of
    #       inodes used. So the whole script is made to minimize files used.
    if ! git clone \
            --depth 1 \
            --branch "$TAG" \
            --single-branch \
            "$REPO" \
            "$DEST"; then
        log "ERROR: Failed to clone $VERSION"
        exit 1
    fi

    # In case we have problems with inodes (like on CESGA FT3) we can delete the
    # Git directory after cloning, ``rm -rf "$DEST/.git"``.
}

##############################
# Run tests
##############################

run_tests() {
    TOOL="$1"
    VERSION="$2"
    MODE="$3"

    TOOL_DIR="$BASE_DIR/$TOOL/$VERSION/$MODE"
    mkdir -p "$TOOL_DIR"

    LOG_FILE="$TOOL_DIR/run.log"

    log "Running $TOOL on $VERSION ($MODE)"

    # We run each test within a subshell.
    START_TIME=$(date +%s)
    (
        cd "$BASE_DIR/specs/$VERSION" || exit 1
        if [ "$VERSION" = "v1.0" ]; then
          # This is the only exception, 1.1, 1.2, follow a new pattern...
          cd v1.0/
        fi

        # v1.1 and v1.2 run_test.sh did not work on LUMI, MN5, and CESGA FT3.
        # TEST_SCRIPT="$BASE_DIR/specs/$VERSION/run_test.sh"
        TEST_SCRIPT=cwltest

        # shellcheck disable=SC1090
        source "$BASE_DIR/venv-$TOOL/bin/activate"

        RUNNER="${TOOL_BIN[$TOOL]}"
        EXTRA="${TOOL_ARGS[$TOOL]}"

        if [ "$TOOL" = "toil" ] && [ "$MODE" = "slurm" ]; then
            EXTRA="${EXTRA} --batchSystem slurm"
        fi

        TEST_FILE="conformance_tests.yaml"
        if [ "$VERSION" = "v1.0" ]; then
          TEST_FILE="conformance_test_v1.0.yaml"
        fi

        # Build base args
        ARGS=(
            "--verbose"
            "--test=${TEST_FILE}"
            "--junit-verbose"
            "--junit-xml=${TOOL_DIR}/junit.xml"
            "--timeout=30"
            "-j${N_TESTS_IN_PARALLEL}"
            "--tool=$RUNNER"
            "--"
        )
        # split EXTRA into words safely
        read -r -a EXTRA_ARR <<< "$EXTRA"

        # TODO: -j8 works only on cwl v1.0. The run_test of the others has a bug
        #       in argparse (eval expects =?).
        # v1.1 and v1.2 scripts have issues with EXTRA?
        # if [ "$VERSION" != "v1.0" ]; then
        #     sed -i 's|eval $(echo "$arg" | cut -d= -f1)="$(echo "$arg" | cut -d= -f2-)"|key=$(echo "$arg" | cut -d= -f1); val=$(echo "$arg" | cut -d= -f2-); printf -v "$key" "%s" "$val"|' "$TEST_SCRIPT"
        # fi

        {
            echo "=== RUN START ==="
            date
            echo "TOOL=$TOOL"
            echo "VERSION=$VERSION"
            echo "MODE=$MODE"
            echo "RUNNER=${TOOL_BIN[$TOOL]}"
            echo "EXTRA=${EXTRA}"
            echo "================="
            echo ""

            "$RUNNER" --version || true
            echo ""
            set -exv
            "$TEST_SCRIPT" "${ARGS[@]}" "${EXTRA_ARR[@]}"
            set +exv
        }

    ) >"$LOG_FILE" 2>&1

    EXIT_CODE=$?

    if [ "$EXIT_CODE" -ne 0 ]; then
        log "[FAIL] $TOOL $VERSION ($MODE) exit code: $EXIT_CODE"
    else
        log "[OK]   $TOOL $VERSION ($MODE)"
    fi
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    log "[TIME] $TOOL $VERSION ($MODE) took ${DURATION}s"

    echo "$TOOL $VERSION ($MODE) exit code: $EXIT_CODE" >>"$SUMMARY_FILE"
}

##############################
# Main loop
##############################

# Clone CWL specs once
log "Cloning CWL specification Git repos..."
for VERSION in "${CWL_VERSIONS[@]}"; do
    clone_cwl_repo "$VERSION"
done
log "All CWL specifications cloned locally."

# Run tests per tool
log "Running the tests..."

MODE="${MODE:-local}"

for TOOL in "${TOOLS[@]}"; do

    log "Setting up environment for $TOOL"
    setup_python_env "$TOOL"
    log "Done!"

    for VERSION in "${CWL_VERSIONS[@]}"; do
      log "[RUN] tool=$TOOL version=$VERSION mode=$MODE"
      run_tests "$TOOL" "$VERSION" "$MODE"
      log "[RUN] Finished $TOOL $VERSION ($MODE)"
      log "----------------------------------------"
    done

done

log "All runs completed."
