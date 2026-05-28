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
    print(r"\usepackage{hhline}")
    print(r"\geometry{margin=1in}")
    print(r"\begin{document}")

    col = (
        r"|>{\columncolor{lightgray!30}}c|>{\columncolor{lightgray!30}}c|"
        r"c|c|c|"
        r"c|c|c|"
        r"c|c|c|"
    )

    for runner_key, runner_name in RUNNERS.items():
        print(r"\clearpage")
        print(r"\section*{" + runner_name + r"}")

        print(r"\begin{table}[htbp]")
        print(r"\centering")
        print(r"\setlength{\tabcolsep}{6pt}")
        print(r"\renewcommand{\arraystretch}{1.4}")

        print(r"\begin{tabular}{" + col + r"}")
        print(r"\hline")

        # First Header Row
        print(r"\rowcolor{lightgray!50}")
        print(
            r" & "
            r" & "
            r"\multicolumn{3}{c|}{\textbf{CWL v1.0.2}} & "
            r"\multicolumn{3}{c|}{\textbf{CWL v1.1.0}} & "
            r"\multicolumn{3}{c|}{\textbf{CWL v1.2.1}} \\"
        )

        print(r"\hhline{>{\arrayrulecolor{lightgray!50}}-->{\arrayrulecolor{black}}|---------|}")

        # Second Header Row
        print(r"\rowcolor{lightgray!50}")
        print(
            r"\multirow{-2}{*}{\textbf{HPC}} & "
            r"\multirow{-2}{*}{\textbf{Mode}} & "
            r"\textbf{Passed} & \textbf{Failed} & \textbf{Skipped} & "
            r"\textbf{Passed} & \textbf{Failed} & \textbf{Skipped} & "
            r"\textbf{Passed} & \textbf{Failed} & \textbf{Skipped} \\"
        )

        print(r"\hline")

        # This guarantees "batch" rows show up everywhere, even if the directory was missing.
        runner_data = results_found.get(runner_key, {})

        # Build flat collection array for safe indexing and clean look-ahead grouping
        flat_rows = []
        for hpc in HPCS:
            for mode in MODES:
                flat_rows.append((hpc, mode))

        for i, (hpc, mode) in enumerate(flat_rows):
            r10 = runner_data.get((hpc, mode, "v1.0"))
            r11 = runner_data.get((hpc, mode, "v1.1"))
            r12 = runner_data.get((hpc, mode, "v1.2"))

            def cell(r: Result | None) -> str:
                # If a structural result or folder doesn't exist, output clean "—" tags
                if r is None:
                    return "— — —"
                return f"{r.passed} {r.failed} {r.skipped}"

            print(
                hpc.upper() + r" & " +
                mode + r" & "
                + " & ".join(cell(r10).split()) + " & "
                + " & ".join(cell(r11).split()) + " & "
                + " & ".join(cell(r12).split()) + r" \\"
            )

            # Cluster separation logic (double-rule lines down when HPC changes)
            if i < len(flat_rows) - 1:
                next_hpc = flat_rows[i + 1][0]
                if hpc != next_hpc:
                    print(r"\hline\hline")
                else:
                    print(r"\hline")
            else:
                print(r"\hline")

        print(r"\end{tabular}")
        print(r"\end{table}")

    print(r"\end{document}")


if __name__ == "__main__":
    results = collect_results()
    print_latex(results)
