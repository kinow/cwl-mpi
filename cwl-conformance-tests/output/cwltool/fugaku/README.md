This directory contains tests performed on Fugaku HPC.

Fugaku was not included in the first tag of this repository, which includes
the tests performed for the CWL + MPI master's thesis.

`local` is the same as in other HPCs, a login node in Fugaku HPC.

`pjm` refers to the execution where the CWL conformance tests were executed
within an interactive PJM allocation. **NOTE**: Previously, there were errors
launching the tests in this configuration because the `local` tests produced
`x86_64` containers and `pip` dependencies that were cached and then re-used
during the execution on `aarch64` PJM. The micromamba environment was created
completely within the interactive PJM session.

The conformance tests were executed directly on a Fugaku login node, using
`cwltest`. All tests passed successfully 🎉🥳!
