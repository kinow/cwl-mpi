# CWL Conformance Tests

This directory contains automation code to assist running CWL Conformance Tests on
different HPC systems.

## Python

Micromamba was used to create and manage Conda environments on each HPC system.
The first experiments were performed with `module` system. However, in many cases
i) the Python version was not compatible (too old), or ii) Node.js or other dependencies
like GDAL were not available.

## CWL specification Git folders

Each CWL specification has a Git repository with its files (Schema Salad files, scripts,
documentation, etc.). The automation code will clone these repositories and run the
tests.

## Output

The output of these tests is stored in the output directory for each CWL runner. Each
output directory contains subfolders with the output of each run. e.g.,

```
cwl-conformance-tests/
├── cwl_conformance_tests.sh
└── hpc/
    ├── ft3.sh
    ├── lumi.sh
    ├── mn5.sh
    output/
    ├── cwltool/
    ├── streamflow/
    ├── toil/
    runs/
    ├── specs/
    │   ├── v1.0/
    │   ├── v1.1/
    │   └── v1.2/
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