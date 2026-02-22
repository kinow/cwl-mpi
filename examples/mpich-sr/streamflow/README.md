# Example: MPICH's sr.c (test)

## StreamFlow

Prerequisites:

```bash
pip install streamflow
```

StreamFlow includes a CWL runner, but it does not support the `MPIRequirement`
hint. Running the version of the workflow `mpirun` used with `cwltool` works
with StreamFlow. It does not require any change to the tool or settings. We
simply need to create a [StreamFlow configuration file][streamflow_file], which
uses the YAML syntax.

File `run-sr-mpirun-streamflow.cwl`:

```yaml
# Ref: https://streamflow.di.unito.it/documentation/latest/cwl/cwl-runner.html
version: v1.0
workflows:
  workflow_name:
    type: cwl
    config:
      file: run-sr-mpirun.cwl
      settings: run-sr-mpirun-job.yml
```

We run it with StreamFlow:

```bash
streamflow run run-sr-mpirun-streamflow.cwl
```

This creates the `sr.out` and `sr.err` files, as with `cwltool`.

As StreamFlow does not support `MPIRequirement`, running the other workflow
that worked with `cwltool` results in an error as the `sr.c` program expects
a minimum number of processes.

We also have to specify a job settings file to use in the StreamFlow file.

File `run-sr-mpireq-nodocker-streamflow-job.cwl`:

```yaml
np: 4
executable:
  class: File
  path: ./sr.out
msg_size: 0
niter: 1
```

And a StreamFlow file to call the CWL tool with `MPIRequirement`,

File `run-sr-mpireq-nodocker-streamflow.cwl`:

```yaml
# Ref: https://streamflow.di.unito.it/documentation/latest/cwl/cwl-runner.html
version: v1.0
workflows:
  workflow_name:
    type: cwl
    config:
      file: run-sr-mpireq-nodocker.cwl
      settings: run-sr-mpireq-nodocker-streamflow-job.cwl
```

Then, running it with StreamFlow, we can see that there is an error,
even though StreamFlow does not print the program output directly.

```bash
$ streamflow run --debug run-sr-mpireq-nodocker-streamflow.cwl
2026-02-21 17:36:59.735 INFO     Processing workflow dd5ae3dd-103e-4f45-83c1-f86249d749e4
2026-02-21 17:36:59.735 INFO     Building workflow execution plan
2026-02-21 17:37:00.159 DEBUG    Translating CommandLineTool /
2026-02-21 17:37:00.410 INFO     COMPLETED building of workflow execution plan
2026-02-21 17:37:00.410 INFO     EXECUTING workflow dd5ae3dd-103e-4f45-83c1-f86249d749e4
2026-02-21 17:37:00.436 WARNING  Skipping Storage on partition portal on /run/user/1000/doc for deployment __LOCAL__: [Errno 1] Operation not permitted: '/run/user/1000/doc'
...
...
2026-02-21 17:37:00.494 DEBUG    Job /0 changed status to RUNNING
2026-02-21 17:37:00.494 DEBUG    Job /0 inputs: {
    "executable": {
        "basename": "sr.out",
        "checksum": "sha1$64cb27a9adc2945d46cd6f025ec17e64bda3d5f1",
        "class": "File",
        "dirname": "/tmp/streamflow/89c65b5e-29f9-477e-aacc-c2b6d2921f94/50a9386f-3dec-48ad-82a5-48ebdce2ae47",
        "location": "file:///tmp/streamflow/89c65b5e-29f9-477e-aacc-c2b6d2921f94/50a9386f-3dec-48ad-82a5-48ebdce2ae47/sr.out",
        "nameext": ".out",
        "nameroot": "sr",
        "path": "/tmp/streamflow/89c65b5e-29f9-477e-aacc-c2b6d2921f94/50a9386f-3dec-48ad-82a5-48ebdce2ae47/sr.out",
        "size": 218
    },
    "msg_size": 0,
    "niter": 1,
    "np": 4
}
2026-02-21 17:37:00.494 INFO     EXECUTING step / (job /0) locally into directory /tmp/streamflow/f1ed7037-a731-44d0-8f9a-253366ef54ed:
/tmp/streamflow/89c65b5e-29f9-477e-aacc-c2b6d2921f94/50a9386f-3dec-48ad-82a5-48ebdce2ae47/sr.out \
	0 \
	1
2026-02-21 17:37:00.495 DEBUG    Step / received termination token with Status COMPLETED
2026-02-21 17:37:00.495 DEBUG    EXECUTING command cd /tmp/streamflow/f1ed7037-a731-44d0-8f9a-253366ef54ed && export HOME="/tmp/streamflow/f1ed7037-a731-44d0-8f9a-253366ef54ed" && export TMPDIR="/tmp/streamflow/26e9173b-6e71-4ff7-b272-082410329860" && /tmp/streamflow/89c65b5e-29f9-477e-aacc-c2b6d2921f94/50a9386f-3dec-48ad-82a5-48ebdce2ae47/sr.out 0 1 > sr.out 2>sr.err on __LOCAL__/__LOCAL__ for job /0
2026-02-21 17:37:00.496 ERROR    FAILED Job /0 with error:
	
Traceback (most recent call last):
  File "/home/kinow/Development/python/workspace/streamflow/streamflow/core/recovery.py", line 44, in wrapper
    await func(*args, **kwargs)
  File "/home/kinow/Development/python/workspace/streamflow/streamflow/workflow/step.py", line 747, in _execute_command
    raise WorkflowExecutionException(
        f"FAILED Job {job.name} with error:\n\t{command_output.value}"
    )
streamflow.core.exception.WorkflowExecutionException: FAILED Job /0 with error:
	
2026-02-21 17:37:00.497 WARNING  Job /0 failure can not be recovered. Failure manager is not enabled.
2026-02-21 17:37:00.497 ERROR    FAILED Job /0 with error:
	
2026-02-21 17:37:00.497 DEBUG    Job /0 changed status to FAILED
2026-02-21 17:37:00.497 DEBUG    FAILED Job /0 terminated
2026-02-21 17:37:00.498 DEBUG    Step /stdout_file-collector-transformer received termination token with Status FAILED
2026-02-21 17:37:00.498 DEBUG    Step /stderr_file-collector-transformer received termination token with Status FAILED
2026-02-21 17:37:00.498 DEBUG    Step /stdout_file-collector received termination token with Status FAILED
2026-02-21 17:37:00.498 DEBUG    Step /stdout_file-collector/__schedule__ received termination token with Status FAILED
2026-02-21 17:37:00.498 DEBUG    Step /stderr_file-collector received termination token with Status FAILED
2026-02-21 17:37:00.498 DEBUG    Step /stderr_file-collector/__schedule__ received termination token with Status FAILED
2026-02-21 17:37:00.498 INFO     FAILED Step /
2026-02-21 17:37:00.498 DEBUG    FAILED Step /stdout_file-collector-transformer
2026-02-21 17:37:00.498 DEBUG    FAILED Step /stderr_file-collector-transformer
2026-02-21 17:37:00.498 DEBUG    FAILED Step /stdout_file-collector/__schedule__
2026-02-21 17:37:00.498 DEBUG    FAILED Step /stderr_file-collector/__schedule__
2026-02-21 17:37:00.498 DEBUG    FAILED Step /stdout_file-collector
2026-02-21 17:37:00.498 DEBUG    FAILED Step /stderr_file-collector
2026-02-21 17:37:00.510 ERROR    FAILED Workflow execution
Traceback (most recent call last):
  File "/home/kinow/Development/python/workspace/streamflow/streamflow/main.py", line 281, in main
    asyncio.run(_async_run(parsed_args))
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/usr/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/usr/lib/python3.13/asyncio/base_events.py", line 725, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/home/kinow/Development/python/workspace/streamflow/streamflow/main.py", line 187, in _async_run
    await asyncio.gather(*workflow_tasks)
  File "/home/kinow/Development/python/workspace/streamflow/streamflow/cwl/main.py", line 93, in main
    output_tokens = await executor.run()
                    ^^^^^^^^^^^^^^^^^^^^
  File "/home/kinow/Development/python/workspace/streamflow/streamflow/workflow/executor.py", line 151, in run
    raise WorkflowExecutionException("FAILED Workflow execution")
streamflow.core.exception.WorkflowExecutionException: FAILED Workflow execution
```

Underneath, `streamflow` is failing as it ran `sr.out` directly without `mpirun` (as the
`MPIRequirement` is ignored) and had an error similar to this:

```bash
$ ./sr 0 1
sr: size 1 rank 0
ERROR: needs to be run with at least 2 procs
msg_sz=0, niter=1
[ranma:00000] *** An error occurred in MPI_Send
[ranma:00000] *** reported by process [1576271872,0]
[ranma:00000] *** on communicator MPI_COMM_WORLD
[ranma:00000] *** MPI_ERR_RANK: invalid rank
[ranma:00000] *** MPI_ERRORS_ARE_FATAL (processes in this communicator will now abort,
[ranma:00000] ***    and MPI will try to terminate your MPI job as well)
```

[streamflow_file]: https://streamflow.di.unito.it/documentation/latest/operations.html#put-it-all-together
