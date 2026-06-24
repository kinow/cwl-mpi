# CWL & MPI — Containers

These are some containers used as tests on HPC systems and local laptop.
They may not be directly linked to CWL and are more likely used to
evaluate the underlying operating system, MPI & containers installations.

References:

- https://docs.lumi-supercomputer.eu/software/containers/singularity/

## OSU

(The thesis objectives are mainly around integration and correctness of
CWL and MPI, not performance — these are only illustrative examples.)

The files `mpich-3.4.3-osu-7.4.def` and `mpich-4..3.1-osu-7.5.1.Dockerfile`
were tested to verify using MPI with Singularity and Docker respectively.

The `mpich-3.4.3-osu-7.4.def` was executed on CSC LUMI.

The launch command.

```bash
sbatch \
  --partition=debug \
  --account=[REDACTED] \
  --time=00:10:00 \
  --job-name=lumi_osu_singularity \
  --ntasks=2 \
  --cpus-per-task=1 \
  --wrap="srun --mpi=pmi2 singularity exec mpich-3.4.3-osu-7.4.def /usr/local/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_bw"
```

And results with Singularity (bandwidth plateaus around 24 GB/s).

```bash
# OSU MPI Bandwidth Test v7.4
# Datatype: MPI_CHAR.
# Size      Bandwidth (MB/s)
1                      10.25
2                      20.01
4                      41.32
8                      81.94
16                    163.80
32                    299.38
64                    598.71
128                  1153.15
256                  2123.85
512                  3777.49
1024                 6862.15
2048                11220.21
4096                17290.46
8192                23334.12
16384               28045.90
32768               27572.41
65536               19587.88
131072              21663.76
262144              24800.35
524288              24758.18
1048576             24160.25
2097152             24510.72
4194304             24461.10
```

And results running on native (bandwidth achieves near 50 GB/s).

```bash
# OSU MPI Bandwidth Test v7.4
# Datatype: MPI_CHAR.
# Size      Bandwidth (MB/s)
1                       8.53
2                      21.18
4                      43.00
8                      86.06
16                    168.95
32                    344.33
64                    678.51
128                  1340.01
256                  2423.85
512                  4353.42
1024                 8134.60
2048                11235.76
4096                16509.32
8192                36684.87
16384               43421.54
32768               42946.53
65536               47344.88
131072              50755.53
262144              45000.33
524288              42599.48
1048576             39332.34
2097152             42816.48
4194304             42347.43
```

This shows that while PMI-2 was used to launch the container
successfully, it is not using the Cray MPI stack.

The thesis considered tests that produced a call with `srun` executing
`singularity` as valid and correct. Performance-wise, it is ideal that the
proper MPI stack is used, but the performance tuning details are out of the
scope of this thesis.
