# FALL3D Workflow

The [`cloud`](./cloud/) directory contains information and scripts used to
submit the workflow to the cloud environment (Hetzner).

[`output`](./output/) stores the simulation output.

[`BUILD.md`](./BUILD.md) describes how the FALL3D model was compiled on each
environment.

## Submitting in LUMI

### `baseCommand: mpirun`, no containers

```bash
SIM=workflow-base
ENV=lumi
CONTAINER=none
JOBNAME="${SIM}_${ENV}_${CONTAINER}"

LOGDIR="logs/cwltool/$ENV/$CONTAINER"
mkdir -p "$LOGDIR"

CMD="cwltool \
  --no-container \
  --debug \
  --strict-memory-limit \
  --strict-cpu-limit \
  fall3d-what-if-volcanos.0.2.1.cwl#demo-etna \
  arguments_etna_lumi.yml"

echo "COMMAND: $CMD" > "$LOGDIR/$SIM.cmd"

sbatch \
  --partition=small \
  --account=[REDACTED] \
  --time=00:30:00 \
  --job-name="$JOBNAME" \
  --nodes=2 \
  --ntasks-per-node=32 \
  --cpus-per-task=1 \
  --export=ALL \
  --wrap="
START=\$(date +%s)
$CMD > '$LOGDIR/$SIM.log' 2>&1
EXIT=\$?
END=\$(date +%s)
echo \$((END-START)) > '$LOGDIR/$SIM.time'
echo \$EXIT > '$LOGDIR/$SIM.exit'
exit \$EXIT
"
```

### `baseCommand: mpirun`, with Singularity

```bash
SIM=workflow-base
ENV=lumi
CONTAINER=singularity
JOBNAME="${SIM}_${ENV}_${CONTAINER}"

LOGDIR="logs/cwltool/$ENV/$CONTAINER"
mkdir -p "$LOGDIR"

CMD="cwltool \
  --singularity \
  --debug \
  --strict-memory-limit \
  --strict-cpu-limit \
  fall3d-what-if-volcanos.0.2.1.cwl#demo-etna \
  arguments_etna_container.yml"

echo "COMMAND: $CMD" > "$LOGDIR/$SIM.cmd"

sbatch \
  --partition=small \
  --account=[REDACTED] \
  --time=00:30:00 \
  --job-name="$JOBNAME" \
  --nodes=2 \
  --ntasks-per-node=32 \
  --cpus-per-task=1 \
  --export=ALL \
  --wrap="
START=\$(date +%s)
$CMD > '$LOGDIR/$SIM.log' 2>&1
EXIT=\$?
END=\$(date +%s)
echo \$((END-START)) > '$LOGDIR/$SIM.time'
echo \$EXIT > '$LOGDIR/$SIM.exit'
exit \$EXIT
```

### `MPIRequirement`, no containers

```bash
SIM=workflow-req
ENV=lumi
CONTAINER=none
JOBNAME="${SIM}_${ENV}_${CONTAINER}"

LOGDIR="logs/cwltool/$ENV/$CONTAINER"
mkdir -p "$LOGDIR"

CMD="cwltool \
  --no-container \
  --enable-ext \
  --mpi-config-file mpi-config-file-lumi.yml \
  --debug \
  --strict-memory-limit \
  --strict-cpu-limit \
  fall3d-what-if-volcanos.0.2.1_mpirequirement.cwl#demo-etna \
  arguments_etna_lumi.yml"

echo "COMMAND: $CMD" > "$LOGDIR/$SIM.cmd"

sbatch \
  --partition=small \
  --account=[REDACTED] \
  --time=00:30:00 \
  --job-name="$JOBNAME" \
  --nodes=2 \
  --ntasks-per-node=32 \
  --cpus-per-task=1 \
  --export=ALL \
  --wrap="
START=\$(date +%s)
$CMD > '$LOGDIR/$SIM.log' 2>&1
EXIT=\$?
END=\$(date +%s)
echo \$((END-START)) > '$LOGDIR/$SIM.time'
echo \$EXIT > '$LOGDIR/$SIM.exit'
exit \$EXIT
"
```

### `MPIRequirement`, with Singularity

```bash
SIM=workflow-req
ENV=lumi
CONTAINER=singularity
JOBNAME="${SIM}_${ENV}_${CONTAINER}"

LOGDIR="logs/cwltool/$ENV/$CONTAINER"
mkdir -p "$LOGDIR"

CMD="cwltool \
  --singularity \
  --enable-ext \
  --mpi-config-file mpi-config-file-lumi.yml \
  --debug \
  --strict-memory-limit \
  --strict-cpu-limit \
  fall3d-what-if-volcanos.0.2.1_mpirequirement.cwl#demo-etna \
  arguments_etna_container.yml"

echo "COMMAND: $CMD" > "$LOGDIR/$SIM.cmd"

sbatch \
  --partition=small \
  --account=[REDACTED] \
  --time=00:30:00 \
  --job-name="$JOBNAME" \
  --nodes=2 \
  --ntasks-per-node=32 \
  --cpus-per-task=1 \
  --export=ALL \
  --wrap="
START=\$(date +%s)
$CMD > '$LOGDIR/$SIM.log' 2>&1
EXIT=\$?
END=\$(date +%s)
echo \$((END-START)) > '$LOGDIR/$SIM.time'
echo \$EXIT > '$LOGDIR/$SIM.exit'
exit \$EXIT
```