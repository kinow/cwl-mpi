# Example: MPICH's sr.c (test)

`sr.c` from MPICH source code.

https://github.com/pmodels/mpich/blob/a0f6d778bb864774ef9cdd29b1bd6004adc6cf64/test/basic/sr.c

## Tools

### Tool to compile sr.c

```bash
$ cwltool compile-sr.cwl compile-sr-job.yml
```

This will create the binary `./a.out`.

### Tool to run sr with mpirun

It uses `mpirun` as base command.

```bash
$ cwltool run-sr-mpirun.cwl run-sr-mpirun-job.yml
```

This will create the files `sr.out` and `sr.err`.

## Workflow

```bash
$ cwltool sr-workflow.cwl sr-workflow-job.yml
```

This will run the workflow using `compile-sr.cwl` to compile `sr.c`, and
`run-sr.cwl` to run the binary generated. The input and output are written
to the disk.

You can watch the output log and change the `sr.c` parameters to use
different values for processors, message size, and iterations.

```bash
$ cwltool sr-workflow.cwl sr-workflow-job.yml --np=6 --msg_size=10 --niter=8 --source=./sr.c
```
