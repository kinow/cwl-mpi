# Toil

<https://toil.readthedocs.io/en/latest/>

Toil version: 9.2.0

## Prerequisites

```bash
pip install toil[cwl]
```

## Local Tests

Once Toil is installed, running the same workflow as in the CWLTool
that uses `mpirun` example should work fine.

```bash
$ toil-cwl-runner sr-workflow.cwl sr-workflow-job.yml
[2026-02-22T10:51:33+0100] [MainThread] [I] [toil.lib.history] Recording workflow creation of 6c790769-66ba-49dd-83ab-60eef747a633 in file:/tmp/tmp301bmo25
[2026-02-22T10:51:33+0100] [MainThread] [I] [toil.cwl.cwltoil] Importing tool-associated files...
[2026-02-22T10:51:33+0100] [MainThread] [I] [toil.cwl.cwltoil] Importing input files...
[2026-02-22T10:51:33+0100] [MainThread] [I] [toil.jobStores.abstractJobStore] Importing input file:///home/kinow/Development/python/workspace/cwl-mpi/examples/mpich-sr/toil/sr.c...
[2026-02-22T10:51:33+0100] [MainThread] [I] [toil.cwl.cwltoil] Starting workflow
[2026-02-22T10:51:33+0100] [MainThread] [I] [toil.lib.history] Workflow 6c790769-66ba-49dd-83ab-60eef747a633 is a run of sr-workflow.cwl
[2026-02-22T10:51:34+0100] [MainThread] [I] [toil] Running Toil version 9.2.0-03ecbc5c4965941b0d87c26cc2d09415dbeb670c on host ranma.
[2026-02-22T10:51:34+0100] [MainThread] [I] [toil.realtimeLogger] Starting real-time logging.
...
...
...
[2026-02-22T10:51:43+0100] [MainThread] [I] [toil.cwl.cwltoil] CWL run complete!
[2026-02-22T10:51:43+0100] [MainThread] [I] [toil.lib.history] Workflow 6c790769-66ba-49dd-83ab-60eef747a633 stopped. Success: True
```

※Toil is the only CWL runner that alerts about using more cores than requested.
While the others appear to ignore as the `ResourceRequirement` is not available,
Toil assumes if the user does not specify the cores, then it must be `1`.

```
[2026-02-22T10:58:28+0100] [Thread-4 (statsAndLoggingAggregator)] [W] [toil.statsAndLogging] Got message from job at time 02-22-2026 10:58:2
8: Job 'ResolveIndirect' sr-workflow.cwl._resolve kind-ResolveIndirect/instance-_oartj2f v3 used 1.03x more CPU than the requested 1 cores. 
Consider increasing the job's required CPU cores or limiting the number of processes/threads launched.
```

I tried setting the `ResourceRequirement` to use the number of nodes requested
for `mpirun`:

```yaml
requirements:
  DockerRequirement:
    dockerPull: mfisherman/mpich:4.3.2
  ResourceRequirement:
    coresMin: $(inputs.np)

baseCommand: mpirun

inputs:
  np:
    type: int
    default: 2
    inputBinding:
      prefix: -np
      position: 1
```

But that did not fix the warning. Using `--maxCores` also had no effect.
Not even when combined with `--defaultCores 4.0`.

## HPC Tests

<https://toil.readthedocs.io/en/latest/running/hpcEnvironments.html>

Toil supports provisioning of Toil servers in the cloud and accessing them via SSH.
It also supports running Toil on HPC clusters with Slurm.

For HPC environments, Slurm in Toil is considered "community supported" (sic). Toil
must be executed in one of the head nodes of the cluster.

### BSC MareNostrum5 Tests

```bash
ssh mn5-login  # login node 4, with Internet access
cd ~/cwl/toil
git clone -o upstream https://github.com/kinow/cwl-mpi.git
cd cwl-mpi/examples/mpich-sh/toil/
module load hdf5 python/3.12.1
python3 -m venv venv
source venv/bin/activate
pip install toil[cwl]
```

Running my first Toil Slurm job on MN5 with this command,

```bash
toil-cwl-runner \
    --batchSystem=slurm \
    --slurmTime "00:05:00" \
    --slurmPartition "debug" \
    --slurmArgs="-A <PROJECT> \
    --nodes=1 \
    --ntasks=2 \
    --cpus-per-task=1" \
    sr-workflow.cwl sr-workflow-srun-job.yml
    
```
gives me this error:

```bash
[2026-02-22T14:57:01+0100] [MainThread] [I] [toil.lib.history] Recording workflow creation of d506bdf7-5bdb-4621-9fc3-952c9ef53dae in file:/scratch/tmp/tmpoy8lo5we
[2026-02-22T14:57:01+0100] [MainThread] [I] [toil.cwl.cwltoil] Importing tool-associated files...
[2026-02-22T14:57:01+0100] [MainThread] [I] [toil.cwl.cwltoil] Importing input files...
[2026-02-22T14:57:01+0100] [MainThread] [I] [toil.jobStores.abstractJobStore] Importing input file:///gpfs/home/<PROJECT>/<USER>cwl/toil/cwl-mpi/examples/mpich-sr/toil/sr.c...
[2026-02-22T14:57:01+0100] [MainThread] [I] [toil.cwl.cwltoil] Starting workflow
[2026-02-22T14:57:01+0100] [MainThread] [I] [toil.lib.history] Workflow d506bdf7-5bdb-4621-9fc3-952c9ef53dae is a run of sr-workflow.cwl
slurm_load_node: Access/permission denied
[2026-02-22T14:57:01+0100] [MainThread] [I] [toil.lib.history] Workflow d506bdf7-5bdb-4621-9fc3-952c9ef53dae stopped. Success: False
Traceback (most recent call last):
...
...
toil.lib.misc.CalledProcessErrorStderr: Command '['sinfo', '-a', '-o', '%P %G %l %p %c %m']' exit status 1: slurm_load_node: Access/permission denied
```

Running the same command on BSC MareNostrum5 results in the same error. This is
due to a security policy on the cluster, which prevents Toil from running  with
Slurm on BSC MN5.

<https://github.com/DataBiosphere/toil/issues/5461>

## Container Tests

TODO
