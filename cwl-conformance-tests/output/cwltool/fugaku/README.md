This directory contains tests performed on Fugaku HPC.

Fugaku was not included in the first tag of this repository, which includes
the tests performed for the CWL + MPI master's thesis.

`local` is the same as in other HPCs, a login node in Fugaku HPC.

`pjm` refers to the execution where, using the same environment used for
the login node, tests are submitted via a batch scheduler. Different from
the other HPCs (CESGA FT3, CSC LUMI, BSC MN5), Fugaku uses PJM.

`pjm_install` is the execution also using PJM, but instead of using the same
environment from the login node, the Python virtual environment is created
within the compute node.

`pjm` and `pjm_install` are used because Fugaku (at the time of writing, 2026)
has login nodes with `x86_64` architecture, while PJM compute nodes have
`aarch64` architecture CPUs.

In the `pjm` folder, the execution fails because `cwltool` has a dependency
on `psutil`, which ships with  pre-compiled Linux static object. The `psutil`
package has an `.so` created for `x86_64`, which fails to load on PJM.

```bash
ImportError: /vol0006/mdt1/home/[REDACTED]/venv/lib64/python3.11/site-packages/
psutil/_psutil_linux.abi3.so: cannot open shared object file: No such file
or directory
```

`pjm_install` tries to solve this by doing everything in the compute
node. There are different errors, but one that's recurrent in the logs is
the incorrect architecture of the container image. Again, `x86_64` images
are being used in the PJM compute nodes, causing Singularity to fail running
the CWL conformance tests.

```bash
<system-err>FATAL:   While checking image: could not open image 
/vol0006/mdt1/home/[REDACTED]/common-workflow-language/v1.0/python:2-slim.sif: 
the image's architecture (amd64) could not run on the host's (arm64)
...
```

The Fugaku tests were executed directly on a login node, using `cwltest`.
