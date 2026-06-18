#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree

OUTPUT_DIR = Path("output")

RUNNERS = {
    "cwltool": "cwltool",
    "toil": "Toil",
    "streamflow": "StreamFlow",
}

HPCS = ["ft3", "lumi", "mn5"]
# Enforce that all 3 modes must be presented in this exact row order for each HPC
MODES = ["local", "slurm", "batch"]

FAILED_RUNS = {
    ("streamflow", "v1.1"),
}
"""Configurations that failed to launch the tests."""


@dataclass(frozen=True)
class Result:
    passed: int
    failed: int
    skipped: int
    errors: int


AllResultType = dict[str, dict[tuple[str, str, str], Result]]


def parse_junit(xml_path: Path) -> Result:
    tree = ElementTree.parse(xml_path)
    root = tree.getroot()

    testsuite = root.find("testsuite")
    if testsuite is None:
        raise RuntimeError(f"No testsuite in {xml_path}")

    tests = int(testsuite.attrib.get("tests", 0))
    failures = int(testsuite.attrib.get("failures", 0))
    skipped = int(testsuite.attrib.get("skipped", 0))
    errors = int(testsuite.attrib.get("errors", 0))

    passed = tests - failures - skipped - errors

    return Result(passed, failures, skipped, errors)


def collect_results() -> AllResultType:
    results_found: AllResultType = {}

    for runner in RUNNERS:
        results_found[runner] = {}
        runner_dir = OUTPUT_DIR / runner

        if not runner_dir.exists():
            continue

        for hpc_dir in sorted(runner_dir.iterdir()):
            hpc = hpc_dir.name

            for version_dir in sorted(hpc_dir.iterdir()):
                version = version_dir.name

                for mode_dir in sorted(version_dir.iterdir()):
                    mode = mode_dir.name

                    junit = mode_dir / "junit.xml"

                    if junit.exists():
                        result = parse_junit(junit)
                    else:
                        result = Result(0, 0, 0, 0)

                    results_found[runner][(hpc, mode, version)] = result

    return results_found


def print_latex(results_found: AllResultType) -> None:
    print(r"\documentclass{article}")
    print(r"\usepackage{geometry}")
    print(r"\usepackage{array}")
    print(r"\usepackage{multirow}")
    print(r"\usepackage[table]{xcolor}")
    print(r"\geometry{margin=1in}")
    print(r"\begin{document}")

    CWL_VERSIONS = {
        "v1.0": "CWL v1.0.2",
        "v1.1": "CWL v1.1.0",
        "v1.2": "CWL v1.2.1",
    }

    HPC_NAMES = {
        "ft3": "FinisTerrae III",
        "lumi": "LUMI",
        "mn5": "MareNostrum 5",
    }

    MODE_LABELS = {
        "local": "login-node",
        "slurm": "slurm-node",
        "batch": "slurm-batch",
    }

    def cell(r: Result | None):
        if r is None:
            return ("—", "—", "—")
        return (str(r.passed), str(r.failed), str(r.skipped))

    def success_pct(r: Result | None) -> str:
        if r is None:
            return "—"
        total = r.passed + r.failed + r.skipped
        if total == 0:
            return "—"
        return f"{(r.passed / total) * 100:.1f}"

    def is_failed_run(runner_key: str, version_key: str) -> bool:
        return (runner_key, version_key) in FAILED_RUNS

    for runner_key, runner_name in RUNNERS.items():
        runner_data = results_found.get(runner_key, {})

        print("")
        print("")
        print(rf"% --- {runner_name} ---")
        print("")
        print("")

        print(r"\clearpage")
        print(r"\subsubsection*{" + runner_name + r" Conformance Tests Results}")

        for hpc in HPCS:
            hpc_name = HPC_NAMES.get(hpc, hpc.upper())

            print(r"\begin{table}[ht!]")
            print(r"\centering")
            print(r"\renewcommand{\arraystretch}{1.2}")
            print(r"\setlength{\tabcolsep}{6pt}")

            print(r"\begin{tabular}{|l|c|c|c|c|c|}")
            print(r"\hline")

            print(r"\rowcolor{lightgray!50}")
            print(
                r"\textbf{Version} & \textbf{Mode} & \textbf{Passed} & \textbf{Failed} & \textbf{Skipped} & \textbf{Success (\%)} \\"
            )
            print(r"\hline")

            table_has_rows = False

            for version_key, version_label in CWL_VERSIONS.items():

                if is_failed_run(runner_key, version_key):
                    print(
                        r"\multicolumn{6}{|l|}{\textit{"
                        + f"{version_label}: conformance suite not executed (launch failure)."
                        + r"}} \\ \hline"
                    )
                    print(r"\hline")
                    continue

                version_has_rows = False

                for mode in MODES:
                    rdata = runner_data.get((hpc, mode, version_key))
                    if rdata is None:
                        continue

                    passed, failed, skipped = cell(rdata)
                    pct = success_pct(rdata)

                    mode_label = rf"\texttt{{{MODE_LABELS.get(mode, mode)}}}"

                    print(
                        f"{version_label} & {mode_label} & "
                        f"{passed} & {failed} & {skipped} & {pct} \\\\ \\hline"
                    )

                    version_has_rows = True
                    table_has_rows = True

                if version_has_rows:
                    print(r"\hline")

            print(r"\end{tabular}")

            if table_has_rows:
                print(
                    r"\caption{"
                    + f"{hpc_name} conformance results using {runner_name} across CWL versions."
                    + r"}"
                )
            else:
                print(
                    r"\caption{"
                    + f"{hpc_name} conformance results using {runner_name} (no data available)."
                    + r"}"
                )

            print(r"\end{table}")
            print()

    print(r"\end{document}")


if __name__ == "__main__":
    results = collect_results()
    print_latex(results)
