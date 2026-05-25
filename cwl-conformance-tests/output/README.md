This directory contains CWL Conformance tests output files,
executed on different HPC machines.

BSC MareNostrum → mn5, CSC LUMI → lumi, CESGA Finis Terrae III
→ ft3.

Inside each CWL runner folder (e.g., `cwltool`), you will find a
directory for each HPC (e.g., `mn5`) that was used to execute the
tests. And inside that directory, you will find one more level
with the execution mode (e.g., `local`).

The `local` mode is a local run, executed on the login node of the
HPC. The `slurm` mode is a run in a Slurm allocation using a compute
node. Finally, `batch` mode is for runs executed in a local environment
(could be laptop or login node) submitting jobs via SSH or via a
launcher to a batch scheduler like `sbatch`.
