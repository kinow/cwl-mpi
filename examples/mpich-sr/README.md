`sr.c` from MPICH source code.

https://github.com/pmodels/mpich/blob/a0f6d778bb864774ef9cdd29b1bd6004adc6cf64/test/basic/sr.c

## Tool to compile sr.c

```bash
$ cwltool compile-sr.cwl compile-sr-job.yml
```

This will create the binary `./a.out`.

## Tool to run sr with mpirun

It uses `mpirun` as base command.

```bash
$ cwltool run-sr-mpirun.cwl run-sr-mpirun-job.yml
```

This will create the files `sr.out` and `sr.err`.
