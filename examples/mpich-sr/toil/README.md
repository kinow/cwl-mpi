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

Running the workflow in a container with Toil is quite simple. You must use
the `DockerRequirement` with the right image and other settings for your
container, and launch it with `toil-cwl-runner`:

```bash
toil-cwl-runner \
    --singularity \
    --logLevel=DEBUG \
    --retryCount 0 \
    sr-workflow-docker.cwl sr-workflow-mpirun-job.yml 
```

In the debug output, you should be able to confirm that the command executes successfully
and that it is using Docker. For example:

```bash
...
...
	[2026-02-26T19:37:57+0100] [MainThread] [I] [cwltool] [job sr-workflow-docker.cwl.run.run-sr-mpirun.cwl] /tmp/toilwf-5cdce9ed09a9515ba26de4bb5ac56d89/2904/job/tmp1br7ihn0/tmp-out_zrh1uu3$ docker \
	    run \
	    -i \
	    --mount=type=bind,source=/tmp/toilwf-5cdce9ed09a9515ba26de4bb5ac56d89/2904/job/tmp1br7ihn0/tmp-out_zrh1uu3,target=/TBNLca \
	    --mount=type=bind,source=/tmp/toilwf-5cdce9ed09a9515ba26de4bb5ac56d89/2904/job/tmp_h8t57882i9s1pdy,target=/tmp \
	    --mount=type=bind,source=/tmp/tmp5ry5avkd/files/for-job/kind-CWLJob/instance-nokqatxq/file-b57872aeaadd4e41a6e8de8dfd8870d3/a.out,target=/var/lib/cwl/stg9297013a-74a7-4c22-a5f3-d35194c43512/a.out,readonly \
	    --workdir=/TBNLca \
	    --read-only=true \
	    --net=none \
	    --log-driver=none \
	    --user=1000:1000 \
	    --rm \
	    --cidfile=/tmp/toilwf-5cdce9ed09a9515ba26de4bb5ac56d89/2904/job/tmp_h8t5788be362pm4/20260226193757-899158.cid \
	    --env=TMPDIR=/tmp \
	    --env=HOME=/TBNLca \
	    mfisherman/mpich:4.3.2 \
	    /bin/sh \
	    -c \
	    mpirun -np 2 /var/lib/cwl/stg9297013a-74a7-4c22-a5f3-d35194c43512/a.out 0 1 > /tmp/toilwf-5cdce9ed09a9515ba26de4bb5ac56d89/2904/job/tmp1br7ihn0/tmp-out_zrh1uu3/sr.out 2> /tmp/toilwf-5cdce9ed09a9515ba26de4bb5ac56d89/2904/job/tmp1br7ihn0/tmp-out_zrh1uu3/sr.err
...
...
[2026-02-26T19:35:16+0100] [MainThread] [I] [toil.cwl.cwltoil] Computing output file checksums...
{
    "stderr": {
        "location": "file:///home/kinow/Development/python/workspace/cwl-mpi/examples/mpich-sr/toil/sr.err",
        "basename": "sr.err",
        "nameroot": "sr",
        "nameext": ".err",
        "class": "File",
        "checksum": "sha1$da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "size": 0,
        "path": "/home/kinow/Development/python/workspace/cwl-mpi/examples/mpich-sr/toil/sr.err"
    },
    "stdout": {
        "location": "file:///home/kinow/Development/python/workspace/cwl-mpi/examples/mpich-sr/toil/sr.out",
        "basename": "sr.out",
        "nameroot": "sr",
        "nameext": ".out",
        "class": "File",
        "checksum": "sha1$c9c80dae90e2a704fe4e54e671a4d7dbf768543e",
        "size": 136,
        "path": "/home/kinow/Development/python/workspace/cwl-mpi/examples/mpich-sr/toil/sr.out"
    }
}
[2026-02-26T19:35:16+0100] [MainThread] [I] [toil.cwl.cwltoil] CWL run complete!
[2026-02-26T19:35:16+0100] [MainThread] [I] [toil.lib.history] Workflow 9f3d6d8e-feb0-45a5-a62a-bf62a9ddb226 stopped. Success: True
[2026-02-26T19:35:16+0100] [MainThread] [I] [toil.common] Successfully deleted the job store: FileJobStore(/tmp/tmpn1i95zbo)
```

To test with Singularity, all you have to do is just pass the `--singularity`
option to `toil-cwl-runner`.

```bash
...
...
[2026-02-26T19:39:17+0100] [MainThread] [I] [cwltool] [job sr-workflow-docker.cwl.run.run-sr-mpirun.cwl] /tmp/toilwf-da706989e3e25c2b8c1fdbfc773e3008/2f9b/job/tmpr292j62g/tmp-outqzg4uh29$ singularity \
    --quiet \
    run \
    --contain \
    --ipc \
    --cleanenv \
    --no-eval \
    --userns \
    --home \
    /tmp/toilwf-da706989e3e25c2b8c1fdbfc773e3008/2f9b/job/tmpr292j62g/tmp-outqzg4uh29:/rgHCFe \
    --mount=type=bind,source=/tmp/toilwf-da706989e3e25c2b8c1fdbfc773e3008/2f9b/job/tmpqpoggcmtypfhg5nl,target=/tmp \
    --mount=type=bind,source=/tmp/tmp20il8g28/files/for-job/kind-CWLJob/instance-2f6w8y0j/file-988f01ef7a054e32a3148c9d9e9710fa/a.out,target=/var/lib/cwl/stg72542286-e4e1-4b17-a475-339f3b947bf9/a.out,readonly \
    --pwd \
    /rgHCFe \
    --net \
    --network \
    none \
    /tmp/toilwf-da706989e3e25c2b8c1fdbfc773e3008/2f9b/job/mfisherman_mpich:4.3.2.sif \
    /bin/sh \
    -c \
    mpirun -np 2 /var/lib/cwl/stg72542286-e4e1-4b17-a475-339f3b947bf9/a.out 0 1 > /tmp/toilwf-da706989e3e25c2b8c1fdbfc773e3008/2f9b/job/tmpr292j62g/tmp-outqzg4uh29/sr.out 2> /tmp/toilwf-da706989e3e25c2b8c1fdbfc773e3008/2f9b/job/tmpr292j62g/tmp-outqzg4uh29/sr.err
...
...
```

Now, both cases run fine, but they are not using MPI and Singularity the recommended way for
HPCs. Instead of running `mpirun` inside of `singularity` or `docker`, it must do the reverse:
`mpirun -np 2 singularity run|exec ...`

I could not find a way to get Toil to run `mpirun` inside of `singularity` or `docker`. My last
test was with this command-line, after seeing some tests in Toil
[that appear to use CWLTool](https://github.com/search?q=repo%3ADataBiosphere%2Ftoil%20mpi&type=code):

```bash
toil-cwl-runner \
  --singularity \
  --enable-ext \
  --enable-dev \
  --logLevel=DEBUG \
  --retryCount 0 \
  sr-workflow-docker.cwl sr-workflow-mpirun-job.yml
```

Alas, that still performs `mpirun` inside of `singularity` or `docker`.

It is possible to craft a container that calls `mpirun -np N singularity`, but that becomes
complicated to maintain as we would end up having to guess if it is Apptainer, Singularity,
pass the right arguments to bind and add environment variables, etc. Things that the workflow
manager tool would be better at handling – like what CWLTool tries to do.
