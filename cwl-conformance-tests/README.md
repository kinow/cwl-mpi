# CWL Conformance Tests

This directory contains automation code to assist running CWL Conformance Tests on
different HPC systems.

## Python

For Python, the preferred option is to use one of the HPC modules. The fallback option
is to use micromamba.

We could have inverted the logic to have a more homogeneous test across HPC systems.
However, many (or most?) of the users of these HPC systems will use the Python modules
first, and if that fails, they may resort to something like micromamba. We follow a
similar path and tell users which Python module we used in their HPC system, thus giving
users more reassurance that CWL should work on their environments. Normally, if it works
in the Python module on the HPC, it should work on micromamba/conda/etc, while the
reverse is not true.

## CWL specification Git folders

Each CWL specification has a Git repository with its files (Schema Salad files, scripts,
documentation, etc.). The automation code will clone these repositories and run the
tests.

## Output

The output of these tests is stored in the output directory for each CWL tool. Each
output directory contains subfolders with the output of each run. e.g.,

```
cwl-conformance-tests/
├── cwl_conformance_tests.sh
└── hpc/
    ├── mn5.sh
    ├── lumi.sh
    ├── local.sh
    runs/
    ├── specs/
    │   ├── v1.0/
    │   ├── v1.1/
    │   └── v1.2/
    ├── cwltool/
    ├── toil/
    └── venv-*
```

## Usage

```bash
HPC=mn5 HPC_SCRATCH_DIR=/gpfs/scratch/$bscgroup/$bscuser ./cwl_conformance_tests.sh
```

## LaTeX tables

The `report_feature_coverage.py` script generates a table with the feature coverage
for each CWL version. It downloads the CWL specification Git repositories and runs
the tests. The specification YAML files are saved in the `specs` directory.

```bash
$ python3 report_latex.py >results.tex && pdflatex results.tex && xdg-open results.pdf
$ python3 report_feature_coverage.py >coverage.tex && pdflatex coverage.tex && xdg-open coverage.pdf
```