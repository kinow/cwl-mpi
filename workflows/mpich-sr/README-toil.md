# sr.c – Running with Toil

The [`Makefile`](./Makefile) build script has a pre-defined `CWL_RUNNER` variable
that points to the `cwltool` executable.

The tests conducted in the master's thesis used:

- Toil 9.2.0

As Toil has a command-line interface that is compatible with `cwltool`, we can easily
run all the tools and workflows with Toil using:

```bash
$ make CWL_RUNNER=toil-cwl-runner mpicc
$ make CWL_RUNNER=toil-cwl-runner SINGULARITY=1 mpirun-base
```

See the other targets of cwltool in the [`README-cwltool.md`](./README-cwltool.md)
document.

Toil will also fail when using `MPIRequirement` with Singularity. Since Toil uses
cwltool, it is likely once a new version of cwltool with the pull request
https://github.com/common-workflow-language/cwltool/pull/1004 is released,
and Toil is updated, then it will support `MPIRequirement` with Singularity.

```bash
$ # This works
$ make CWL_RUNNER=toil-cwl-runner SINGULARITY=0 mpirun-req
...
{
    "stderr_file": {
        "location": "file:///home/kinow/Development/python/workspace/cwl-mpi/workflows/mpich-sr/mpirun-mpi-requirement.err",
        "basename": "mpirun-mpi-requirement.err",
        "nameroot": "mpirun-mpi-requirement",
        "nameext": ".err",
        "class": "File",
        "checksum": "sha1$da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "size": 0,
        "path": "/home/kinow/Development/python/workspace/cwl-mpi/workflows/mpich-sr/mpirun-mpi-requirement.err"
    },
    "stdout_file": {
        "location": "file:///home/kinow/Development/python/workspace/cwl-mpi/workflows/mpich-sr/mpirun-mpi-requirement.out",
        "basename": "mpirun-mpi-requirement.out",
        "nameroot": "mpirun-mpi-requirement",
        "nameext": ".out",
        "class": "File",
        "checksum": "sha1$f240f9e6a3172eafdea7d60a750800f64ba05717",
        "size": 136,
        "path": "/home/kinow/Development/python/workspace/cwl-mpi/workflows/mpich-sr/mpirun-mpi-requirement.out"
    }
}
[2026-05-31T20:55:33+0200] [MainThread] [I] [toil.cwl.cwltoil] CWL run complete!
[2026-05-31T20:55:33+0200] [MainThread] [I] [toil.lib.history] Workflow f0a82793-5a2d-4856-92bc-a37b8e638015 stopped. Success: True
[2026-05-31T20:55:33+0200] [MainThread] [I] [toil.common] Successfully deleted the job store: FileJobStore(/tmp/tmpg94mpa83)

$ # This fails
make CWL_RUNNER=toil-cwl-runner SINGULARITY=1 mpirun-req
...
	[2026-05-31T20:57:04+0200] [MainThread] [I] [cwltool] [job mpich-mpirun-base-command] /tmp/toilwf-7d72e6d6f1b954339d909cee94601057/5dba/job/tmp2bbj10bl/tmp-outkdg15z1a$ mpirun \
	    -n \
	    2 \
	    singularity \
	    --quiet \
	    run \
	    --contain \
	    --ipc \
	    --cleanenv \
	    --no-eval \
	    --userns \
	    --home \
	    /tmp/toilwf-7d72e6d6f1b954339d909cee94601057/5dba/job/tmp2bbj10bl/tmp-outkdg15z1a:/rtDGRr \
	    --mount=type=bind,source=/tmp/toilwf-7d72e6d6f1b954339d909cee94601057/5dba/job/tmpt7iac3l4hihqaunw,target=/tmp \
	    --mount=type=bind,source=/tmp/tmp7w4r6x7_/files/no-job/file-53f749fe5e3a4f2991f1adb961d7d487/sr,target=/var/lib/cwl/stg7992e2ab-8c61-4715-8c1d-a94c46c04ee0/sr,readonly \
	    --pwd \
	    /rtDGRr \
	    --net \
	    --network \
	    none \
	    /tmp/toilwf-7d72e6d6f1b954339d909cee94601057/5dba/job/mfisherman_mpich:4.3.2.sif \
	    /var/lib/cwl/stg7992e2ab-8c61-4715-8c1d-a94c46c04ee0/sr \
	    0 \
	    1 > /tmp/toilwf-7d72e6d6f1b954339d909cee94601057/5dba/job/tmp2bbj10bl/tmp-outkdg15z1a/mpirun-mpi-requirement.out 2> /tmp/toilwf-7d72e6d6f1b954339d909cee94601057/5dba/job/tmp2bbj10bl/tmp-outkdg15z1a/mpirun-mpi-requirement.err
	[2026-05-31T20:57:04+0200] [MainThread] [W] [cwltool] [job mpich-mpirun-base-command] exited with status: 6
	[2026-05-31T20:57:04+0200] [MainThread] [W] [cwltool] [job mpich-mpirun-base-command] completed permanentFail
	[2026-05-31T20:57:04+0200] [MainThread] [W] [toil.fileStores.abstractFileStore] Failed job accessed files:
	[2026-05-31T20:57:04+0200] [MainThread] [W] [toil.fileStores.abstractFileStore] Symlinked file 'files/no-job/file-53f749fe5e3a4f2991f1adb961d7d487/sr' to path '/tmp/toilwf-7d72e6d6f1b954339d909cee94601057/5dba/job/tmpndwu97qn.tmp'
	[2026-05-31T20:57:04+0200] [MainThread] [C] [toil.worker] Worker crashed with traceback:
	Traceback (most recent call last):
	  File "/home/kinow/Development/python/workspace/toil/src/toil/worker.py", line 591, in workerScript
	    job._runner(
	    ~~~~~~~~~~~^
	        jobGraph=None,
	        ^^^^^^^^^^^^^^
	    ...<2 lines>...
	        defer=defer,
	        ^^^^^^^^^^^^
	    )
	    ^
	  File "/home/kinow/Development/python/workspace/toil/src/toil/job.py", line 3376, in _runner
	    returnValues = self._run(jobGraph=None, fileStore=fileStore)
	  File "/home/kinow/Development/python/workspace/toil/src/toil/job.py", line 3254, in _run
	    return self.run(fileStore)
	           ~~~~~~~~^^^^^^^^^^^
	  File "/home/kinow/Development/python/workspace/toil/src/toil/cwl/cwltoil.py", line 2864, in run
	    raise cwl_utils.errors.WorkflowException(status)
	cwl_utils.errors.WorkflowException: permanentFail
	
	[2026-05-31T20:57:04+0200] [MainThread] [E] [toil.worker] Exiting the worker because of a failed job on host ranma
<=========
make: *** [Makefile:59: mpirun-req] Error 1
```

You can also call the tools and workflows directly:

```bash
$ toil-cwl-runner mpich-mpicc.cwl
$ toil-cwl-runner --singularity mpich-mpirun-base-command.cwl
$ toil-cwl-runner --singularity --logLevel=DEBUG  --retryCount 0 --bypass-file-store workflow-base-command.cwl
```

※ `--bypass-file-store` is needed to avoid the error:
```bash
$ toil-cwl-runner workflow-base-command.cwl 
Pulling mfisherman/mpich:4.3.2 with docker...
[2026-05-31T21:23:55+0200] [MainThread] [I] [toil.cwl.cwltoil] Importing tool-associated files...
[2026-05-31T21:23:55+0200] [MainThread] [I] [toil.lib.history] Workflow 3554def6-0f34-4317-8ed2-dada93083cc9 stopped. Success: False
[2026-05-31T21:23:55+0200] [MainThread] [E] [root] Could not find file:///home/kinow/Development/python/workspace/cwl-mpi/workflows/mpich-sr/sr
```
That is due to how Toil handles files in workflows, even though that works in cwltool.
https://toil.readthedocs.io/en/latest/cwl/running.html#running-cwl-workflows-with-inplaceupdaterequirement

## Testing with Slurm

The example below works on CSC LUMI HPC with Toil:

```bash
$ toil-cwl-runner --singularity --logLevel=DEBUG \
    --retryCount 0 --bypass-file-store  --batchSystem=slurm \
    --allocate_mem --defaultMemory=2G \
    --slurmArgs="--partition=standard -A project_123 --export=ALL" \
    workflow-base-command.cwl
```

## Note about resource requirements

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
